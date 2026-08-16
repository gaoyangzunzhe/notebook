// /notes/{id}/assist 的 SSE 消费 hook：fetch + ReadableStream（EventSource 无法带 Authorization 头）。
// 事件帧为单行 `data: {json}\n\n`，type ∈ token / done / error。
// 预检失败在流开始前返回普通 HTTP（404/400/422/503 + {detail}），需自行解析。

import { useCallback, useRef, useState } from 'react'
import { getAccessToken } from '@/api/client'
import type { AssistEvent, AssistRequest } from '@/api/types'

interface Handlers {
  onToken: (text: string) => void
  onDone: () => void
  onError: (message: string) => void
  /** 401（token 失效/未登录）时触发登录弹窗 */
  onUnauthorized?: () => void
}

interface UseAssistStreamResult {
  /** 发起一次辅助生成；generating 期间再次调用被忽略 */
  start: (noteId: number, body: AssistRequest, handlers: Handlers) => Promise<void>
  /** 主动停止（abort 掉 fetch，后端 CancelledError 静默清理） */
  stop: () => void
  generating: boolean
}

export function useAssistStream(): UseAssistStreamResult {
  const [generating, setGenerating] = useState(false)
  const ctrlRef = useRef<AbortController | null>(null)

  const start = useCallback(
    async (noteId: number, body: AssistRequest, handlers: Handlers) => {
      if (ctrlRef.current) return
      const ctrl = new AbortController()
      ctrlRef.current = ctrl
      setGenerating(true)
      try {
        const res = await fetch(`/api/v1/notes/${noteId}/assist`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${getAccessToken() ?? ''}`,
          },
          body: JSON.stringify(body),
          signal: ctrl.signal,
        })

        // 预检失败（流未开始）：解析 {detail}
        if (!res.ok) {
          let detail = `请求失败（${res.status}）`
          try {
            const j = (await res.json()) as { detail?: unknown }
            if (typeof j?.detail === 'string') detail = j.detail
          } catch {
            /* 无 JSON body */
          }
          if (res.status === 401) handlers.onUnauthorized?.()
          handlers.onError(detail)
          return
        }
        if (!res.body) {
          handlers.onError('浏览器不支持流式响应')
          return
        }

        const reader = res.body.getReader()
        const decoder = new TextDecoder('utf-8')
        let buffer = ''
        let finished = false

        for (;;) {
          const { done, value } = await reader.read()
          if (done) break
          buffer += decoder.decode(value, { stream: true })

          let idx: number
          while (!finished && (idx = buffer.indexOf('\n\n')) !== -1) {
            const frame = buffer.slice(0, idx)
            buffer = buffer.slice(idx + 2)
            const line = frame.split('\n').find((l) => l.startsWith('data: '))
            if (!line) continue
            try {
              const evt = JSON.parse(line.slice(6)) as AssistEvent
              if (evt.type === 'token') handlers.onToken(evt.content)
              else if (evt.type === 'done') {
                finished = true
                handlers.onDone()
              } else if (evt.type === 'error') {
                finished = true
                handlers.onError(evt.message)
              }
            } catch {
              /* 忽略无法解析的帧 */
            }
          }
        }
      } catch (e) {
        if ((e as Error).name !== 'AbortError') {
          handlers.onError((e as Error).message)
        }
        // AbortError：用户主动停止，不报错
      } finally {
        ctrlRef.current = null
        setGenerating(false)
      }
    },
    [],
  )

  const stop = useCallback(() => {
    ctrlRef.current?.abort()
  }, [])

  return { start, stop, generating }
}
