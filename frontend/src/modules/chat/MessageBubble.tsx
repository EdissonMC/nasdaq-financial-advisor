import { marked } from 'marked'
import DOMPurify from 'dompurify'

type Citation = {
  text_snippet?: string
  source_url?: string
  relevance_score?: number
}

type Props = {
  role: 'user' | 'assistant' | 'system'
  text: string
  citations?: Citation[]
}

export function MessageBubble({ role, text, citations }: Props) {
  const isUser = role === 'user'
  const html = !isUser ? DOMPurify.sanitize(marked.parse(text)) : undefined
  const copy = async () => {
    try { await navigator.clipboard.writeText(text) } catch {}
  }
  return (
    <div style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', margin: '8px 0' }}>
      <div
        style={{
          maxWidth: '78%',
          background: isUser ? 'var(--primary)' : '#0f1424',
          color: isUser ? '#0b1020' : 'var(--text)',
          border: '1px solid var(--border)',
          padding: isUser ? '10px 12px' : '10px 40px 10px 12px',
          borderRadius: isUser ? '14px 14px 4px 14px' : '14px 14px 14px 4px',
          whiteSpace: 'pre-wrap',
          position: 'relative'
        }}
      >
        {!isUser && html ? (
          <div dangerouslySetInnerHTML={{ __html: html }} />
        ) : (
          <>{text}</>
        )}
        {!isUser && (
          <button onClick={copy} title="Copiar" style={{ position: 'absolute', top: 8, right: 8, background: 'var(--panel)', color: 'var(--muted)', border: '1px solid var(--border)', borderRadius: 6, cursor: 'pointer', padding: '4px 8px', fontSize: 12, boxShadow: 'var(--shadow-sm)' }}>Copiar</button>
        )}
        {!isUser && citations && citations.length > 0 && (
          <div style={{ marginTop: 8, borderTop: '1px dashed var(--border)', paddingTop: 6, fontSize: 12 }}>
            <div style={{ color: 'var(--muted)', marginBottom: 4 }}>Fuentes:</div>
            <ul style={{ margin: 0, paddingLeft: 16 }}>
              {citations.slice(0, 3).map((c, idx) => (
                <li key={idx}>
                  {c.source_url ? (
                    <a href={c.source_url} target="_blank" rel="noreferrer">{c.source_url}</a>
                  ) : (
                    <span>{c.text_snippet || 'Fragmento'}</span>
                  )}
                  {typeof c.relevance_score === 'number' && (
                    <span style={{ color: 'var(--muted)' }}> · score {c.relevance_score.toFixed(2)}</span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}


