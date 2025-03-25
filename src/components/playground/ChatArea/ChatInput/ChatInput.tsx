"use client";
import { useState } from "react";
import { toast } from "sonner";
import { TextArea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { usePlaygroundStore } from "@/store";
import useAIChatStreamHandler from "@/hooks/useAIStreamHandler";
import { useQueryState } from "nuqs";
import Icon from "@/components/ui/icon";

const ChatInput = () => {
  const { chatInputRef } = usePlaygroundStore();

  const { handleStreamResponse } = useAIChatStreamHandler();
  const [selectedAgent] = useQueryState("agent");
  const [inputMessage, setInputMessage] = useState("");
  const isStreaming = usePlaygroundStore((state) => state.isStreaming);
  const handleSubmit = async () => {
    if (!inputMessage.trim()) return;

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

  return (
    <div className="relative mx-auto flex w-full max-w-2xl justify-center items-end gap-x-2 mb-1 font-geist">
      <TextArea
        placeholder={"Ask anything"}
        value={inputMessage}
        onChange={(e) => setInputMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
          }
        }}
        className="w-full border border-accent px-4 text-sm focus:border-accent bg-primaryAccent text-primary"
        disabled={!selectedAgent || isStreaming}
        ref={chatInputRef}
      />
      <Button
        onClick={handleSubmit}
        disabled={!selectedAgent || !inputMessage.trim() || isStreaming}
        size="icon"
        className="bg-primary text-primaryAccent p-5 rounded-xl"
      >
        <Icon type="send" color="primaryAccent" />
      </Button>
    </div>
  );
};

export default ChatInput;
