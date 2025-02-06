"use client";
import { useState } from "react";
import { toast } from "sonner";
import { PlaygroundTextArea } from "./PlaygroundTextArea";
import { Button } from "@/components/ui/button";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import useAIChatStreamHandler from "@/hooks/playground/useAIStreamHandler";
import { SendIcon } from "lucide-react";
// import { useAgentsQuery } from '@/hooks/playground/useAgentsQuery'
const ChatInput = () => {
  const { chatInputRef } = usePlaygroundStore();

  // const [selectedAgent] = useQueryState('agent')
  // const [selectedEndpoint] = useQueryState('endpoint')

  // const { data: agents = [] } = useAgentsQuery(selectedEndpoint)
  const { handleStreamResponse } = useAIChatStreamHandler();
  const selectedAgent = usePlaygroundStore((state) => state.selectedAgent);
  const setStreamingError = usePlaygroundStore(
    (state) => state.setStreamingError,
  );
  const streamingError = usePlaygroundStore((state) => state.streamingError);
  const [inputMessage, setInputMessage] = useState("");

  const handleSubmit = async () => {
    if (!inputMessage.trim()) return;

    // if (!selectedEndpoint || !selectedAgent) {
    // toast.error('No endpoint or agent selected')
    // return
    // }

    if (streamingError) {
      setStreamingError(false);
    }

    const currentMessage = inputMessage;
    setInputMessage("");

    try {
      await handleStreamResponse(currentMessage);
    } catch (error) {
      toast.error(
        `Error in handleSubmit: ${
          error instanceof Error ? error.message : String(error)
        }`,
      );
    }
  };

  const isDisabled = selectedAgent === "";

  return (
    <div className="relative mx-auto flex w-full max-w-2xl justify-center gap-x-2 mb-1 font-inter">
      <PlaygroundTextArea
        placeholder={"Ask anything"}
        value={inputMessage}
        onChange={(e) => setInputMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
          }
        }}
        className="w-full border border-border/50 pr-10 text-sm focus:border-border bg-primary"
        disabled={isDisabled}
        ref={chatInputRef}
      />
      <Button
        onClick={handleSubmit}
        disabled={isDisabled}
        variant="link"
        className="absolute bottom-[-12px] right-1.5 -translate-y-1/2 text-secondary"
      >
        <SendIcon className="w-4 h-4" />
      </Button>
    </div>
  );
};

export default ChatInput;
