import { useState, useEffect } from 'react'
import api from '../services/api'
import VideoAdder from './VideoAdder'
import TutorialViewer from './TutorialViewer'
import VersionHistory from './VersionHistory'
import './TopicDetail.css'

function TopicDetail({ topic, onTopicUpdated }) {
  const [tutorial, setTutorial] = useState(null)
  const [versions, setVersions] = useState([])
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('tutorial')

  useEffect(() => {
    loadTutorial()
  }, [topic.id])

  const loadTutorial = async () => {
    try {
      setLoading(true)
      const response = await api.get(`/topics/${topic.id}/tutorial`)
      setTutorial(response.data)
      
      // Load versions
      const versionsResponse = await api.get(`/topics/${topic.id}/tutorial/versions`)
      setVersions(versionsResponse.data)
    } catch (error) {
      if (error.response?.status !== 404) {
        console.error('Error loading tutorial:', error)
      }
      setTutorial(null)
    } finally {
      setLoading(false)
    }
  }

  const handleVideoAdded = () => {
    loadTutorial()
    onTopicUpdated()
  }

  return (
    <div className="topic-detail">
      <div className="topic-header">
        <div>
          <h2>{topic.name}</h2>
          {topic.description && <p className="topic-description">{topic.description}</p>}
        </div>
        <div className="topic-stats">
          <span className="stat">
            <strong>{topic.videos?.length || 0}</strong> videos
          </span>
          <span className="stat">
            <strong>{Math.round(topic.completeness_score * 100)}%</strong> complete
          </span>
        </div>
      </div>

      <VideoAdder topicId={topic.id} onVideoAdded={handleVideoAdded} />

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'tutorial' ? 'active' : ''}`}
          onClick={() => setActiveTab('tutorial')}
        >
          📋 Tutorial
        </button>
        <button
          className={`tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          📜 Version History ({versions.length})
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'tutorial' && (
          loading ? (
            <div className="loading-tutorial">Loading tutorial...</div>
          ) : tutorial ? (
            <TutorialViewer tutorial={tutorial} />
          ) : (
            <div className="no-tutorial">
              <h3>No tutorial yet</h3>
              <p>Add a YouTube video to generate your first tutorial!</p>
            </div>
          )
        )}

        {activeTab === 'history' && (
          <VersionHistory versions={versions} currentVersion={tutorial?.version} />
        )}
      </div>
    </div>
  )
}

export default TopicDetail
