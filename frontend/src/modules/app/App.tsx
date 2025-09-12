import { useEffect, useMemo, useState } from 'react'
import { ChatWindow, type ChatMessage } from '../chat/ChatWindow'
import { Sidebar } from '../conversations/Sidebar'
import { ConfigModal } from '../config/ConfigModal'
import { LoginModal } from '../auth/LoginModal'
import { RegisterModal } from '../auth/RegisterModal'
import type { Conversation } from '../conversations/types'
import type { ApiConfig } from '../config/types'
import { loadConversations, saveConversations } from '../conversations/storage'
import { loadConfig, saveConfig } from '../config/storage'
import { askQuestion, setApiConfig, getHistory } from '../../services/api'

export function App() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [activeId, setActiveId] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [apiConfig, setApiConfigState] = useState<ApiConfig>({ chatApiUrl: 'http://localhost:8000' })
  const [isConfigOpen, setIsConfigOpen] = useState(false)
  const [isLoginOpen, setIsLoginOpen] = useState(false)
  const [isRegisterOpen, setIsRegisterOpen] = useState(false)

  useEffect(() => {
    // Cargar configuración del API
    const config = loadConfig()
    setApiConfigState(config)
    setApiConfig(config)

    // Cargar conversaciones
    const stored = loadConversations()
    if (stored.length > 0) {
      setConversations(stored)
      setActiveId(stored[0].id)
    } else {
      const first: Conversation = {
        id: crypto.randomUUID(),
        title: 'Nueva conversación',
        messages: [{ id: 'welcome', role: 'assistant', content: 'Hola, ¿en qué empresa NASDAQ te gustaría enfocarte?' }],
        createdAt: Date.now(),
        updatedAt: Date.now()
      }
      setConversations([first])
      setActiveId(first.id)
    }
  }, [])

  useEffect(() => {
    if (conversations.length) saveConversations(conversations)
  }, [conversations])

  const activeConv = useMemo(() => conversations.find(c => c.id === activeId), [conversations, activeId])

  const createConversation = () => {
    const conv: Conversation = {
      id: crypto.randomUUID(),
      title: 'Nueva conversación',
      messages: [{ id: crypto.randomUUID(), role: 'assistant', content: 'Nueva sesión lista. Pregúntame sobre una empresa.' }],
      createdAt: Date.now(),
      updatedAt: Date.now()
    }
    setConversations(prev => [conv, ...prev])
    setActiveId(conv.id)
  }

  const renameConversation = (id: string, title: string) => {
    setConversations(prev => prev.map(c => c.id === id ? { ...c, title, updatedAt: Date.now() } : c))
  }

  const deleteConversation = (id: string) => {
    setConversations(prev => prev.filter(c => c.id !== id))
    if (activeId === id) {
      const next = conversations.find(c => c.id !== id)
      if (next) setActiveId(next.id)
      else createConversation()
    }
  }

  const handleConfigSave = (config: ApiConfig) => {
    setApiConfigState(config)
    setApiConfig(config)
    saveConfig(config)
  }

  const handleLogout = () => {
    const next: ApiConfig = { ...apiConfig, authToken: undefined }
    handleConfigSave(next)
  }

  const handleSend = async (text: string) => {
    if (!activeConv) return
    const newUser: ChatMessage = { id: crypto.randomUUID(), role: 'user', content: text }
    const cid = activeConv.id
    setConversations(prev => prev.map(c => c.id === cid ? { ...c, messages: [...c.messages, newUser], updatedAt: Date.now() } : c))
    setLoading(true)
    try {
      const data = await askQuestion(text, cid)
      const bot: ChatMessage = { id: crypto.randomUUID(), role: 'assistant', content: data.answer ?? 'Sin respuesta disponible.', citations: data.citations }
      setConversations(prev => prev.map(c => c.id === cid ? { ...c, messages: [...c.messages, bot], updatedAt: Date.now() } : c))
      if (activeConv.title === 'Nueva conversación') {
        const inferred = text.slice(0, 40).trim() || 'Conversación'
        renameConversation(cid, inferred)
      }
    } catch {
      const err: ChatMessage = { id: crypto.randomUUID(), role: 'assistant', content: 'Error al obtener respuesta. Intenta nuevamente.' }
      setConversations(prev => prev.map(c => c.id === cid ? { ...c, messages: [...c.messages, err], updatedAt: Date.now() } : c))
    } finally {
      setLoading(false)
    }
  }

  // Ejemplo de función para cargar historial cuando el backend esté listo
  const loadHistoryFromApi = async (cid: string) => {
    try {
      const data = await getHistory(cid)
      const msgs: ChatMessage[] = data.messages.map(m => ({ id: m.id, role: m.role, content: m.content }))
      setConversations(prev => prev.map(c => c.id === cid ? { ...c, messages: msgs, updatedAt: Date.now() } : c))
    } catch {
      // Ignorar si no está disponible; seguimos con localStorage
    }
  }

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header a ancho completo */}
      <div style={{ width: '100%', padding: '12px 24px', borderBottom: '1px solid var(--border)', marginBottom: 12 }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', alignItems: 'center', gap: 16 }}>
          <div style={{ display: 'grid', gap: 4, justifyItems: 'start' }}>
            <h1 style={{ margin: 0 }}>Asesor Financiero</h1>
            <span style={{ color: 'var(--muted)', fontSize: 14 }}>Haz preguntas sobre temas financieros</span>
            {apiConfig.authToken && apiConfig.authToken.includes('mock-token') && (
              <span style={{ fontSize: 12, color: '#0b1020', background: '#facc15', padding: '4px 8px', borderRadius: 6 }}>
                Aviso: usando token simulado (solo DEMO)
              </span>
            )}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 8 }}>
            {apiConfig.authToken ? (
              <button
                onClick={handleLogout}
                style={{ height: 36, padding: '0 12px', background: '#ff4757', color: '#fff', border: '1px solid var(--border)', borderRadius: 8, cursor: 'pointer', fontWeight: 500, fontSize: 14 }}
              >
                Cerrar sesión
              </button>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <button
                  onClick={() => setIsLoginOpen(true)}
                  style={{ height: 36, padding: '0 12px', background: 'var(--accent)', color: '#0b1020', border: '1px solid var(--border)', borderRadius: 8, cursor: 'pointer', fontWeight: 500, fontSize: 14 }}
                >
                  Iniciar sesión
                </button>
                <button
                  onClick={() => setIsRegisterOpen(true)}
                  style={{ height: 36, padding: '0 12px', background: '#8b5cf6', color: '#0b1020', border: '1px solid var(--border)', borderRadius: 8, cursor: 'pointer', fontWeight: 500, fontSize: 14 }}
                >
                  Registrarse
                </button>
              </div>
            )}
            <button
              onClick={() => setIsConfigOpen(true)}
              style={{
                height: 36,
                padding: '0 12px',
                background: 'var(--primary)',
                color: '#0b1020',
                border: '1px solid var(--border)',
                borderRadius: 8,
                cursor: 'pointer',
                fontWeight: 500,
                fontSize: 14
              }}
              title={`API: ${apiConfig.chatApiUrl}`}
            >
              ⚙️ Config
            </button>
          </div>
        </div>
      </div>

      <div className="container" style={{ width: '100%', flex: 1, minHeight: 0 }}>
        {!apiConfig.authToken ? (
          <div style={{
            height: '100%',
            border: '1px solid var(--border)',
            borderRadius: 12,
            background: 'var(--panel)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            padding: 24
          }}>
            <div>
              <h2 style={{ marginTop: 0 }}>Necesitas iniciar sesión</h2>
              <p className="muted" style={{ marginBottom: 16 }}>Inicia sesión para comenzar a chatear.</p>
              <div style={{ display: 'flex', gap: 8, justifyContent: 'center' }}>
                <button onClick={() => setIsLoginOpen(true)} style={{ padding: '10px 16px', background: 'var(--accent)', color: '#0b1020', border: '1px solid var(--border)', borderRadius: 8, cursor: 'pointer', fontWeight: 500 }}>Iniciar sesión</button>
                <button onClick={() => setIsConfigOpen(true)} style={{ padding: '10px 16px', background: 'var(--primary)', color: '#0b1020', border: '1px solid var(--border)', borderRadius: 8, cursor: 'pointer', fontWeight: 500 }}>Configurar API</button>
              </div>
            </div>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: 20, height: '100%', minHeight: 0 }}>
            <Sidebar
              conversations={conversations}
              activeId={activeId}
              onSelect={setActiveId}
              onCreate={createConversation}
              onRename={renameConversation}
              onDelete={deleteConversation}
            />
            <div style={{ height: '100%', minHeight: 0 }}>
              <ChatWindow messages={activeConv?.messages ?? []} loading={loading} onSend={handleSend} />
            </div>
          </div>
        )}
      </div>

      <div className="container">
        <footer style={{ marginTop: 8, color: 'var(--muted)', fontSize: 12 }}>
          <span>Proyecto AnyoneAI - 2025</span>
        </footer>
      </div>

      <ConfigModal
        isOpen={isConfigOpen}
        onClose={() => setIsConfigOpen(false)}
        onSave={handleConfigSave}
        currentConfig={apiConfig}
      />
      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onSubmit={async (email, password) => {
          // Nota: si el backend requiere un formato distinto, ajustar aquí
          // y guardar el token con el prefijo que corresponda (p. ej., "Bearer ...")
          const { login } = await import('../../services/api')
          const res = await login(email, password)
          const token = `${res.token_type ?? 'Bearer'} ${res.access_token}`.trim()
          handleConfigSave({ ...apiConfig, authToken: token })
        }}
      />
      <RegisterModal
        isOpen={isRegisterOpen}
        onClose={() => setIsRegisterOpen(false)}
        onSubmit={async (name, email, password) => {
          const { register } = await import('../../services/api')
          await register(name, email, password)
          // Después de registrarse, opcionalmente iniciar sesión automáticamente
          const { login } = await import('../../services/api')
          const res = await login(email, password)
          const token = `${res.token_type ?? 'Bearer'} ${res.access_token}`.trim()
          handleConfigSave({ ...apiConfig, authToken: token })
        }}
      />
    </div>
  )
}


