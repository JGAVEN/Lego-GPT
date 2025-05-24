import { StrictMode, useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import Settings from './Settings.tsx'
import { flushQueue } from './lib/queue'

function Root() {
  const [hash, setHash] = useState(window.location.hash)
  useEffect(() => {
    const handle = () => setHash(window.location.hash)
    window.addEventListener('hashchange', handle)
    return () => window.removeEventListener('hashchange', handle)
  }, [])
  return hash === '#settings' ? <Settings /> : <App />
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Root />
  </StrictMode>,
)

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {
      console.warn('service worker registration failed')
    })
  })
}

flushQueue().catch(() => {})
window.addEventListener('online', () => {
  flushQueue().catch(() => {})
})
