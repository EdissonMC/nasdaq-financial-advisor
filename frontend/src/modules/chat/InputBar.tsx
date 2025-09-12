import { useState } from 'react'

type Props = {
  disabled?: boolean
  onSend: (text: string) => void
}

export function InputBar({ disabled, onSend }: Props) {
  const [text, setText] = useState('')
  const [rows, setRows] = useState(1)

  const send = () => {
    const t = text.trim()
    if (!t || disabled) return
    onSend(t)
    setText('')
    setRows(1)
  }

  const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  const onChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value)
    const lineBreaks = (e.target.value.match(/\n/g) || []).length + 1
    setRows(Math.min(8, Math.max(1, lineBreaks)))
  }

  return (
    <div style={{ display: 'flex', gap: 8, padding: 12 }}>
      <textarea
        value={text}
        onChange={onChange}
        onKeyDown={onKeyDown}
        placeholder="Escribe tu pregunta..."
        disabled={disabled}
        rows={rows}
        style={{
          flex: 1,
          padding: '12px 14px',
          background: '#0f1424',
          color: 'var(--text)',
          border: '1px solid var(--border)',
          borderRadius: 10,
          resize: 'none',
          lineHeight: 1.4
        }}
      />
      <button
        onClick={send}
        disabled={disabled}
        style={{
          padding: '12px 16px',
          background: 'var(--accent)',
          color: '#0b1020',
          border: '1px solid var(--border)',
          borderRadius: 10,
          cursor: 'pointer'
        }}
      >
        Enviar
      </button>
    </div>
  )
}


