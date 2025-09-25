import { useRef, useEffect,useState } from 'react'
import { MessageBubble } from './MessageBubble'
import { InputBar } from './InputBar'
import { FeedbackModal } from './FeedbackModal'
import { submitFeedback } from '../../services/api'
export type ChatMessage = {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  citations?: Array<{ text_snippet?: string; source_url?: string; relevance_score?: number }>
  metadata?: {  // ✅ AÑADIR metadata opcional
    request_feedback?: boolean
  }
}

type Props = {
  messages: ChatMessage[]
  loading?: boolean
  onSend: (text: string) => void
}

export function ChatWindow({ messages, loading, onSend }: Props) {
  const listRef = useRef<HTMLDivElement>(null)
  const [showFeedbackModal, setShowFeedbackModal] = useState(false)

  // ✅ Estado para activar/desactivar feedback con mejor nombre
  const [autoFeedbackEnabled, setAutoFeedbackEnabled] = useState(() => {
    const saved = localStorage.getItem('autoFeedbackEnabled')
    return saved !== null ? JSON.parse(saved) : true
  })

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, loading])

  useEffect(() => {
    localStorage.setItem('autoFeedbackEnabled', JSON.stringify(autoFeedbackEnabled))
  }, [autoFeedbackEnabled])

  useEffect(() => {
    if (!autoFeedbackEnabled) return
    
    const lastMessage = messages[messages.length - 1];
    if (lastMessage?.role === 'assistant' && lastMessage.metadata?.request_feedback) {
      console.log('😔 Negative sentiment detected, showing feedback modal');
      setShowFeedbackModal(true);
    }
  }, [messages, autoFeedbackEnabled]);

  // ✅ MANEJAR envío de feedback
  const handleFeedbackSubmit = async (feedbackData: { feedback_text: string; rating: number }) => {
    try {
      const response = await submitFeedback(feedbackData);
      console.log('✅ Feedback sent successfully:', response);
      alert('¡Gracias por tu feedback! 🙏 Trabajaremos para mejorar tu experiencia.');
    } catch (error) {
      console.error('❌ Error sending feedback:', error);
      throw error;
    }
  };


  return (
    <>
      <div style={{ 
        display: 'grid', 
        gridTemplateRows: 'auto 1fr auto', 
        height: '100%', 
        background: 'var(--panel)', 
        border: '1px solid var(--border)', 
        borderRadius: 12, 
        minHeight: 0 }}
      >
        
        {/* ✅ HEADER MEJORADO CON FEEDBACK TOGGLE */}
        <div style={{
          padding: '12px 16px',
          borderBottom: '1px solid var(--border)',
          background: 'var(--background)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ 
              fontSize: '14px', 
              fontWeight: '600',
              color: 'var(--text)'
            }}>
              💬 Chat Assistant
            </span>
          </div>
          
          {/* ✅ TOGGLE MEJORADO */}
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px',
            background: 'var(--panel)',
            padding: '6px 10px',
            borderRadius: '6px',
            border: '1px solid var(--border)'
          }}>
            <span style={{ 
              fontSize: '12px', 
              color: 'var(--muted)',
              fontWeight: '500'
            }}>
              🤔 Smart Feedback
            </span>

          <label style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '6px', 
            cursor: 'pointer',
            fontSize: '12px',
            color: autoFeedbackEnabled ? 'var(--accent)' : 'var(--muted)',
            fontWeight: '500'
          }}>
            <input
              type="checkbox"
              checked={autoFeedbackEnabled}
              onChange={(e) => setAutoFeedbackEnabled(e.target.checked)}
              style={{
                width: '14px',
                height: '14px',
                accentColor: 'var(--accent)',
                cursor: 'pointer',
                margin: 0
              }}
            />
            {autoFeedbackEnabled ? 'ON' : 'OFF'}
          </label>      
        </div>
      </div>
        
        <div ref={listRef} style={{ 
            flex: 1,
            overflowY: 'auto',
            padding: 16,
            display: 'flex',
            flexDirection: 'column',
            gap: 12
          }} 
          aria-live="polite"
          aria-busy={!!loading}>
          {messages.map(m => (
            <MessageBubble key={m.id} role={m.role} text={m.content} citations={m.citations} />
          ))}
          {loading && (
            <div style={{ 
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '12px 16px',
              color: 'var(--muted)',
              fontStyle: 'italic'
            }}>
            <div style={{
                width: '16px',
                height: '16px',
                border: '2px solid var(--border)',
                borderTop: '2px solid var(--accent)',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite'
              }}></div>
              Wally está pensando...
            </div>
          )}
        </div>
      
        <div style={{ borderTop: '1px solid var(--border)' }}>
          <InputBar disabled={!!loading} onSend={onSend} />
        </div>
      </div>  
        {/* ✅ MODAL DE FEEDBACK */}
        <FeedbackModal
          isOpen={showFeedbackModal}
          onClose={() => setShowFeedbackModal(false)}
          onSubmit={handleFeedbackSubmit}
        />
        {/* ✅ CSS PARA ANIMACIÓN DE LOADING */}
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
    </>
  )
}


