// 将 Tiptap 文档位置映射为「后端 note.content(HTML) 中的偏移量」。
// 后端 continue 用 note.content[:cursor_position] 取光标前内容，因此需要 HTML 空间的精确偏移。

import { DOMSerializer, Fragment } from '@tiptap/pm/model'
import type { Editor } from '@tiptap/react'

/** 序列化一个 fragment 为 HTML 字符串 */
function fragmentToHtml(editor: Editor, fragment: Fragment): string {
  const node = DOMSerializer.fromSchema(editor.state.schema).serializeFragment(fragment)
  const div = document.createElement('div')
  div.appendChild(node)
  return div.innerHTML
}

/** 剥掉 HTML 尾部所有闭合标签（用于「光标恰在一个块/标记内部」的情形：该元素在光标处仍是打开的） */
function stripTrailingClosers(html: string): string {
  let s = html
  for (;;) {
    const m = /<\/[a-zA-Z][^>]*>$/.exec(s)
    if (!m) return s
    s = s.slice(0, m.index)
  }
}

/**
 * 计算「光标之前」内容的 HTML 前缀长度（与 editor.getHTML() 前缀精确对齐）。
 *
 * - 光标在文末/节点边界：doc.cut(0,pos) 即完整节点，序列化结果即为准确前缀。
 * - 光标在文本/标记中间：fragment 序列化会把打开的标签闭合（<p>…<strong>wor</strong></p>），
 *   而真实前缀只到光标（<p>…<strong>wor），故剥掉尾部闭合标签。
 */
export function htmlLengthBefore(editor: Editor, pos: number): number {
  const { doc } = editor.state
  const clamped = Math.max(0, Math.min(pos, doc.content.size))
  const $pos = doc.resolve(clamped)
  // 位置是否落在节点边界（nodeAfter 存在，或恰为父节点末尾）→ 不剥闭合标签
  const atBoundary = $pos.nodeAfter !== null || $pos.parentOffset === $pos.parent.content.size

  // doc.cut 运行时语义：恰为整段时返回 Node 自身，否则返回 Fragment（类型声明只标了 Node，故强转）
  const fragment: Fragment =
    clamped >= doc.content.size ? doc.content : (doc.cut(0, clamped) as unknown as Fragment)
  let html = fragmentToHtml(editor, fragment)
  if (!atBoundary) html = stripTrailingClosers(html)
  return html.length
}

/** 把笔记 HTML 剥成纯文本（列表卡片预览用） */
export function htmlToText(html: string): string {
  const div = document.createElement('div')
  div.innerHTML = html
  return (div.textContent ?? '').replace(/\s+/g, ' ').trim()
}
