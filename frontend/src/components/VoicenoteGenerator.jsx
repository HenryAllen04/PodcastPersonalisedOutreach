// Purpose: Main voicenote generation component for PODVOX workflow

import { useState } from 'react'
import { HiMicrophone, HiPlay, HiArrowPath, HiCloudArrowDown, HiExclamationTriangle } from 'react-icons/hi2'
import './VoicenoteGenerator.css'

const VoicenoteGenerator = () => {
  const [formData, setFormData] = useState({
    videoUrl: '',
    topic: '',
    prospectName: ''
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [currentStage, setCurrentStage] = useState('')

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const generateVoicenote = async () => {
    if (!formData.videoUrl || !formData.topic) {
      setError('Please provide both a video URL and topic')
      return
    }

    setIsProcessing(true)
    setError(null)
    setResult(null)
    setCurrentStage('Initializing...')

    try {
      // Create form data for the API call
      const apiFormData = new FormData()
      apiFormData.append('video_url', formData.videoUrl)
      apiFormData.append('topic', formData.topic)
      if (formData.prospectName) {
        apiFormData.append('prospect_name', formData.prospectName)
      }

      setCurrentStage('🎯 Stage 1: Extracting moments from video...')
      
      const response = await fetch('http://localhost:8000/generate-voicenote-simple', {
        method: 'POST',
        body: apiFormData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate voicenote')
      }

      const data = await response.json()
      
      if (data.success) {
        setResult(data)
        setCurrentStage('✅ Complete! Voicenote ready for download')
      } else {
        throw new Error(data.error || 'Voicenote generation failed')
      }

    } catch (err) {
      setError(err.message)
      setCurrentStage('')
    } finally {
      setIsProcessing(false)
    }
  }

  const downloadVoicenote = async (filename) => {
    try {
      const response = await fetch(`http://localhost:8000/download-voicenote/${filename}`)
      if (!response.ok) throw new Error('Download failed')
      
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError('Failed to download voicenote: ' + err.message)
    }
  }

  const resetForm = () => {
    setFormData({ videoUrl: '', topic: '', prospectName: '' })
    setResult(null)
    setError(null)
    setCurrentStage('')
  }

  return (
    <div className="voicenote-generator">
      <div className="generator-header">
        <div className="header-icon">
          <HiMicrophone />
        </div>
        <h2>Generate Voicenote</h2>
        <p>Transform any video into a personalized podcast outreach</p>
      </div>

      <div className="generator-form">
        <div className="form-group">
          <label htmlFor="videoUrl">Video URL *</label>
          <input
            type="url"
            id="videoUrl"
            name="videoUrl"
            value={formData.videoUrl}
            onChange={handleInputChange}
            placeholder="https://youtube.com/watch?v=..."
            disabled={isProcessing}
            required
          />
          <small>YouTube, podcast, or any video URL</small>
        </div>

        <div className="form-group">
          <label htmlFor="topic">Topic to Search For *</label>
          <input
            type="text"
            id="topic"
            name="topic"
            value={formData.topic}
            onChange={handleInputChange}
            placeholder="e.g. AI thoughts, productivity tips, startup advice"
            disabled={isProcessing}
            required
          />
          <small>What specific topic should we find in the video?</small>
        </div>

        <div className="form-group">
          <label htmlFor="prospectName">Prospect Name (Optional)</label>
          <input
            type="text"
            id="prospectName"
            name="prospectName"
            value={formData.prospectName}
            onChange={handleInputChange}
            placeholder="e.g. John, Sarah"
            disabled={isProcessing}
          />
          <small>For personalization - leave empty for generic</small>
        </div>

        <div className="form-actions">
          <button 
            onClick={generateVoicenote}
            disabled={isProcessing || !formData.videoUrl || !formData.topic}
            className="generate-button"
          >
            {isProcessing ? (
              <>
                <HiArrowPath className="button-icon spinning" />
                Processing...
              </>
            ) : (
              <>
                <HiPlay className="button-icon" />
                Generate Voicenote
              </>
            )}
          </button>
          
          {(result || error) && (
            <button onClick={resetForm} className="reset-button">
              <HiArrowPath className="button-icon" />
              Start New
            </button>
          )}
        </div>
      </div>

      {/* Processing Status */}
      {isProcessing && (
        <div className="processing-status">
          <div className="loading-spinner"></div>
          <p>{currentStage}</p>
          <small>This may take 30-60 seconds...</small>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="error-result">
          <div className="error-header">
            <HiExclamationTriangle className="error-icon" />
            <h3>Error</h3>
          </div>
          <p>{error}</p>
        </div>
      )}

      {/* Success Result */}
      {result && result.success && (
        <div className="success-result">
          <h3>🎉 Voicenote Generated Successfully!</h3>
          
          <div className="result-details">
            <div className="result-row">
              <span>Topic:</span>
              <span>{result.topic}</span>
            </div>
            <div className="result-row">
              <span>Prospect:</span>
              <span>{result.prospect_name}</span>
            </div>
            <div className="result-row">
              <span>Script:</span>
              <span className="script-text">"{result.generated_script}"</span>
            </div>
            <div className="result-row">
              <span>Moments Found:</span>
              <span>{result.moments_found}</span>
            </div>
            <div className="result-row">
              <span>Processing Time:</span>
              <span>{result.stage_times?.total}</span>
            </div>
          </div>

          {result.voicenote ? (
            <div className="download-section">
              <button 
                onClick={() => downloadVoicenote(result.voicenote.filename)}
                className="download-button"
              >
                <HiCloudArrowDown className="button-icon" />
                Download MP3 ({result.voicenote.filename})
              </button>
            </div>
          ) : (
            <div className="no-audio-notice">
              <HiExclamationTriangle className="warning-icon" />
              <p>Audio generation not available (ElevenLabs not configured)</p>
              <p>Script generated successfully - you can copy it above!</p>
            </div>
          )}

          {result.stage_times && (
            <div className="timing-breakdown">
              <h4>⏱️ Processing Breakdown:</h4>
              <ul>
                <li>Stage 1 (Moments): {result.stage_times.stage1_moments}</li>
                <li>Stage 2 (Analysis): {result.stage_times.stage2_ask}</li>
                <li>Stage 3 (Script): {result.stage_times.stage3_chatgpt}</li>
                <li>Stage 4 (Audio): {result.stage_times.stage4_elevenlabs}</li>
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default VoicenoteGenerator 