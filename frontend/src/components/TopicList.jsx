import './TopicList.css'

function TopicList({ topics, selectedTopic, onTopicSelect, loading }) {
  if (loading) {
    return (
      <div className="topic-list">
        <h3>Your Topics</h3>
        <div className="loading">Loading topics...</div>
      </div>
    )
  }

  if (topics.length === 0) {
    return (
      <div className="topic-list">
        <h3>Your Topics</h3>
        <div className="empty">
          <p>No topics yet. Create one to get started!</p>
        </div>
      </div>
    )
  }

  return (
    <div className="topic-list">
      <h3>Your Topics ({topics.length})</h3>
      <div className="topics">
        {topics.map((topic) => (
          <div
            key={topic.id}
            className={`topic-item ${selectedTopic?.id === topic.id ? 'active' : ''}`}
            onClick={() => onTopicSelect(topic)}
          >
            <div className="topic-name">{topic.name}</div>
            <div className="topic-meta">
              <span className="video-count">{topic.videos?.length || 0} videos</span>
              <span className="completeness">
                {Math.round(topic.completeness_score * 100)}% complete
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TopicList
