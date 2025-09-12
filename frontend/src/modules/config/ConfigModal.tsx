import { useState, useEffect } from 'react'
import type { ApiConfig } from './types'

type Props = {
  isOpen: boolean
  onClose: () => void
  onSave: (config: ApiConfig) => void
  currentConfig: ApiConfig
}

export function ConfigModal({ isOpen, onClose, onSave, currentConfig }: Props) {
  const [config, setConfig] = useState<ApiConfig>(currentConfig)
  const [isValid, setIsValid] = useState(true)

  useEffect(() => {
    if (isOpen) {
      setConfig(currentConfig)
    }
  }, [isOpen, currentConfig])

  const validateUrl = (url: string) => {
    try {
      new URL(url)
      return true
    } catch {
      return false
    }
  }

  const handleSave = () => {
    if (validateUrl(config.chatApiUrl)) {
      onSave(config)
      onClose()
    } else {
      setIsValid(false)
    }
  }

  const handleUrlChange = (url: string) => {
    setConfig(prev => ({ ...prev, chatApiUrl: url }))
    setIsValid(validateUrl(url))
  }

  if (!isOpen) return null

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        background: 'var(--panel)',
        border: '1px solid var(--border)',
        borderRadius: 12,
        padding: 24,
        width: '90%',
        maxWidth: 500,
        maxHeight: '90vh',
        overflow: 'auto'
      }}>
        <h2 style={{ margin: '0 0 16px 0', color: 'var(--text)' }}>
          Configuración del API
        </h2>
        
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 8, color: 'var(--text)', fontWeight: '500' }}>
            URL del Chat API
          </label>
          <input
            type="url"
            value={config.chatApiUrl}
            onChange={(e) => handleUrlChange(e.target.value)}
            placeholder="http://localhost:8000"
            style={{
              width: '100%',
              padding: '12px 14px',
              background: '#0f1424',
              color: 'var(--text)',
              border: `1px solid ${isValid ? 'var(--border)' : '#ff4757'}`,
              borderRadius: 8,
              fontSize: 14
            }}
          />
          {!isValid && (
            <div style={{ color: '#ff4757', fontSize: 12, marginTop: 4 }}>
              URL no válida. Debe incluir http:// o https://
            </div>
          )}
        </div>

        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 8, color: 'var(--text)', fontWeight: '500' }}>
            Timeout (ms)
          </label>
          <input
            type="number"
            value={config.timeout || 30000}
            onChange={(e) => setConfig(prev => ({ ...prev, timeout: parseInt(e.target.value) || 30000 }))}
            min="1000"
            max="120000"
            style={{
              width: '100%',
              padding: '12px 14px',
              background: '#0f1424',
              color: 'var(--text)',
              border: '1px solid var(--border)',
              borderRadius: 8,
              fontSize: 14
            }}
          />
        </div>

        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 8, color: 'var(--text)', fontWeight: '500' }}>
            Top K (resultados)
          </label>
          <input
            type="number"
            value={config.topK || 8}
            onChange={(e) => setConfig(prev => ({ ...prev, topK: Math.max(1, Math.min(20, parseInt(e.target.value) || 8)) }))}
            min="1"
            max="20"
            style={{
              width: '100%',
              padding: '12px 14px',
              background: '#0f1424',
              color: 'var(--text)',
              border: '1px solid var(--border)',
              borderRadius: 8,
              fontSize: 14
            }}
          />
        </div>

        <div style={{ marginBottom: 24, display: 'flex', alignItems: 'center', gap: 8 }}>
          <input
            id="simulate"
            type="checkbox"
            checked={!!config.simulateIfOffline}
            onChange={(e) => setConfig(prev => ({ ...prev, simulateIfOffline: e.target.checked }))}
          />
          <label htmlFor="simulate" style={{ color: 'var(--text)' }}>
            Usar simulación local si no hay conexión
          </label>
        </div>

        <div style={{ marginBottom: 8 }}>
          <label style={{ display: 'block', marginBottom: 8, color: 'var(--text)', fontWeight: '500' }}>
            Auth Token (opcional)
          </label>
          <input
            type="text"
            value={config.authToken || ''}
            onChange={(e) => setConfig(prev => ({ ...prev, authToken: e.target.value }))}
            placeholder="Bearer eyJhbGci..."
            style={{
              width: '100%',
              padding: '12px 14px',
              background: '#0f1424',
              color: 'var(--text)',
              border: '1px solid var(--border)',
              borderRadius: 8,
              fontSize: 14
            }}
          />
        </div>

        <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
          <button
            onClick={onClose}
            style={{
              padding: '12px 20px',
              background: 'transparent',
              color: 'var(--muted)',
              border: '1px solid var(--border)',
              borderRadius: 8,
              cursor: 'pointer'
            }}
          >
            Cancelar
          </button>
          <button
            onClick={handleSave}
            disabled={!isValid}
            style={{
              padding: '12px 20px',
              background: isValid ? 'var(--accent)' : 'var(--muted)',
              color: isValid ? '#0b1020' : 'var(--text)',
              border: '1px solid var(--border)',
              borderRadius: 8,
              cursor: isValid ? 'pointer' : 'not-allowed',
              fontWeight: '500'
            }}
          >
            Guardar
          </button>
        </div>
      </div>
    </div>
  )
}
