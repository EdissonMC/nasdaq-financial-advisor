import type { ApiConfig } from './types'

const CONFIG_KEY = 'fa_chat_config_v1'

const DEFAULT_CONFIG: ApiConfig = {
  chatApiUrl: import.meta.env.VITE_CHAT_API_URL || 'http://localhost:8000',
  timeout: 30000,
  topK: 8,
  simulateIfOffline: true
}

export function loadConfig(): ApiConfig {
  try {
    const stored = localStorage.getItem(CONFIG_KEY)
    if (!stored) return DEFAULT_CONFIG
    
    const parsed = JSON.parse(stored) as ApiConfig
    return {
      chatApiUrl: parsed.chatApiUrl || (parsed as any).baseUrl || DEFAULT_CONFIG.chatApiUrl,
      timeout: parsed.timeout || DEFAULT_CONFIG.timeout,
      topK: parsed.topK || DEFAULT_CONFIG.topK,
      simulateIfOffline: typeof parsed.simulateIfOffline === 'boolean' ? parsed.simulateIfOffline : DEFAULT_CONFIG.simulateIfOffline
    }
  } catch {
    return DEFAULT_CONFIG
  }
}

export function saveConfig(config: ApiConfig) {
  localStorage.setItem(CONFIG_KEY, JSON.stringify(config))
}
