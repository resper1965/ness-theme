import { useCallback } from "react";
import { getPlaygroundSessionAPI } from "@/api/playground";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import { PlaygroundChatMessage, ToolCall } from "@/types/playground";

interface ReasoningMessage {
  role: string;
  content: string;
  tool_call_id?: string;
  tool_name?: string;
  tool_args?: Record<string, string>;
  tool_call_error?: boolean;
  metrics?: { time: number };
  created_at?: number;
}

interface SessionResponse {
  session_id: string;
  agent_id: string;
  user_id: string | null;
  memory: {
    runs?: Array<{
      message: {
        role: string;
        content: string;
        created_at: number;
      };
      response: {
        content: string;
        tools?: ToolCall[];
        extra_data?: {
          reasoning_messages?: ReasoningMessage[];
        };
        images?: string[];
        videos?: string[];
        audio?: string[];
        response_audio?: {
          transcript?: string;
        };
        created_at: number;
      };
    }>;
    chats?: any[];
  };
  agent_data: Record<string, any>;
}

const useSessionLoader = () => {
  const setMessages = usePlaygroundStore((state) => state.setMessages);
  const selectedEndpoint = usePlaygroundStore((state) => state.selectedEndpoint);

  const loadSession = useCallback(
    async (sessionId: string, agentId: string) => {
      if (!sessionId || !agentId || !selectedEndpoint) {
        return null;
      }

      try {
        const response = await getPlaygroundSessionAPI(
          selectedEndpoint,
          agentId,
          sessionId
        ) as SessionResponse;

        if (response && response.memory) {
          const chatHistory = response.memory.runs ?? response.memory.chats;

          if (chatHistory && Array.isArray(chatHistory)) {
            const messagesForPlayground = chatHistory.flatMap((run) => {
              const filteredMessages: PlaygroundChatMessage[] = [];

              if (run.message) {
                filteredMessages.push({
                  role: "user",
                  content: run.message.content ?? "",
                  created_at: run.message.created_at,
                });
              }

              if (run.response) {
                const toolCalls = [
                  ...(run.response.tools ?? []),
                  ...(run.response.extra_data?.reasoning_messages ?? []).reduce(
                    (acc: ToolCall[], msg: ReasoningMessage) => {
                      if (msg.role === "tool") {
                        acc.push({
                          role: msg.role,
                          content: msg.content,
                          tool_call_id: msg.tool_call_id ?? "",
                          tool_name: msg.tool_name ?? "",
                          tool_args: msg.tool_args ?? {},
                          tool_call_error: msg.tool_call_error ?? false,
                          metrics: msg.metrics ?? { time: 0 },
                          created_at: msg.created_at ?? Math.floor(Date.now() / 1000),
                        });
                      }
                      return acc;
                    },
                    []
                  ),
                ];

                filteredMessages.push({
                  role: "agent",
                  content: (run.response.content as string) ?? "",
                  tool_calls: toolCalls.length > 0 ? toolCalls : undefined,
                  extra_data: run.response.extra_data,
                  images: run.response.images,
                  videos: run.response.videos,
                  audio: run.response.audio,
                  response_audio: run.response.response_audio,
                  created_at: run.response.created_at,
                });
              }
              return filteredMessages;
            });

            const processedMessages = messagesForPlayground.map(
              (message: PlaygroundChatMessage) => {
                if (Array.isArray(message.content)) {
                  const textContent = message.content
                    .filter((item: { type: string }) => item.type === "text")
                    .map((item) => item.text)
                    .join(" ");

                  return {
                    ...message,
                    content: textContent,
                  };
                }
                return message;
              }
            );

            setMessages(processedMessages);
            return processedMessages;
          }
        }
        throw new Error("Invalid session data structure");
      } catch (error) {
        console.error("Error loading session:", error);
        return null;
      }
    },
    [selectedEndpoint, setMessages]
  );

  return { loadSession };
};

export default useSessionLoader;
