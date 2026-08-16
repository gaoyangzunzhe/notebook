import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { PreferencesProvider } from '@/context/PreferencesContext'
import { AuthProvider } from '@/context/AuthContext'
import './index.css'

ReactDOM.createRoot(document.getElementById('app')!).render(
  <React.StrictMode>
    {/* AuthProvider 在外层：PreferencesProvider 需要 useAuth 做登录后偏好同步 */}
    <AuthProvider>
      <PreferencesProvider>
        <App />
      </PreferencesProvider>
    </AuthProvider>
  </React.StrictMode>,
)
