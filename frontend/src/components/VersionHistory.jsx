import './VersionHistory.css'

function VersionHistory({ versions, currentVersion }) {
  if (versions.length === 0) {
    return (
      <div className="version-history-empty">
        <p>No version history yet. Add more videos to see how your tutorial evolves!</p>
      </div>
    )
  }

  return (
    <div className="version-history">
      <p className="history-intro">
        Track how your tutorial has improved over time as you added more videos.
      </p>
      
      <div className="versions-list">
        {versions.map((version) => (
          <div key={version.id} className="version-item">
            <div className="version-header">
              <div className="version-info">
                <span className={`version-number ${version.version === currentVersion ? 'current' : ''}`}>
                  Version {version.version}
                  {version.version === currentVersion && ' (Current)'}
                </span>
                <span className="version-date">
                  {new Date(version.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </span>
              </div>
            </div>
            
            {version.changes_summary && (
              <div className="changes-summary">
                <strong>Changes:</strong>
                <p>{version.changes_summary}</p>
              </div>
            )}

            <div className="version-stats">
              <span>
                {version.content.steps?.length || 0} steps
              </span>
              <span>
                {version.content.prerequisites?.length || 0} prerequisites
              </span>
              <span>
                {version.content.common_pitfalls?.length || 0} pitfalls
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default VersionHistory
