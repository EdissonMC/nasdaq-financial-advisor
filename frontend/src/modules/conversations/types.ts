import type { ChatMessage } from '../chat/ChatWindow'

export type Conversation = {
  id: string
  title: string
  messages: ChatMessage[]
  createdAt: number
  updatedAt: number
}


