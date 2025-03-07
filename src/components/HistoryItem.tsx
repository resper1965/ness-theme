import { useQueryState } from "nuqs";
import { HistoryEntry } from "@/types/playground";
import { Button } from "./ui/button";
import useSessionLoader from "@/hooks/playground/useSessionLoader";

type SessionHistoryItemProps = HistoryEntry;

const truncateTitle = (text: string, limit: number) => {
  if (text) {
    return text.length > limit ? `${text.slice(0, limit)}...` : text;
  }
  return "";
};

export const HistoryItem = ({ title, session_id }: SessionHistoryItemProps) => {
  const [agentId] = useQueryState("agent");
  const { loadSession } = useSessionLoader();
  const [, setSessionId] = useQueryState("session");

  const handleLoadSession = async () => {
    if (agentId) {
      await loadSession(session_id, agentId);
      setSessionId(session_id);
    }
  };

  return (
    <Button
      className="flex w-full items-center h-12 justify-start rounded-lg bg-background-secondary p-3 hover:bg-background-secondary/50"
      variant="default"
      size="icon"
      onClick={handleLoadSession}
    >
      <div className="flex flex-col gap-1">
        <h4 className="text-sm font-medium">{truncateTitle(title, 20)}</h4>
      </div>
    </Button>
  );
};
