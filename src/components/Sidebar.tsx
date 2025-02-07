"use client";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "@radix-ui/react-icons";
import { AgentSelector } from "@/components/AgentSelector";
import useChatActions from "@/hooks/playground/useChatActions";
import { AgnoIcon } from "@/components/ui/Icons";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import { useQueryState } from "nuqs";
import { useEffect } from "react";

export default function Sidebar() {
  const { clearChat, loadData } = useChatActions();
  const { messages, selectedEndpoint, isEndpointActive, setAgents } =
    usePlaygroundStore();
  const [model] = useQueryState("model");

  useEffect(() => {
    const initializeData = async () => {
      if (selectedEndpoint) {
        const agents = await loadData();
        setAgents(agents);
      }
    };
    initializeData();
  }, [selectedEndpoint, loadData, setAgents]);

  return (
    <aside className="h-screen w-64 bg-primaryAccent py-4 px-2 flex flex-col gap-4">
      <div className="flex items-center gap-2">
        <AgnoIcon size={20} />
        <span className="text-white text-xs font-medium uppercase font-geist-mono">
          Agent UI
        </span>
      </div>
      <Button
        onClick={clearChat}
        disabled={messages.length === 0}
        className="bg-primary text-background hover:bg-primary/80 rounded-xl text-xs"
      >
        <PlusIcon />
        <span className="uppercase">New Chat</span>
      </Button>
      {selectedEndpoint && (
        <>
          <Endpoint />
          {isEndpointActive && (
            <>
              <div className="flex flex-col items-start gap-2">
                <div className="uppercase text-xs font-medium text-muted">
                  Agent
                </div>
                <AgentSelector />
              </div>
              {model && (
                <div className="flex flex-col items-start gap-2">
                  <div className="uppercase text-xs font-medium text-muted">
                    Model
                  </div>
                  <div className="w-full border-[#FAFAFA0D] border text-xs font-medium bg-accent rounded-lg uppercase py-2.5 px-2">
                    {model}
                  </div>
                </div>
              )}
            </>
          )}
        </>
      )}
    </aside>
  );
}

const Endpoint = () => {
  const { selectedEndpoint } = usePlaygroundStore();

  return (
    <div className="flex flex-col items-start gap-2">
      <div className="uppercase text-xs font-medium text-muted">Endpoint</div>
      <div className="flex w-full">
        <span className="w-full border-[#FAFAFA0D] border text-xs font-medium bg-accent rounded-lg uppercase py-2.5 px-2">
          {selectedEndpoint}
        </span>
      </div>
    </div>
  );
};
