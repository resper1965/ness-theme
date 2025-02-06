"use client";
import { Button } from "../ui/button";
import { PlusIcon } from "@radix-ui/react-icons";
import useChatActions from "@/hooks/playground/useChatActions";

function NewChatButton() {
  const { clearChat } = useChatActions();
  return (
    <Button
      className="absolute top-4 left-4 z-10 bg-brand hover:bg-brand/80 text-white font-bold py-2 px-4 rounded cursor-pointer"
      onClick={clearChat}
    >
      <div className="flex items-center gap-2">
        <p>New Chat</p> <PlusIcon />
      </div>
    </Button>
  );
}

export default NewChatButton;
