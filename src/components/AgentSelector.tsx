"use client";

import * as React from "react";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import useChatActions from "@/hooks/playground/useChatActions";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import { useEffect } from "react";
import { AgentIcon } from "./ui/Icons";
import { useQueryState } from "nuqs";

interface Agent {
  value: string;
  label: string;
}

export function AgentSelector() {
  const [agents, setAgents] = React.useState<Agent[]>([]);
  const setMessages = usePlaygroundStore((state) => state.setMessages);
  const { getAgents } = useChatActions();

  const [agentId, setAgentId] = useQueryState("agent", {
    parse: (value) => value || undefined,
    history: "push",
  });

  useEffect(() => {
    const fetchAgents = async () => {
      const result: Agent[] = await getAgents();
      setAgents(result);
    };
    fetchAgents();
  }, [getAgents]);

  return (
    <Select
      value={agentId || ""}
      onValueChange={(value) => {
        const newAgent = value === agentId ? "" : value;
        setAgentId(newAgent);
        setMessages([]);
      }}
    >
      <SelectTrigger className="w-full border-none text-xs font-medium bg-[#27272a] rounded-lg uppercase">
        <SelectValue placeholder="Select Agent" />
      </SelectTrigger>
      <SelectContent className="border-none bg-[#27272a] rounded-lg">
        {agents.map((agent, index) => (
          <SelectItem key={`${agent.value}-${index}`} value={agent.value}>
            <div className="flex items-center gap-2 cursor-pointer uppercase text-xs font-medium">
              <AgentIcon /> {agent.label}
            </div>
          </SelectItem>
        ))}
        {agents.length === 0 && (
          <SelectItem
            value="no-agents"
            className="text-center cursor-not-allowed select-none"
          >
            No agents found
          </SelectItem>
        )}
      </SelectContent>
    </Select>
  );
}
