import { toast } from "sonner";

import { APIRoutes } from "./routes";

import { Agent } from "@/types/playground";

// Define a local type to shape the agent data for the combobox.
interface ComboboxAgent {
  value: string;
  label: string;
}

export const getPlaygroundAgentsAPI = async (
  endpoint: string,
): Promise<ComboboxAgent[]> => {
  const url = APIRoutes.GetPlaygroundAgents(endpoint);
  try {
    const response = await fetch(url, { method: "GET" });
    if (!response.ok) {
      toast.error(`Failed to fetch playground agents: ${response.statusText}`);
      return [];
    }
    const data = await response.json();
    // Transform the API response into the expected shape.
    const agents: ComboboxAgent[] = data.map((item: Agent) => ({
      value: item.agent_id || "",
      label: item.name || "",
    }));
    return agents;
  } catch {
    toast.error("Error fetching playground agents");
    return [];
  }
};
