"use client";

import * as React from "react";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import { useQueryState } from "nuqs";
import Icon from "@/components/ui/icon";
export function AgentSelector() {
  const { agents, setMessages } = usePlaygroundStore();
  const [agentId, setAgentId] = useQueryState("agent", {
    parse: (value) => value || undefined,
    history: "push",
  });

  const [, setModel] = useQueryState("model", {
    history: "push",
  });

  return (
    <Select
      value={agentId || ""}
      onValueChange={(value) => {
        const newAgent = value === agentId ? "" : value;
        setModel(
          agents.find((agent) => agent.value === newAgent)?.model.provider ||
            "",
        );
        setAgentId(newAgent);
        setMessages([]);
      }}
    >
      <SelectTrigger className="w-full border-primary/20 border text-xs font-medium bg-primaryAccent rounded-xl uppercase">
        <SelectValue placeholder="Select Agent" />
      </SelectTrigger>
      <SelectContent className="border-primary/20 border bg-primaryAccent">
        {agents.map((agent, index) => (
          <SelectItem key={`${agent.value}-${index}`} value={agent.value}>
            <div className="flex items-center gap-3 cursor-pointer uppercase text-xs font-medium">
              <Icon type={"agent"} size="xs" />
              {agent.label}
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
