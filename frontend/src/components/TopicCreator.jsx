import { useState } from 'react'
import api from '../services/api'
import './TopicCreator.css'

function TopicCreator({ onTopicCreated }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim()) return

    try {
      setLoading(true)
      setError('')
      const response = await api.post('/topics', {
        name: name.trim(),
        description: description.trim() || null
      })
      onTopicCreated(response.data)
      setName('')
      setDescription('')
    } catch (err) {
      setError('Failed to create topic. Please try again.')
      console.error('Error creating topic:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="topic-creator">
      <h3>Create New Topic</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Topic name (e.g., Cursor 2.0 Tutorial)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={loading}
          required
        />
        <textarea
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
          rows="3"
        />
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={loading || !name.trim()}>
          {loading ? 'Creating...' : '+ Create Topic'}
        </button>
      </form>
    </div>
  )
}

export default TopicCreator
