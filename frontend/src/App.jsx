import { useState, useEffect } from 'react'
import './App.css'
import TopicList from './components/TopicList'
import TopicCreator from './components/TopicCreator'
import TopicDetail from './components/TopicDetail'
import api from './services/api'

function App() {
  const [topics, setTopics] = useState([])
  const [selectedTopic, setSelectedTopic] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadTopics()
  }, [])

  const loadTopics = async () => {
    try {
      setLoading(true)
      const response = await api.get('/topics')
      setTopics(response.data)
    } catch (error) {
      console.error('Error loading topics:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleTopicCreated = (newTopic) => {
    setTopics([...topics, newTopic])
    setSelectedTopic(newTopic)
  }

  const handleTopicSelect = (topic) => {
    setSelectedTopic(topic)
  }

  const handleTopicUpdated = () => {
    loadTopics()
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📺 YouTube Tutorial Generator</h1>
        <p>Turn hours of video content into actionable step-by-step guides</p>
      </header>

      <div className="app-container">
        <aside className="sidebar">
          <TopicCreator onTopicCreated={handleTopicCreated} />
          <TopicList 
            topics={topics} 
            selectedTopic={selectedTopic}
            onTopicSelect={handleTopicSelect}
            loading={loading}
          />
        </aside>

        <main className="main-content">
          {selectedTopic ? (
            <TopicDetail 
              topic={selectedTopic} 
              onTopicUpdated={handleTopicUpdated}
            />
          ) : (
            <div className="welcome">
              <h2>👋 Welcome!</h2>
              <p>Create a new topic or select an existing one to get started.</p>
              <div className="features">
                <div className="feature">
                  <span className="feature-icon">🎯</span>
                  <h3>Create Topics</h3>
                  <p>Organize tutorials by subject</p>
                </div>
                <div className="feature">
                  <span className="feature-icon">📹</span>
                  <h3>Add Videos</h3>
                  <p>Paste YouTube URLs to process</p>
                </div>
                <div className="feature">
                  <span className="feature-icon">✨</span>
                  <h3>AI Refinement</h3>
                  <p>Tutorials improve with each video</p>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default App
