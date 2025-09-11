import type { Conversation } from './types'

type Props = {
  conversations: Conversation[]
  activeId: string
  onSelect: (id: string) => void
  onCreate: () => void
  onRename: (id: string, title: string) => void
  onDelete: (id: string) => void
  hidden?: boolean
  onClose?: () => void
}

export function Sidebar({ conversations, activeId, onSelect, onCreate, onRename, onDelete, hidden, onClose }: Props) {
  return (
    <aside style={{
      width: 320,
      background: 'var(--panel)',
      border: '1px solid var(--border)',
      borderRadius: 12,
      padding: 16,
      height: '100%',
      display: hidden ? 'none' : 'grid',
      gridTemplateRows: 'auto 1fr auto',
      gap: 8,
      position: 'relative',
      minHeight: 0
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <strong>Historial</strong>
        <div style={{ display: 'flex', gap: 8 }}>
          <button 
            onClick={onCreate} 
            style={{ 
              padding: '12px 16px', 
              background: 'var(--accent)', 
              color: '#0b1020', 
              border: '1px solid var(--border)', 
              borderRadius: 10, 
              cursor: 'pointer',
              fontWeight: '500'
            }}
          >
            Nuevo
          </button>
          {onClose && (
            <button
              onClick={onClose}
              title="Cerrar"
              style={{ padding: '8px 10px', background: 'transparent', color: 'var(--muted)', border: '1px solid var(--border)', borderRadius: 8, cursor: 'pointer' }}
            >
              ✕
            </button>
          )}
        </div>
      </div>
      <div style={{ overflowY: 'auto' }}>
        {conversations.length === 0 && (
          <div style={{ color: 'var(--muted)', fontSize: 13 }}>
            Sin conversaciones. Crea una nueva para empezar.
          </div>
        )}
        {conversations.map(c => (
          <div key={c.id} style={{
            border: '1px solid var(--border)',
            borderRadius: 10,
            padding: 12,
            marginBottom: 8,
            background: c.id === activeId ? '#0f1424' : 'transparent'
          }}>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <button 
                onClick={() => onSelect(c.id)} 
                style={{ 
                  flex: 1, 
                  textAlign: 'left', 
                  background: 'transparent', 
                  color: 'var(--text)', 
                  border: 'none', 
                  cursor: 'pointer',
                  padding: '8px 0'
                }}
              >
                {c.title}
              </button>
              <button 
                onClick={() => {
                  const t = prompt('Nuevo nombre', c.title)
                  if (t && t.trim()) onRename(c.id, t.trim())
                }} 
                title="Renombrar" 
                style={{ 
                  padding: '8px 12px', 
                  background: 'var(--primary)', 
                  color: '#0b1020', 
                  border: '1px solid var(--border)', 
                  borderRadius: 8, 
                  cursor: 'pointer',
                  fontWeight: '500'
                }}
              >
                ✎
              </button>
              <button 
                onClick={() => { if (confirm('¿Eliminar conversación?')) onDelete(c.id) }} 
                title="Eliminar" 
                style={{ 
                  padding: '8px 12px', 
                  background: '#ff4757', 
                  color: '#fff', 
                  border: '1px solid var(--border)', 
                  borderRadius: 8, 
                  cursor: 'pointer',
                  fontWeight: '500'
                }}
              >
                🗑
              </button>
            </div>
            <div style={{ color: 'var(--muted)', fontSize: 12, marginTop: 6 }}>{new Date(c.updatedAt).toLocaleString()}</div>
          </div>
        ))}
      </div>
      <div style={{ fontSize: 12, color: 'var(--muted)' }}>Guardado localmente</div>
    </aside>
  )
}


