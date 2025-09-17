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
      chatApiUrl: import.meta.env.VITE_CHAT_API_URL || 'http://127.0.0.1:8000/api/v1', // http://127.0.0.1:8000/api/v1/generate
      timeout: 30000,
      topK: 8,
      simulateIfOffline: false
    }
  )
}

export async function askQuestion(
  prompt: string,
  sessionId?: string,
  model_id?: string,
  max_tokens?: number,
  temperature?: number
): Promise<AskResponse> {


//   {
//         "prompt": "tienes historicos sobre el desempeño de la accion de apple?",
//         //"model_id": "dummy-claude-3-haiku",
//         "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
//         "max_tokens": 250,
//         "temperature": 0.7,
//         "top_k":0,
//         "session_id": "id-de-conversacion"
// }

  const config = getApiConfig()
  const payload: Record<string, unknown> = { prompt }
  if (sessionId) payload.session_id = sessionId
  if (config.topK) payload.top_k = config.topK
  if (model_id) payload.model_id = model_id
  if (max_tokens) payload.max_tokens = max_tokens
  if (typeof temperature === 'number') payload.temperature = temperature

  // LOG para depuración
  console.log('[askQuestion] URL base:', config.chatApiUrl)
  console.log('[askQuestion] Payload:', payload)

  // Limpiar la URL base para evitar duplicados de /generate
  let baseUrl = config.chatApiUrl.replace(/\/+$/, '') // quita barras al final
  baseUrl = baseUrl.replace(/\/generate$/, '') // quita /generate si está al final
  const url = `${baseUrl}/generate`
  console.log('[askQuestion] URL final:', url)

  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), config.timeout || 30000)

  try {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    if (config.authToken) headers['Authorization'] = config.authToken

    const res = await fetch(url, {
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
    let responseJson = await res.json()
    // LOG para depuración de la respuesta
    console.log('[askQuestion] Respuesta del servidor:', responseJson)
    // Adaptar para que siempre tenga 'answer'
    if (!responseJson.answer && responseJson.text) {
      responseJson = { ...responseJson, answer: responseJson.text }
    }
    return responseJson
  } catch (error) {
    clearTimeout(timeoutId)
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

export async function deleteHistory(sessionId: string): Promise<{ deleted: number }> {
  const cfg = getApiConfig()
  const url = new URL(`${cfg.chatApiUrl}/chat/history`)
  url.searchParams.set('session_id', sessionId)
  const headers: Record<string, string> = {}
  if (cfg.authToken) headers['Authorization'] = cfg.authToken
  const res = await fetch(url.toString(), { method: 'DELETE', headers })
  if (!res.ok) throw new Error('No se pudo borrar el historial')
  return res.json()
}

// ===== Conversaciones estilo ChatGPT =====
export async function listConversations(): Promise<{ conversations: Array<{ session_id: string; title: string; updated_at?: string; created_at?: string }> }> {
  const cfg = getApiConfig()
  const headers: Record<string, string> = {}
  if (cfg.authToken) headers['Authorization'] = cfg.authToken
  const res = await fetch(`${cfg.chatApiUrl}/conversations`, { headers })
  if (!res.ok) throw new Error('No se pudo listar conversaciones')
  return res.json()
}

export async function createConversation(sessionId: string, title?: string): Promise<{ session_id: string; title: string }> {
  const cfg = getApiConfig()
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (cfg.authToken) headers['Authorization'] = cfg.authToken
  const res = await fetch(`${cfg.chatApiUrl}/conversations`, {
    method: 'POST', headers, body: JSON.stringify({ session_id: sessionId, title })
  })
  if (!res.ok) throw new Error('No se pudo crear la conversación')
  return res.json()
}

export async function renameConversationApi(sessionId: string, title: string): Promise<{ session_id: string; title: string }> {
  const cfg = getApiConfig()
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (cfg.authToken) headers['Authorization'] = cfg.authToken
  const res = await fetch(`${cfg.chatApiUrl}/conversations/${sessionId}`, {
    method: 'PATCH', headers, body: JSON.stringify({ title })
  })
  if (!res.ok) throw new Error('No se pudo renombrar la conversación')
  return res.json()
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const cfg = getApiConfig()
  const res = await fetch(`${cfg.chatApiUrl}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  if (!res.ok) throw new Error('Login failed')
  return res.json()
}

export async function register(name: string, email: string, password: string): Promise<{ status: string; message?: string }> {
  const cfg = getApiConfig()
  const res = await fetch(`${cfg.chatApiUrl}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password })
  })
  if (!res.ok) throw new Error('Register failed')
  return res.json()
}


