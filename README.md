# 📺 YouTube Tutorial Generator & Refiner

Transform hours of YouTube video content into concise, actionable step-by-step tutorials. Add multiple videos on the same topic and watch as AI intelligently refines and improves your tutorials with each source!

## 🌟 Key Features

- **🎯 Smart Topic Management** - Organize tutorials by subject with completeness tracking
- **📹 Automatic Video Processing** - Extract transcripts from any YouTube video with captions
- **✨ AI-Powered Generation** - Convert transcripts into structured, actionable tutorials
- **🔄 Intelligent Refinement** - Each video you add improves the tutorial
- **📜 Version History** - Track how your tutorials evolve over time
- **🎨 Beautiful UI** - Modern, responsive interface with smooth animations

## 🚀 The Magic: Multi-Source Refinement

The killer feature! Unlike tools that just convert one video at a time:

1. **First video** → Generates initial tutorial
2. **Second video** → AI analyzes gaps and adds missing details
3. **Third video** → Fills in edge cases and alternative approaches
4. **Result** → A comprehensive guide combining the best insights from all sources

Perfect for learning complex topics where no single video covers everything!

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python)
- SQLAlchemy + SQLite/PostgreSQL
- youtube-transcript-api
- Anthropic Claude 3.5 Sonnet

**Frontend:**
- React 18
- Vite
- Modern CSS with animations

## 📦 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run server
python run.py
```

Backend runs at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at `http://localhost:3000`

## 📖 Usage

1. **Create a Topic** - E.g., "Cursor 2.0 Tutorial"
2. **Add First Video** - Paste YouTube URL, AI generates initial tutorial
3. **Add More Videos** - Each video refines and improves the tutorial
4. **View History** - See what changed and why
5. **Learn Efficiently** - Follow the consolidated guide instead of watching hours of video!

## 🎯 Perfect For

- **Learning software tools** - Combine multiple tutorials into one comprehensive guide
- **Technical skills** - Programming, design, data science, etc.
- **Productivity tools** - Master complex software quickly
- **Course creation** - Research and consolidate information from multiple sources

## 🏗️ Project Structure

```
youtube-tutorial-app/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── main.py      # App initialization
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # API schemas
│   │   ├── routes/      # API endpoints
│   │   └── services/    # Business logic
│   └── requirements.txt
├── frontend/            # React app
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── services/    # API client
│   │   └── App.jsx
│   └── package.json
├── PROJECT_PLAN.md      # Detailed technical plan
├── SETUP_GUIDE.md       # Step-by-step setup instructions
└── README.md            # This file
```

## 🔮 Future Enhancements

- Export to PDF/Markdown
- Browser extension for quick capture
- Playlist batch processing
- User accounts and sharing
- Integration with note-taking apps
- AI-suggested related videos

## 📝 How It Works

1. **Transcript Extraction** - Uses youtube-transcript-api to get video captions
2. **AI Analysis** - Claude 3.5 Sonnet analyzes content and identifies key steps
3. **Tutorial Generation** - Structures content into overview, prerequisites, steps, pitfalls, and verification
4. **Intelligent Refinement** - When adding more videos, AI:
   - Identifies new information
   - Fills gaps in existing tutorial
   - Merges complementary details
   - Resolves contradictions
   - Tracks changes

## 🤝 Contributing

This is a working MVP! Contributions welcome:
- Bug reports and fixes
- Feature requests
- UI/UX improvements
- Documentation

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Acknowledgments

- Anthropic Claude for powerful AI generation
- youtube-transcript-api for easy transcript access
- The open source community

---

**Ready to turn video marathons into quick action plans?** Get started with [SETUP_GUIDE.md](SETUP_GUIDE.md)! 🚀
