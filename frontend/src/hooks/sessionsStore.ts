// 会话列表共享模块 store：侧边栏与对话页同源，避免各自重复拉取。
// 会话只在服务端有记录（首条消息发出后）才出现在列表，本地不保留「临时会话」伪条目。

import { useSyncExternalStore } from 'react'
import { chatApi } from '@/api/endpoints'
import type { ChatMessage, SessionSummary } from '@/api/types'

interface SessionsState {
  sessions: SessionSummary[]
  loading: boolean
  dbAvailable: boolean
}

let state: SessionsState = { sessions: [], loading: false, dbAvailable: true }

const listeners = new Set<() => void>()

function emit() {
  for (const l of listeners) l()
}

function setState(next: SessionsState) {
  state = next
  emit()
}

// 当前会话的消息缓存（切走再切回不丢；sources 挂在消息上）
const messageCache = new Map<string, ChatMessage[]>()

export function cacheMessages(sessionId: string, messages: ChatMessage[]): void {
  messageCache.set(sessionId, messages)
}

export function getCachedMessages(sessionId: string): ChatMessage[] | undefined {
  return messageCache.get(sessionId)
}

let fetching = false

/** 拉取会话列表，返回最新列表；失败静默保留旧数据 */
export async function refreshSessions(): Promise<SessionSummary[]> {
  if (fetching) return state.sessions
  fetching = true
  setState({ ...state, loading: true })
  try {
    const res = await chatApi.listSessions()
    setState({ sessions: res.data.sessions, loading: false, dbAvailable: res.data.db_available })
  } catch {
    setState({ ...state, loading: false })
  } finally {
    fetching = false
  }
  return state.sessions
}

export function getSnapshot(): SessionsState {
  return state
}

export function subscribe(cb: () => void): () => void {
  listeners.add(cb)
  return () => listeners.delete(cb)
}

/** 供组件订阅：返回会话状态 + 刷新操作 */
export function useSessions() {
  const snapshot = useSyncExternalStore(subscribe, getSnapshot)
  return {
    ...snapshot,
    refresh: refreshSessions,
  }
}
