import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { initAnalytics } from './utils/analytics'
import ErrorBoundary from './ErrorBoundary.tsx'

// Initialize analytics
initAnalytics()

console.log('main.tsx loaded');

// Initialize analytics (wrapped in try-catch to prevent errors from breaking the app)
try {
  console.log('Initializing analytics...');
  initAnalytics()
  console.log('Analytics initialized');
} catch (error) {
  console.warn('Analytics initialization failed:', error)
}

const rootElement = document.getElementById('root')
console.log('Root element:', rootElement);
if (!rootElement) {
  throw new Error('Root element not found')
}

console.log('Rendering app...');
createRoot(rootElement).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
console.log('App rendered');
