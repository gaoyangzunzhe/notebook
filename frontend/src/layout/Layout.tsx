import { Outlet } from 'react-router'
import Sidebar from './Sidebar'
import LoginModal from '@/components/LoginModal'

export default function Layout() {
  return (
    <div className="flex h-screen overflow-hidden bg-bg text-ink">
      <Sidebar />
      <main className="flex-1 min-w-0 overflow-auto">
        <Outlet />
      </main>
      <LoginModal />
    </div>
  )
}
