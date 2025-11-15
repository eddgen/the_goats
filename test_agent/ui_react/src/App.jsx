import { useState, useRef, useEffect } from 'react'
import { Send, Upload, X, Trash2, Dumbbell, Activity, Apple, MessageSquare, Refrigerator } from 'lucide-react'
import './App.css'

function App() {
  // Tab state
  const [activeTab, setActiveTab] = useState('chat') // 'chat' or 'fridge'
  
  // Chat state
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [images, setImages] = useState([]) // Multiple images
  const [imagePreviews, setImagePreviews] = useState([]) // Multiple previews
  const [isLoading, setIsLoading] = useState(false)
  
  // Fridge state
  const [fridgeImage, setFridgeImage] = useState(null)
  const [fridgeImagePreview, setFridgeImagePreview] = useState(null)
  const [fridgeInventory, setFridgeInventory] = useState(() => {
    // Load from localStorage
    const saved = localStorage.getItem('fridgeInventory')
    return saved ? JSON.parse(saved) : null
  })
  const [analyzingFridge, setAnalyzingFridge] = useState(false)
  
  const fileInputRef = useRef(null)
  const fridgeFileInputRef = useRef(null)
  const messagesEndRef = useRef(null)

  // Save fridge inventory to localStorage whenever it changes
  useEffect(() => {
    if (fridgeInventory) {
      localStorage.setItem('fridgeInventory', JSON.stringify(fridgeInventory))
    }
  }, [fridgeInventory])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files)
    if (files.length > 0) {
      // Add new images to existing ones
      setImages(prev => [...prev, ...files])
      
      // Generate previews for new images
      files.forEach(file => {
        const reader = new FileReader()
        reader.onloadend = () => {
          setImagePreviews(prev => [...prev, reader.result])
        }
        reader.readAsDataURL(file)
      })
    }
  }

  const removeImage = (index) => {
    setImages(prev => prev.filter((_, i) => i !== index))
    setImagePreviews(prev => prev.filter((_, i) => i !== index))
  }

  const clearAllImages = () => {
    setImages([])
    setImagePreviews([])
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const sendMessage = async () => {
    if (!input.trim() && images.length === 0) return

    const userMessage = {
      role: 'user',
      content: input,
      images: [...imagePreviews], // Store all image previews
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Simulate API call to Python backend
      const formData = new FormData()
      formData.append('message', input)
      // Append all images
      images.forEach((img, index) => {
        formData.append('images', img)
      })

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
      clearAllImages() // Clear all images after sending
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

  // Fridge functions
  const handleFridgeImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      setFridgeImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setFridgeImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const analyzeFridge = async () => {
    if (!fridgeImage) return

    setAnalyzingFridge(true)
    try {
      const formData = new FormData()
      formData.append('message', 'Analyze my fridge contents using the analyze_fridge tool')
      formData.append('images', fridgeImage)

      const response = await fetch('/api/chat', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('API call failed')
      }

      const data = await response.json()
      
      // Parse the response to extract food data
      // The agent's response may contain the data in various formats
      let foods = []
      let rawResponse = data.response
      
      try {
        const responseText = data.response
        
        // First, try to find [DATA]...[/DATA] tags
        const dataTagMatch = responseText.match(/\[DATA\]([\s\S]*?)\[\/DATA\]/);
        if (dataTagMatch) {
          const parsedData = JSON.parse(dataTagMatch[1].trim())
          foods = parsedData.foods || []
          // Remove the data tags from the display
          rawResponse = responseText.replace(/\[DATA\][\s\S]*?\[\/DATA\]/g, '').trim()
        } else {
          // Try to find JSON object in the response
          const jsonMatch = responseText.match(/\{[\s\S]*"foods"[\s\S]*?\}/);
          if (jsonMatch) {
            const parsedData = JSON.parse(jsonMatch[0])
            foods = parsedData.foods || []
          }
        }
      } catch (parseError) {
        console.log('Could not parse structured data from response:', parseError)
      }
      
      setFridgeInventory({
        analyzedAt: new Date().toISOString(),
        imagePreview: fridgeImagePreview,
        foods: foods,
        rawResponse: foods.length === 0 ? rawResponse : null
      })

    } catch (error) {
      // Mock response for demo
      setFridgeInventory({
        analyzedAt: new Date().toISOString(),
        imagePreview: fridgeImagePreview,
        foods: [
          { name: 'Eggs', quantity: '6 eggs', calories_per_serving: 70, category: 'protein', freshness: 'fresh' },
          { name: 'Chicken Breast', quantity: '300g', calories_per_serving: 165, category: 'protein', freshness: 'fresh' },
          { name: 'Milk', quantity: '500ml', calories_per_serving: 42, category: 'dairy', freshness: 'fresh' },
          { name: 'Greek Yogurt', quantity: '200g', calories_per_serving: 100, category: 'dairy', freshness: 'fresh' },
          { name: 'Broccoli', quantity: '200g', calories_per_serving: 55, category: 'vegetables', freshness: 'fresh' },
          { name: 'Tomatoes', quantity: '4 tomatoes', calories_per_serving: 22, category: 'vegetables', freshness: 'consume_soon' },
          { name: 'Spinach', quantity: '100g', calories_per_serving: 23, category: 'vegetables', freshness: 'fresh' },
          { name: 'Bananas', quantity: '3 bananas', calories_per_serving: 105, category: 'fruits', freshness: 'fresh' },
          { name: 'Apples', quantity: '2 apples', calories_per_serving: 95, category: 'fruits', freshness: 'fresh' },
          { name: 'Rice', quantity: '1kg', calories_per_serving: 130, category: 'carbs', freshness: 'fresh' },
          { name: 'Whole Wheat Bread', quantity: '1 loaf', calories_per_serving: 80, category: 'carbs', freshness: 'fresh' }
        ],
        rawResponse: '🤖 Mock: Backend not connected. Start with python api/server.py'
      })
    } finally {
      setAnalyzingFridge(false)
    }
  }

  const clearFridge = () => {
    setFridgeInventory(null)
    localStorage.removeItem('fridgeInventory')
  }

  const examplePrompts = [
    "Calculate my BMI (75kg, 175cm)",
    "Generate meal plan for 2000 calories",
    "What's in my fridge? (upload photo)",
    "Suggest dinner with 600 calories from fridge"
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

        {/* Tab Navigation */}
        <div className="tabs-container">
          <button 
            className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            <MessageSquare size={18} />
            <span>Chat</span>
          </button>
          <button 
            className={`tab ${activeTab === 'fridge' ? 'active' : ''}`}
            onClick={() => setActiveTab('fridge')}
          >
            <Refrigerator size={18} />
            <span>Fridge</span>
          </button>
        </div>

        {/* Chat Tab Content */}
        {activeTab === 'chat' && (
          <>
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
                <li>🥘 Smart fridge analysis & meal suggestions</li>
                <li>💪 Workout plan generation</li>
                <li>📸 Image analysis for body fat & transformation</li>
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
                {msg.images && msg.images.length > 0 && (
                  <div className="message-images">
                    {msg.images.map((img, imgIdx) => (
                      <img key={imgIdx} src={img} alt={`Uploaded ${imgIdx + 1}`} className="message-image" />
                    ))}
                  </div>
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
          {imagePreviews.length > 0 && (
            <div className="images-preview-container">
              {imagePreviews.map((preview, idx) => (
                <div key={idx} className="image-preview">
                  <img src={preview} alt={`Preview ${idx + 1}`} />
                  <button onClick={() => removeImage(idx)} className="remove-image-btn">
                    <X size={16} />
                  </button>
                </div>
              ))}
            </div>
          )}

          <div className="input-wrapper">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleImageUpload}
              accept="image/*"
              multiple
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
              disabled={!input.trim() && images.length === 0}
              className="send-btn"
            >
              <Send size={20} />
            </button>
          </div>

          <div className="input-hint">
            💡 Upload multiple images for body fat analysis or transformation tracking (before/after)
            {imagePreviews.length > 0 && (
              <span className="image-count"> • {imagePreviews.length} image{imagePreviews.length > 1 ? 's' : ''} selected</span>
            )}
          </div>
        </div>
          </>
        )}

        {/* Fridge Tab Content */}
        {activeTab === 'fridge' && (
          <div className="fridge-tab">
            <div className="fridge-layout">
              {/* Left side - Upload */}
              <div className="fridge-upload-section">
                <h2>📸 Fridge Photo</h2>
                {!fridgeImagePreview ? (
                  <div className="fridge-upload-area">
                    <input
                      type="file"
                      ref={fridgeFileInputRef}
                      onChange={handleFridgeImageUpload}
                      accept="image/*"
                      className="file-input"
                    />
                    <button
                      onClick={() => fridgeFileInputRef.current?.click()}
                      className="fridge-upload-btn"
                    >
                      <Upload size={48} />
                      <p>Upload Fridge Photo</p>
                      <span>Click to select image</span>
                    </button>
                  </div>
                ) : (
                  <div className="fridge-image-preview">
                    <img src={fridgeImagePreview} alt="Fridge" />
                    <div className="fridge-image-actions">
                      <button 
                        onClick={analyzeFridge}
                        disabled={analyzingFridge}
                        className="analyze-btn"
                      >
                        {analyzingFridge ? '🔄 Analyzing...' : '🔍 Analyze Fridge'}
                      </button>
                      <button 
                        onClick={() => {
                          setFridgeImage(null)
                          setFridgeImagePreview(null)
                          if (fridgeFileInputRef.current) {
                            fridgeFileInputRef.current.value = ''
                          }
                        }}
                        className="change-photo-btn"
                      >
                        <X size={16} /> Change Photo
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Right side - Inventory List */}
              <div className="fridge-inventory-section">
                <div className="inventory-header">
                  <h2>🥗 Inventory</h2>
                  {fridgeInventory && (
                    <button onClick={clearFridge} className="clear-inventory-btn">
                      <Trash2 size={16} /> Clear
                    </button>
                  )}
                </div>
                
                {!fridgeInventory ? (
                  <div className="empty-inventory">
                    <Refrigerator size={64} className="empty-icon" />
                    <p>No fridge data yet</p>
                    <span>Upload a photo and analyze to see your inventory</span>
                  </div>
                ) : (
                  <div className="inventory-content">
                    <div className="inventory-meta">
                      <p className="analyzed-time">
                        📅 Analyzed: {new Date(fridgeInventory.analyzedAt).toLocaleString()}
                      </p>
                    </div>

                    {fridgeInventory.foods && fridgeInventory.foods.length > 0 ? (
                      <>
                        {/* Summary Stats */}
                        <div className="inventory-stats">
                          <div className="stat-item">
                            <span className="stat-number">{fridgeInventory.foods.length}</span>
                            <span className="stat-label">Total Items</span>
                          </div>
                          <div className="stat-item">
                            <span className="stat-number">
                              {fridgeInventory.foods.filter(f => f.category === 'protein').length}
                            </span>
                            <span className="stat-label">🍖 Proteins</span>
                          </div>
                          <div className="stat-item">
                            <span className="stat-number">
                              {fridgeInventory.foods.filter(f => f.category === 'vegetables').length}
                            </span>
                            <span className="stat-label">🥗 Veggies</span>
                          </div>
                          <div className="stat-item">
                            <span className="stat-number">
                              {fridgeInventory.foods.filter(f => f.category === 'fruits').length}
                            </span>
                            <span className="stat-label">🍎 Fruits</span>
                          </div>
                        </div>

                        {/* Grouped by Category */}
                        {['protein', 'vegetables', 'fruits', 'dairy', 'carbs', 'fats', 'other'].map(category => {
                          const categoryFoods = fridgeInventory.foods.filter(f => f.category === category)
                          if (categoryFoods.length === 0) return null

                          const categoryIcons = {
                            protein: '🍖',
                            vegetables: '🥗',
                            fruits: '🍎',
                            dairy: '🥛',
                            carbs: '🍚',
                            fats: '🧈',
                            other: '🍴'
                          }

                          const categoryNames = {
                            protein: 'Proteins',
                            vegetables: 'Vegetables',
                            fruits: 'Fruits',
                            dairy: 'Dairy',
                            carbs: 'Carbohydrates',
                            fats: 'Fats',
                            other: 'Other'
                          }

                          return (
                            <div key={category} className="category-section">
                              <h3 className="category-title">
                                {categoryIcons[category]} {categoryNames[category]} ({categoryFoods.length})
                              </h3>
                              <div className="foods-list">
                                {categoryFoods.map((food, idx) => (
                                  <div key={idx} className="food-item">
                                    <div className="food-icon">{categoryIcons[category]}</div>
                                    <div className="food-details">
                                      <div className="food-header">
                                        <h4>{food.name}</h4>
                                        {food.calories_per_serving && (
                                          <span className="calories-badge">
                                            {typeof food.calories_per_serving === 'number' 
                                              ? `${food.calories_per_serving} cal`
                                              : food.calories_per_serving}
                                          </span>
                                        )}
                                      </div>
                                      <p className="food-quantity">{food.quantity}</p>
                                      <div className="food-meta">
                                        <span className={`freshness ${food.freshness}`}>
                                          {food.freshness === 'fresh' && '✅ Fresh'}
                                          {food.freshness === 'consume_soon' && '⚠️ Consume Soon'}
                                          {food.freshness === 'check_expiry' && '🚨 Check Expiry'}
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )
                        })}
                      </>
                    ) : (
                      <div className="raw-response">
                        <p>{fridgeInventory.rawResponse}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
