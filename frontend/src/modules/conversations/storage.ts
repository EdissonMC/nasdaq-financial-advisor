import type { Conversation } from './types'
import { getHistory, deleteHistory } from '../../services/api'

const KEY = 'fa_chat_conversations_v1'

export function loadConversations(): Conversation[] {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw) as Conversation[]
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function saveConversations(conversations: Conversation[]) {
  localStorage.setItem(KEY, JSON.stringify(conversations))
}

// Sincronización básica con backend para que no quede como "guardado localmente"
export async function syncConversationFromApi(conv: Conversation): Promise<Conversation> {
  try {
    const data = await getHistory(conv.id)
    if (data && Array.isArray(data.messages) && data.messages.length > 0) {
      return {
        ...conv,
        messages: data.messages.map(m => ({ id: m.id, role: m.role, content: m.content })),
        updatedAt: Date.now()
      }
    }
  } catch {
    // ignorar
  }
  return conv
}

export async function removeConversationFromApi(sessionId: string): Promise<void> {
  try { await deleteHistory(sessionId) } catch {}
}


