import { useEffect, useState } from 'react'
import { healthApi } from '@/api/endpoints'
import type { HealthResponse } from '@/api/types'

/** 拉一次 /health（公开端点，无需鉴权）；后端未启动时保持 null */
export function useHealth(): HealthResponse | null {
  const [health, setHealth] = useState<HealthResponse | null>(null)

  useEffect(() => {
    let cancelled = false
    healthApi
      .get()
      .then((res) => {
        if (!cancelled) setHealth(res.data)
      })
      .catch(() => {
        /* 保持 null */
      })
    return () => {
      cancelled = true
    }
  }, [])

  return health
}
