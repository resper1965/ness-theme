"use client";
import { Button } from "@/components/ui/button";
import { PlusIcon } from "@radix-ui/react-icons";
import { AgentSelector } from "@/components/AgentSelector";
import useChatActions from "@/hooks/playground/useChatActions";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import { useQueryState } from "nuqs";
import { useEffect, useState } from "react";
import { RefreshCcw } from "lucide-react";
import Icon from "@/components/ui/icon";
import { getProviderIcon } from "@/utils/modelProvider";
const SidebarHeader = () => (
  <div className="flex items-center gap-2">
    <Icon type="agno" size="sm" />
    <span className="text-white text-xs font-medium uppercase font-geist-mono">
      Agent UI
    </span>
  </div>
);

const NewChatButton = ({
  disabled,
  onClick,
}: {
  disabled: boolean;
  onClick: () => void;
}) => (
  <Button
    onClick={onClick}
    disabled={disabled}
    size="lg"
    className="bg-primary text-background hover:bg-primary/80 rounded-xl text-xs font-medium w-full"
  >
    <PlusIcon />
    <span className="uppercase">New Chat</span>
  </Button>
);

const ModelDisplay = ({ model }: { model: string }) => (
  <div className="w-full border-primary/20 flex items-center gap-3 border text-muted text-xs font-medium bg-accent rounded-xl uppercase p-3">
    {(() => {
      const icon = getProviderIcon(model);
      return icon ? <Icon type={icon} className="shrink-0" size="xs" /> : null;
    })()}
    {model}
  </div>
);

const Endpoint = () => {
  const { selectedEndpoint, isEndpointActive } = usePlaygroundStore();
  const { loadData } = useChatActions();

  const getStatusColor = (isActive: boolean) =>
    isActive ? "bg-positive" : "bg-destructive";

  return (
    <div className="flex flex-col items-start gap-2">
      <div className="uppercase text-xs font-medium text-primary">Endpoint</div>
      <div className="flex w-full gap-4 items-center">
        <div className="flex w-full items-center justify-between border-primary/20 border bg-accent rounded-xl uppercase p-3">
          <p className="text-xs font-medium text-muted "> {selectedEndpoint}</p>
          <div
            className={`size-2 rounded-full ${getStatusColor(isEndpointActive)}`}
          />
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={loadData}
          className="hover:bg-transparent hover:cursor-pointer"
        >
          <RefreshCcw size={16} />
        </Button>
      </div>
    </div>
  );
};

// Main Sidebar component
export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const { clearChat, loadData } = useChatActions();
  const { messages, selectedEndpoint, isEndpointActive } = usePlaygroundStore();
  const [model] = useQueryState("model");

  useEffect(() => {
    if (selectedEndpoint) {
      loadData();
    }
  }, [selectedEndpoint, loadData]);

  return (
    <aside
      className={`h-screen relative bg-primaryAccent py-6 pl-4 pr-3 flex flex-col gap-4 shrink-0 grow-0
        ${isCollapsed ? "w-12" : "w-80"} transition-all duration-300 ease-in-out overflow-hidden`}
    >
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute top-4 right-2 p-1"
        aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        type="button"
      >
        <Icon
          type="sheet"
          size="xs"
          className={`transform ${isCollapsed ? "rotate-180" : "rotate-0"}`}
        />
      </button>
      <div
        className={`space-y-5 transition-[opacity,visibility] duration-200 ${
          isCollapsed ? "invisible opacity-0" : "visible opacity-100"
        }`}
      >
        <SidebarHeader />
        <NewChatButton disabled={messages.length === 0} onClick={clearChat} />
        {selectedEndpoint && (
          <>
            <Endpoint />
            {isEndpointActive && (
              <div className="flex flex-col items-start gap-2">
                <div className="uppercase text-xs font-medium text-primary">
                  Agent
                </div>
                <AgentSelector />
                {model && <ModelDisplay model={model} />}
              </div>
            )}
          </>
        )}
      </div>
    </aside>
  );
}
