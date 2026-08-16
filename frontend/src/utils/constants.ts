// 与 backend/app/api/v1/documents.py 的 SUPPORTED_EXTENSIONS 保持一致
export const SUPPORTED_EXTENSIONS = ['.txt', '.md', '.markdown', '.pdf', '.docx', '.pptx']

export function isSupportedFile(name: string): boolean {
  const dot = name.lastIndexOf('.')
  if (dot < 0) return false
  return SUPPORTED_EXTENSIONS.includes(name.slice(dot).toLowerCase())
}
