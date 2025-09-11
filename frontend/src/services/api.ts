import type { ApiConfig } from '../modules/config/types'

export type Citation = {
  document_id?: string
  company?: string
  document_type?: string
  filing_year?: number
  page_number?: number
  text_snippet?: string
  source_url?: string
  relevance_score?: number
}

export type AskResponse = {
  answer: string
  citations?: Citation[]
}

export type LoginResponse = {
  access_token: string
  token_type?: string
}

let currentConfig: ApiConfig | null = null

export function setApiConfig(config: ApiConfig) {
  currentConfig = config
}

export function getApiConfig(): ApiConfig {
  return (
    currentConfig || {
      chatApiUrl: import.meta.env.VITE_CHAT_API_URL || 'http://localhost:8000',
      timeout: 30000,
      topK: 8,
      simulateIfOffline: true
    }
  )
}

export async function askQuestion(query: string, sessionId?: string): Promise<AskResponse> {
  const config = getApiConfig()
  const payload: Record<string, unknown> = { query }
  if (sessionId) payload.session_id = sessionId
  if (config.topK) payload.top_k = config.topK

  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), config.timeout || 30000)

  try {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (config.authToken) headers['Authorization'] = config.authToken

    const res = await fetch(`${config.chatApiUrl}/chat`, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
      signal: controller.signal
    })
    
    clearTimeout(timeoutId)
    
    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(text || `Error ${res.status}: ${res.statusText}`)
    }
    return res.json()
  } catch (error) {
    clearTimeout(timeoutId)
    if (config.simulateIfOffline) {
      // Fallback local de simulación para desarrollo sin backend
      const simulated: AskResponse = {
        answer: 'Simulación local: para respuestas reales conecta el Chat API en Configuración.'
      }
      return simulated
    }
    if (error instanceof Error && error.name === 'AbortError') {
      throw new Error('La solicitud tardó demasiado. Verifica la URL del API.')
    }
    throw error
  }
}

export async function getHistory(sessionId: string): Promise<{ messages: Array<{ id: string; role: 'user'|'assistant'; content: string; timestamp?: string }> }> {
  const cfg = getApiConfig()
  const url = new URL(`${cfg.chatApiUrl}/chat/history`)
  url.searchParams.set('session_id', sessionId)
  const headers: Record<string, string> = {}
  if (cfg.authToken) headers['Authorization'] = cfg.authToken
  const res = await fetch(url.toString(), { headers })
  if (!res.ok) throw new Error('No se pudo obtener el historial')
  return res.json()
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const cfg = getApiConfig()
  try {
    const res = await fetch(`${cfg.chatApiUrl}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    if (!res.ok) throw new Error('Login failed')
    return res.json()
  } catch (e) {
    if (cfg.simulateIfOffline) {
      return { access_token: 'mock-token-123', token_type: 'Bearer' }
    }
    throw e
  }
}

export async function register(name: string, email: string, password: string): Promise<{ status: string; message?: string }> {
  const cfg = getApiConfig()
  try {
    const res = await fetch(`${cfg.chatApiUrl}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    })
    if (!res.ok) throw new Error('Register failed')
    return res.json()
  } catch (e) {
    if (cfg.simulateIfOffline) {
      return { status: 'ok', message: 'Usuario registrado (mock)' }
    }
    throw e
  }
}


