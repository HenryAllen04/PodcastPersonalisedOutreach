import { useState } from 'react'
import { HiMicrophone, HiPlay, HiCog } from 'react-icons/hi2'
import './App.css'
import VoicenoteGenerator from './components/VoicenoteGenerator'

function App() {
  const [isConnected, setIsConnected] = useState(false)
  const [activeTab, setActiveTab] = useState('generator')

  const checkBackendConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/docs')
      setIsConnected(response.ok)
    } catch (error) {
      setIsConnected(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo-container">
          <HiMicrophone className="logo-icon" />
          <h1>PODVOX</h1>
        </div>
        <p>Personalised Podcast Outreach</p>
      </header>
      
      <nav className="app-nav">
        <button 
          className={`nav-button ${activeTab === 'generator' ? 'active' : ''}`}
          onClick={() => setActiveTab('generator')}
        >
          <HiPlay className="nav-icon" />
          Generate Voicenote
        </button>
        <button 
          className={`nav-button ${activeTab === 'status' ? 'active' : ''}`}
          onClick={() => setActiveTab('status')}
        >
          <HiCog className="nav-icon" />
          System Status
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'generator' && (
          <VoicenoteGenerator />
        )}

        {activeTab === 'status' && (
          <div className="status-content">
            <div className="status-card">
              <h2>System Status</h2>
              <button 
                onClick={checkBackendConnection}
                className="status-button"
              >
                Check Backend Connection
              </button>
              <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
                Backend: {isConnected ? '✅ Connected' : '❌ Disconnected'}
              </div>
            </div>

            <div className="welcome-card">
              <h2>Welcome to PODVOX</h2>
              <p>Your personalised podcast outreach platform is ready!</p>
              <ul>
                <li>✅ React Frontend - Running on port 3000</li>
                <li>✅ FastAPI Backend - Running on port 8000</li>
                <li>✅ Docker Containerization - Ready for deployment</li>
              </ul>
              
              <div className="quick-start">
                <h3>Quick Start:</h3>
                <ol>
                  <li>Go to "Generate Voicenote" tab</li>
                  <li>Paste a YouTube or podcast video URL</li>
                  <li>Enter a topic to search for</li>
                  <li>Click "Generate Voicenote"</li>
                  <li>Download your personalized MP3!</li>
                </ol>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
