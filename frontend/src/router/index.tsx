import { createBrowserRouter, Navigate } from 'react-router'
import Layout from '@/layout/Layout'
import NotesPage from '@/pages/NotesPage'
import KnowledgeBasePage from '@/pages/KnowledgeBasePage'
import ChatPage from '@/pages/ChatPage'
import SettingsPage from '@/pages/SettingsPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Navigate to="/notes" replace /> },
      { path: 'notes', element: <NotesPage /> },
      { path: 'kb', element: <KnowledgeBasePage /> },
      { path: 'chat', element: <ChatPage /> },
      { path: 'chat/:sessionId', element: <ChatPage /> },
      { path: 'settings', element: <SettingsPage /> },
    ],
  },
])
