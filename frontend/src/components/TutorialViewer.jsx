import './TutorialViewer.css'

function TutorialViewer({ tutorial }) {
  const content = tutorial.content

  return (
    <div className="tutorial-viewer">
      <div className="tutorial-meta">
        <span className="version-badge">Version {tutorial.version}</span>
        {tutorial.source_video_ids && (
          <span className="sources">
            Based on {tutorial.source_video_ids.length} video{tutorial.source_video_ids.length !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      {tutorial.refinement_notes && (
        <div className="refinement-notes">
          <strong>Latest Changes:</strong>
          <p>{tutorial.refinement_notes}</p>
        </div>
      )}

      {content.overview && (
        <section className="tutorial-section">
          <h3>📖 Overview</h3>
          <p className="overview">{content.overview}</p>
        </section>
      )}

      {content.prerequisites && content.prerequisites.length > 0 && (
        <section className="tutorial-section">
          <h3>✅ Prerequisites</h3>
          <ul className="prerequisites">
            {content.prerequisites.map((prereq, index) => (
              <li key={index}>{prereq}</li>
            ))}
          </ul>
        </section>
      )}

      {content.steps && content.steps.length > 0 && (
        <section className="tutorial-section">
          <h3>🚀 Step-by-Step Instructions</h3>
          <div className="steps">
            {content.steps.map((step) => (
              <div key={step.step_number} className="step">
                <div className="step-header">
                  <span className="step-number">{step.step_number}</span>
                  <h4>{step.title}</h4>
                </div>
                <p className="step-description">{step.description}</p>
                {step.details && step.details.length > 0 && (
                  <ul className="step-details">
                    {step.details.map((detail, index) => (
                      <li key={index}>{detail}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {content.common_pitfalls && content.common_pitfalls.length > 0 && (
        <section className="tutorial-section">
          <h3>⚠️ Common Pitfalls</h3>
          <ul className="pitfalls">
            {content.common_pitfalls.map((pitfall, index) => (
              <li key={index}>{pitfall}</li>
            ))}
          </ul>
        </section>
      )}

      {content.verification && content.verification.length > 0 && (
        <section className="tutorial-section">
          <h3>✨ Verification</h3>
          <ul className="verification">
            {content.verification.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}

export default TutorialViewer
