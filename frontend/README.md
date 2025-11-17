# YouTube Tutorial Generator - Frontend

React frontend for the YouTube Tutorial Generator & Refiner app.

## Setup

1. **Install Node.js 18+**

2. **Install dependencies**
```bash
cd frontend
npm install
```

3. **Start development server**
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Features

### 🎯 Topic Management
- Create topics to organize tutorials
- Track completeness score
- View number of source videos

### 📹 Video Processing
- Paste YouTube URLs
- Real-time processing feedback
- Automatic transcript extraction

### ✨ AI Tutorial Generation
- First video generates initial tutorial
- Each additional video refines and improves
- Track changes with version history

### 📋 Tutorial Display
- Beautiful, readable format
- Overview, prerequisites, steps
- Common pitfalls and verification steps
- Step-by-step instructions with details

### 📜 Version History
- See how tutorials evolve
- Track what changed and why
- Compare versions

## Components

```
src/
├── components/
│   ├── TopicCreator.jsx      # Create new topics
│   ├── TopicList.jsx          # List of topics
│   ├── TopicDetail.jsx        # Topic details and tutorial
│   ├── VideoAdder.jsx         # Add YouTube videos
│   ├── TutorialViewer.jsx     # Display tutorials
│   └── VersionHistory.jsx     # Show version history
├── services/
│   └── api.js                 # API client
└── App.jsx                    # Main app component
```

## Technologies

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Modern styling with gradients and animations

## Building for Production

```bash
npm run build
```

Output will be in `dist/` directory.

## Configuration

The app expects the backend API at `http://localhost:8000`. To change this, edit `src/services/api.js`.

## Design

The UI features:
- Modern gradient backgrounds
- Smooth animations and transitions
- Responsive design (mobile-friendly)
- Clear visual hierarchy
- Loading states and error handling
- Real-time feedback during processing
