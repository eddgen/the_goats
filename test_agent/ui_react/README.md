# FitCoach AI - React UI

Modern, beautiful React interface for FitCoach AI fitness assistant.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ui_react
npm install
```

### 2. Start Backend (Python FastAPI)

```bash
# Install backend dependencies
pip install fastapi uvicorn python-multipart

# Run backend server
python api/server.py
```

Backend runs on: `http://localhost:8000`

### 3. Start Frontend (React)

```bash
# In ui_react folder
npm run dev
```

Frontend runs on: `http://localhost:3000`

## ✨ Features

- **Modern UI** - Beautiful gradient design with smooth animations
- **Real-time Chat** - Instant messaging with the AI agent
- **Multiple Image Upload** - Upload 1 or more images at once
  - Single image → Body fat analysis
  - Two images → Before/After transformation comparison
- **Image Preview** - See all uploaded images before sending (with individual remove buttons)
- **Example Prompts** - Quick start buttons for common queries
- **Typing Indicator** - Shows when AI is thinking
- **Auto-scroll** - Automatically scrolls to latest message
- **Responsive** - Works on desktop, tablet, and mobile
- **Dark gradient theme** - Eye-catching purple gradient background

## 📸 How to Use Images

### Single Image Analysis
1. Click the upload button (📤)
2. Select 1 image of your body
3. Type: "Analyze my body fat percentage"
4. Click send - image will be analyzed and cleared from input

### Transformation Comparison (Before/After)
1. Click the upload button (📤)
2. Select 2 images:
   - First image = BEFORE photo
   - Second image = AFTER photo
3. Type: "Compare my transformation" or "Analyze my progress"
4. Click send - agent calls `visualize_transformation()` automatically

### Multiple Images
- You can upload as many images as needed
- Each image shows preview with X button to remove
- After sending, all images are cleared automatically
- Images appear in your chat message in a grid layout

## 🎨 Design Features

- Gradient purple theme (667eea → 764ba2)
- Smooth animations and transitions
- Chat bubbles with rounded corners
- Avatar icons for user/assistant
- Welcome screen with feature highlights
- Clean, minimalist interface
- Professional typography

## 🔧 Tech Stack

- **Frontend**: React 18 + Vite
- **Backend**: FastAPI (Python)
- **Icons**: Lucide React
- **HTTP**: Axios
- **Styling**: Pure CSS with gradients

## 📁 Project Structure

```
ui_react/
├── src/
│   ├── App.jsx          # Main component
│   ├── App.css          # Styles
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── package.json
├── vite.config.js
└── index.html

api/
└── server.py            # FastAPI backend
```

## 🎯 Usage

1. **Text Chat**: Type message and press Enter or click Send
2. **Image Upload**: Click upload icon, select image, then send message
3. **Example Prompts**: Click any example button to auto-fill input
4. **Clear Chat**: Click trash icon in header to reset conversation

## 🔌 API Endpoints

- `POST /api/chat` - Send message with optional image
- `POST /api/reset` - Reset conversation
- `GET /api/health` - Health check

## 💡 Example Interactions

**Calculate BMI:**
```
"I'm 75kg and 175cm, calculate my BMI"
```

**Body Fat Analysis:**
1. Upload body photo
2. Type: "Analyze body fat from this image"

**Meal Planning:**
```
"Generate a 2000 calorie meal plan with balanced diet"
```

**Calorie Tracking:**
```
"Track calories for: 100g oats, 300ml milk, 5 eggs"
```

## 🐛 Troubleshooting

**Backend not connecting:**
- Make sure Python server is running: `python api/server.py`
- Check `.env` has `OPENAI_API_KEY`

**CORS errors:**
- Backend should allow `http://localhost:3000`
- Check FastAPI CORS middleware

**Image upload fails:**
- Check `data/uploads/` folder exists
- Verify file size < 10MB

## 📱 Responsive Design

- Desktop: Full chat experience
- Tablet: Optimized layout
- Mobile: Touch-friendly interface

## 🎨 Customization

Edit `src/App.css` to customize:
- Colors: Change gradient values
- Fonts: Modify font-family
- Spacing: Adjust padding/margins
- Animations: Edit keyframes

Enjoy your beautiful FitCoach AI interface! 🏋️✨
