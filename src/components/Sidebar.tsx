"use client";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "@radix-ui/react-icons";
import { AgentSelector } from "@/components/AgentSelector";
import useChatActions from "@/hooks/playground/useChatActions";
import { AgnoIcon } from "@/components/ui/Icons";
export default function Sidebar() {
  const { clearChat } = useChatActions();

  return (
    <aside className=" h-screen w-64 bg-[#18181B] p-4 flex flex-col gap-4">
      <div className="flex items-center gap-2">
        <AgnoIcon />
        <span className="text-white text-xs font-medium uppercase font-geist-mono">
          Agno Chat
        </span>
      </div>
      <Button
        onClick={clearChat}
        className="bg-secondary text-primary hover:bg-secondary/80 rounded-xl text-xs"
      >
        <PlusIcon />
        <span className="ml-2 uppercase">New Chat</span>
      </Button>
      <AgentSelector />
    </aside>
  );
}
