import { useState } from 'react'
import api from '../services/api'
import './VideoAdder.css'

function VideoAdder({ topicId, onVideoAdded }) {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!url.trim()) return

    try {
      setLoading(true)
      setError('')
      setSuccess('')

      const response = await api.post(`/topics/${topicId}/videos`, {
        youtube_url: url.trim()
      })

      setSuccess(`Video ${response.data.action} successfully! Tutorial version: ${response.data.tutorial_version}`)
      setUrl('')
      onVideoAdded()

      // Clear success message after 5 seconds
      setTimeout(() => setSuccess(''), 5000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add video. Please check the URL and try again.')
      console.error('Error adding video:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="video-adder">
      <h3>Add YouTube Video</h3>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="url"
            placeholder="Paste YouTube URL here (e.g., https://www.youtube.com/watch?v=...)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={loading}
            required
          />
          <button type="submit" disabled={loading || !url.trim()}>
            {loading ? (
              <>
                <span className="spinner"></span>
                Processing...
              </>
            ) : (
              '+ Add Video'
            )}
          </button>
        </div>
        {error && <div className="message error">{error}</div>}
        {success && <div className="message success">{success}</div>}
      </form>
      {loading && (
        <div className="processing-info">
          <p>⏳ Processing video... This may take 30-60 seconds.</p>
          <p className="small">Extracting transcript and generating/refining tutorial with AI...</p>
        </div>
      )}
    </div>
  )
}

export default VideoAdder
