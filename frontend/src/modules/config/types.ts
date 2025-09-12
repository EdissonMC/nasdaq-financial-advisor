export type ApiConfig = {
  chatApiUrl: string
  timeout?: number
  topK?: number
  simulateIfOffline?: boolean
  authToken?: string
}

export type ConfigState = {
  api: ApiConfig
  isModalOpen: boolean
}
