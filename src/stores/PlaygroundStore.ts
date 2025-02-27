import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

import { type PlaygroundChatMessage } from "@/types/playground";

interface Agent {
  value: string;
  label: string;
  model: {
    provider: string;
  };
}

interface PlaygroundStore {
  streamingError: boolean;
  setStreamingError: (streamingError: boolean) => void;
  storage: boolean;
  setStorage: (storage: boolean) => void;
  endpoints: {
    endpoint: string;
    id_playground_endpoint: string;
  }[];
  setEndpoints: (
    endpoints: {
      endpoint: string;
      id_playground_endpoint: string;
    }[]
  ) => void;
  isStreaming: boolean;
  setIsStreaming: (isStreaming: boolean) => void;
  isSidebarCollapsed: boolean;
  setIsSidebarCollapsed: (isSidebarCollapsed: boolean) => void;
  historyLoading: boolean;
  setHistoryLoading: (loading: boolean) => void;
  isEndpointActive: boolean;
  setIsEndpointActive: (isActive: boolean) => void;
  endpointLoading: boolean;
  setEndpointLoading: (loading: boolean) => void;

  messages: PlaygroundChatMessage[];
  setMessages: (
    messages:
      | PlaygroundChatMessage[]
      | ((prevMessages: PlaygroundChatMessage[]) => PlaygroundChatMessage[])
  ) => void;

  chatInputRef: React.RefObject<HTMLTextAreaElement | null>;
  selectedEndpoint: string;
  setSelectedEndpoint: (selectedEndpoint: string) => void;

  agents: Agent[];
  setAgents: (agents: Agent[]) => void;

  selectedModel: string;
  setSelectedModel: (model: string) => void;
}

export const usePlaygroundStore = create<PlaygroundStore>()(
  persist(
    (set) => ({
      streamingError: false,
      setStreamingError: (streamingError) => set(() => ({ streamingError })),
      storage: false,
      setStorage: (storage) => set(() => ({ storage })),
      endpoints: [],
      setEndpoints: (endpoints) => set(() => ({ endpoints })),
      isStreaming: false,
      setIsStreaming: (isStreaming) => set(() => ({ isStreaming })),
      isSidebarCollapsed: true,
      setIsSidebarCollapsed: (isSidebarCollapsed) =>
        set(() => ({ isSidebarCollapsed })),
      historyLoading: false,
      setHistoryLoading: (loading) => set(() => ({ historyLoading: loading })),
      isEndpointActive: false,
      setIsEndpointActive: (isActive) =>
        set(() => ({ isEndpointActive: isActive })),
      endpointLoading: true,
      setEndpointLoading: (loading) =>
        set(() => ({ endpointLoading: loading })),

      messages: [],
      setMessages: (messages) =>
        set((state) => ({
          messages:
            typeof messages === "function"
              ? messages(state.messages)
              : messages,
        })),

      chatInputRef: { current: null },
      selectedEndpoint: "http://localhost:7777",
      setSelectedEndpoint: (selectedEndpoint) =>
        set(() => ({ selectedEndpoint })),

      agents: [],
      setAgents: (agents) => set({ agents }),

      selectedModel: "",
      setSelectedModel: (selectedModel) => set(() => ({ selectedModel })),
    }),
    {
      name: "endpoint-storage",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        selectedEndpoint: state.selectedEndpoint,
        selectedModel: state.selectedModel,
      }),
    }
  )
);
