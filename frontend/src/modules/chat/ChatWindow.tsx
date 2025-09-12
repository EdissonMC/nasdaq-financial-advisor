import { useRef, useEffect } from 'react'
import { MessageBubble } from './MessageBubble'
import { InputBar } from './InputBar'

export type ChatMessage = {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  citations?: Array<{ text_snippet?: string; source_url?: string; relevance_score?: number }>
}

type Props = {
  messages: ChatMessage[]
  loading?: boolean
  onSend: (text: string) => void
}

export function ChatWindow({ messages, loading, onSend }: Props) {
  const listRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div style={{ display: 'grid', gridTemplateRows: '1fr auto', height: '100%', background: 'var(--panel)', border: '1px solid var(--border)', borderRadius: 12, minHeight: 0 }}>
      <div ref={listRef} style={{ overflowY: 'auto', padding: 16 }} aria-live="polite" aria-busy={!!loading}>
        {messages.map(m => (
          <MessageBubble key={m.id} role={m.role} text={m.content} citations={m.citations} />
        ))}
        {loading && (
          <div className="skeleton" style={{ height: 60, margin: '8px 0' }} />
        )}
      </div>
      <div style={{ borderTop: '1px solid var(--border)' }}>
        <InputBar disabled={!!loading} onSend={onSend} />
      </div>
    </div>
  )
}


