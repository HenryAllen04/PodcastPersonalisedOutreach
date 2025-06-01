import { useState } from 'react'
import './App.css'

function App() {
  const [isConnected, setIsConnected] = useState(false)

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
        <h1>🎙️ PODVOX</h1>
        <p>Personalised Podcast Outreach</p>
      </header>
      
      <main className="app-main">
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
        </div>
      </main>
    </div>
  )
}

export default App
