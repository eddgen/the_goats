import { useState, useRef, useEffect } from 'react'
import { Send, Upload, X, Trash2, Dumbbell, Activity, Apple } from 'lucide-react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [image, setImage] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const fileInputRef = useRef(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const removeImage = () => {
    setImage(null)
    setImagePreview(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const sendMessage = async () => {
    if (!input.trim() && !image) return

    const userMessage = {
      role: 'user',
      content: input,
      image: imagePreview,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Simulate API call to Python backend
      const formData = new FormData()
      formData.append('message', input)
      if (image) {
        formData.append('image', image)
      }

      // TODO: Replace with actual API endpoint
      const response = await fetch('/api/chat', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('API call failed')
      }

      const data = await response.json()

      const assistantMessage = {
        role: 'assistant',
        content: data.response || 'Sorry, I encountered an error. Please make sure the Python backend is running.',
        timestamp: new Date().toISOString()
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      // Mock response for demo
      const mockResponse = {
        role: 'assistant',
        content: `🤖 Mock Response (Backend not connected):\n\nYou said: "${input}"\n\nTo connect to the real agent, start the Python backend server:\n\npython api/server.py\n\nThen I'll be able to:\n- Calculate BMI\n- Analyze body fat from images\n- Generate meal plans\n- Track calories\n- And more!`,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, mockResponse])
    } finally {
      setIsLoading(false)
      removeImage()
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const clearChat = () => {
    setMessages([])
  }

  const examplePrompts = [
    "Calculate my BMI (75kg, 175cm)",
    "Generate meal plan for 2000 calories",
    "Track: 100g oats, 300ml milk, 5 eggs",
    "Analyze body fat from uploaded image"
  ]

  return (
    <div className="app-container">
      <div className="chat-container">
        {/* Header */}
        <div className="header">
          <div className="header-content">
            <div className="header-left">
              <Dumbbell className="logo" size={32} />
              <div>
                <h1>FitCoach AI</h1>
                <p className="subtitle">Personal Fitness & Nutrition Assistant</p>
              </div>
            </div>
            <button onClick={clearChat} className="clear-btn" title="Clear chat">
              <Trash2 size={20} />
            </button>
          </div>
        </div>

        {/* Features bar */}
        <div className="features-bar">
          <div className="feature">
            <Activity size={16} />
            <span>Body Analysis</span>
          </div>
          <div className="feature">
            <Apple size={16} />
            <span>Nutrition</span>
          </div>
          <div className="feature">
            <Dumbbell size={16} />
            <span>Workouts</span>
          </div>
        </div>

        {/* Messages */}
        <div className="messages-container">
          {messages.length === 0 && (
            <div className="welcome-screen">
              <Dumbbell size={64} className="welcome-icon" />
              <h2>Welcome to FitCoach AI!</h2>
              <p>I'm your AI fitness and nutrition assistant. I can help you with:</p>
              <ul className="welcome-list">
                <li>📊 Body composition analysis (BMI, body fat %)</li>
                <li>🍽️ Personalized meal planning & calorie tracking</li>
                <li>💪 Workout plan generation</li>
                <li>📸 Image analysis for body fat estimation</li>
              </ul>
              <div className="example-prompts">
                <p className="example-title">Try these prompts:</p>
                <div className="example-grid">
                  {examplePrompts.map((prompt, idx) => (
                    <button
                      key={idx}
                      className="example-btn"
                      onClick={() => setInput(prompt)}
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-avatar">
                {msg.role === 'user' ? '👤' : '🏋️'}
              </div>
              <div className="message-content">
                {msg.image && (
                  <img src={msg.image} alt="Uploaded" className="message-image" />
                )}
                <div className="message-text">
                  {msg.content.split('\n').map((line, i) => (
                    <p key={i}>{line}</p>
                  ))}
                </div>
                <div className="message-time">
                  {new Date(msg.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message assistant">
              <div className="message-avatar">🏋️</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input area */}
        <div className="input-container">
          {imagePreview && (
            <div className="image-preview">
              <img src={imagePreview} alt="Preview" />
              <button onClick={removeImage} className="remove-image-btn">
                <X size={16} />
              </button>
            </div>
          )}

          <div className="input-wrapper">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleImageUpload}
              accept="image/*"
              className="file-input"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="upload-btn"
              title="Upload image"
            >
              <Upload size={20} />
            </button>

            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message... (e.g., 'I'm 75kg and 175cm, calculate my BMI')"
              className="message-input"
              rows="1"
            />

            <button
              onClick={sendMessage}
              disabled={!input.trim() && !image}
              className="send-btn"
            >
              <Send size={20} />
            </button>
          </div>

          <div className="input-hint">
            💡 Upload images for body fat analysis or transformation tracking
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
