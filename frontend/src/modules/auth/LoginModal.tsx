import { useState } from 'react'

type Props = {
  isOpen: boolean
  onClose: () => void
  onSubmit: (email: string, password: string) => Promise<void>
}

export function LoginModal({ isOpen, onClose, onSubmit }: Props) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  if (!isOpen) return null

  const handleSubmit = async () => {
    setError(null)
    setLoading(true)
    try {
      await onSubmit(email.trim(), password)
      onClose()
    } catch (e) {
      setError('Error de autenticación. Verifica tus credenciales.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      <div style={{ background: 'var(--panel)', border: '1px solid var(--border)', borderRadius: 12, padding: 24, width: '90%', maxWidth: 420 }}>
        <h2 style={{ margin: '0 0 16px 0' }}>Iniciar sesión</h2>
        <div style={{ display: 'grid', gap: 12 }}>
          <div>
            <label style={{ display: 'block', marginBottom: 6 }}>Email</label>
            <input value={email} onChange={e => setEmail(e.target.value)} type="email" placeholder="tu@email.com" style={{ width: '100%', padding: '12px 14px', background: '#0f1424', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: 8 }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: 6 }}>Contraseña</label>
            <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="•••••••" style={{ width: '100%', padding: '12px 14px', background: '#0f1424', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: 8 }} />
          </div>
          {error && <div style={{ color: '#ff4757', fontSize: 13 }}>{error}</div>}
          <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
            <button onClick={onClose} style={{ padding: '10px 14px', border: '1px solid var(--border)', borderRadius: 8, background: 'transparent', color: 'var(--muted)' }}>Cancelar</button>
            <button onClick={handleSubmit} disabled={loading} style={{ padding: '10px 16px', border: '1px solid var(--border)', borderRadius: 8, background: 'var(--accent)', color: '#0b1020', fontWeight: 500 }}>{loading ? 'Ingresando...' : 'Entrar'}</button>
          </div>
        </div>
      </div>
    </div>
  )
}


