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

interface Agent {
  value: string;
  label: string;
}

export function AgentSelector() {
  const [agents, setAgents] = React.useState<Agent[]>([]);
  const selectedAgent = usePlaygroundStore((state) => state.selectedAgent);
  const setSelectedAgent = usePlaygroundStore(
    (state) => state.setSelectedAgent,
  );
  const { getAgents } = useChatActions();

  // Fetch agents when the component mounts
  useEffect(() => {
    const fetchAgents = async () => {
      const result: Agent[] = await getAgents();
      setAgents(result);
    };
    fetchAgents();
  }, [getAgents]);

  return (
    <Select
      value={selectedAgent || ""}
      onValueChange={(value) =>
        setSelectedAgent(value === selectedAgent ? "" : value)
      }
    >
      <SelectTrigger className="w-60 border-border/50 focus:border-border/100">
        <SelectValue placeholder="Select agent..." />
      </SelectTrigger>
      <SelectContent className="border-border/50 focus:border-border/100">
        {agents.map((agent, index) => (
          <SelectItem key={`${agent.value}-${index}`} value={agent.value}>
            {agent.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
