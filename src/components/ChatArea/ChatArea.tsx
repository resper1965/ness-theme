"use client";

import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import MessageList from "./Messages/MessageList";
const ChatArea = () => {
  const { messages } = usePlaygroundStore();

  return (
    <div className="relative flex min-h-0 flex-grow flex-col overflow-y-auto">
      <div className="flex min-h-full flex-col justify-center">
        <div className="mx-auto w-full max-w-2xl space-y-9 px-4 pb-4">
          <MessageList messages={messages} />
        </div>
      </div>
    </div>
  );
};

export default ChatArea;
