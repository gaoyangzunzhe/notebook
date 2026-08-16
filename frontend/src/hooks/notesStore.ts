// 笔记列表共享模块 store：全部笔记（笔记已独立，不再归属笔记本）。
// 挂载时 refreshNotes() 拉全量；保存/删除后可 upsert/removeNote 局部同步。

import { useSyncExternalStore } from 'react'
import { notesApi } from '@/api/endpoints'
import type { NoteOut } from '@/api/types'

interface NotesState {
  notes: NoteOut[]
  loading: boolean
}

let state: NotesState = { notes: [], loading: false }

const listeners = new Set<() => void>()

function emit() {
  for (const l of listeners) l()
}

function setState(next: NotesState) {
  state = next
  emit()
}

/** 刷新序号：每次 refresh 自增；本地变更（增/删）也自增，使任何在途响应作废 */
let seq = 0

/** 拉取全部笔记；过期响应（seq 已被后发操作超越）直接丢弃 */
export async function refreshNotes(): Promise<NoteOut[]> {
  const mySeq = ++seq
  setState({ ...state, loading: true })
  try {
    const res = await notesApi.list()
    if (mySeq !== seq) return state.notes
    setState({ notes: res.data.notes, loading: false })
  } catch {
    if (mySeq !== seq) return state.notes
    setState({ ...state, loading: false })
  }
  return state.notes
}

/** 局部更新一条笔记（保存后回填列表卡片；也作废在途列表响应避免覆盖） */
export function upsertNote(note: NoteOut): void {
  seq++
  setState({
    ...state,
    notes: state.notes.some((n) => n.id === note.id)
      ? state.notes.map((n) => (n.id === note.id ? note : n))
      : [note, ...state.notes],
  })
}

export function removeNote(id: number): void {
  seq++
  setState({ ...state, notes: state.notes.filter((n) => n.id !== id) })
}

export function getSnapshot(): NotesState {
  return state
}

export function subscribe(cb: () => void): () => void {
  listeners.add(cb)
  return () => listeners.delete(cb)
}

export function useNotes() {
  const snapshot = useSyncExternalStore(subscribe, getSnapshot)
  return { ...snapshot, refresh: refreshNotes, upsertNote, removeNote }
}
