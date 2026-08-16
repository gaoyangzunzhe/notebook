import { useCallback, useState } from 'react'
import { documentsApi } from '@/api/endpoints'
import type { DocumentRecord } from '@/api/types'

export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [dbAvailable, setDbAvailable] = useState(true)

  const refresh = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await documentsApi.list()
      setDocuments(res.data.documents)
      setDbAvailable(res.data.db_available)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }, [])

  const deleteOne = useCallback(async (docId: string) => {
    await documentsApi.del(docId)
    setDocuments((prev) => prev.filter((d) => d.doc_id !== docId))
  }, [])

  return { documents, loading, error, dbAvailable, refresh, deleteOne }
}
