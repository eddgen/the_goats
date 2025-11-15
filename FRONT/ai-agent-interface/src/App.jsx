import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, Loader2, FileText, Image, X, Settings, Trash2 } from 'lucide-react';

export default function AIAgentModern() {
  const [messages, setMessages] = useState([
    { id: 1, type: 'ai', content: 'Bună! Sunt agentul tău AI. Cum te pot ajuta astăzi?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() && uploadedFiles.length === 0) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input,
      files: [...uploadedFiles]
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setUploadedFiles([]);
    setIsLoading(true);

    // Simulare apel API - înlocuiește cu backend-ul tău
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'Am primit mesajul tău' + (userMessage.files.length > 0 ? ` și ${userMessage.files.length} fișier(e)` : '') + '. Aici ar fi răspunsul de la API-ul tău backend.'
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsLoading(false);
    }, 1500);

    /* 
    // Cod real pentru backend-ul tău:
    try {
      const formData = new FormData();
      formData.append('message', input);
      uploadedFiles.forEach(file => formData.append('files', file));

      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, { id: Date.now(), type: 'ai', content: data.response }]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
    */
  };

  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files);
    setUploadedFiles(prev => [...prev, ...files]);
  };

  const removeFile = (index) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const clearChat = () => {
    setMessages([{ id: 1, type: 'ai', content: 'Bună! Sunt agentul tău AI. Cum te pot ajuta astăzi?' }]);
  };

  return (
    <div className="h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-light text-slate-900">AI Agent</h1>
          <p className="text-sm text-slate-500">Powered by your custom API</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={clearChat}
            className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
            title="Șterge conversația"
          >
            <Trash2 className="w-5 h-5 text-slate-600" />
          </button>
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 hover:bg-slate-100 rounded-lg transition-colors"
            title="Setări"
          >
            <Settings className="w-5 h-5 text-slate-600" />
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="bg-blue-50 border-b border-blue-200 px-6 py-4">
          <h3 className="text-sm font-medium text-slate-700 mb-3">Setări API</h3>
          <div className="grid grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="API Endpoint"
              className="px-4 py-2 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              defaultValue="http://localhost:8000/api"
            />
            <input
              type="text"
              placeholder="API Key (opțional)"
              className="px-4 py-2 rounded-lg border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="w-full space-y-6">
          {messages.map(msg => (
            <div
              key={msg.id}
              className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-2xl rounded-2xl px-6 py-4 ${
                  msg.type === 'user'
                    ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                    : 'bg-white text-slate-800 shadow-sm border border-slate-200'
                }`}
              >
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                {msg.files && msg.files.length > 0 && (
                  <div className="mt-3 space-y-2">
                    {msg.files.map((file, idx) => (
                      <div
                        key={idx}
                        className={`flex items-center gap-2 text-xs ${
                          msg.type === 'user' ? 'text-blue-100' : 'text-slate-600'
                        }`}
                      >
                        {file.type.includes('image') ? (
                          <Image className="w-4 h-4" />
                        ) : (
                          <FileText className="w-4 h-4" />
                        )}
                        <span>{file.name}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-2xl px-6 py-4 shadow-sm border border-slate-200">
                <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Uploaded Files Preview */}
      {uploadedFiles.length > 0 && (
        <div className="px-6 py-3 bg-white border-t border-slate-200">
          <div className="w-full flex flex-wrap gap-2">
            {uploadedFiles.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 bg-slate-100 rounded-lg px-3 py-2 text-sm"
              >
                {file.type.includes('image') ? (
                  <Image className="w-4 h-4 text-slate-600" />
                ) : (
                  <FileText className="w-4 h-4 text-slate-600" />
                )}
                <span className="text-slate-700">{file.name}</span>
                <button
                  onClick={() => removeFile(idx)}
                  className="ml-1 hover:bg-slate-200 rounded p-1"
                >
                  <X className="w-3 h-3 text-slate-600" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white border-t border-slate-200 px-6 py-4">
        <div className="w-full">
          <div className="flex items-end gap-3">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              multiple
              className="hidden"
              accept=".pdf,.doc,.docx,.txt,image/*"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="p-3 hover:bg-slate-100 rounded-xl transition-colors"
              title="Atașează fișiere"
            >
              <Paperclip className="w-5 h-5 text-slate-600" />
            </button>
            
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Scrie un mesaj..."
              className="flex-1 px-4 py-3 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows="1"
              style={{ maxHeight: '120px' }}
            />
            
            <button
              onClick={handleSend}
              disabled={isLoading || (!input.trim() && uploadedFiles.length === 0)}
              className="p-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-sm"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}