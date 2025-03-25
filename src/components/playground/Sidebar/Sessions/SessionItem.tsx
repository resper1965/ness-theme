import { useQueryState } from "nuqs";
import { SessionEntry } from "@/types/playground";
import { Button } from "../../../ui/button";
import useSessionLoader from "@/hooks/useSessionLoader";
import { deletePlaygroundSessionAPI } from "@/api/playground";
import { usePlaygroundStore } from "@/store";
import { toast } from "sonner";
import Icon from "@/components/ui/icon";
import { useState } from "react";
import DeleteSessionModal from "./DeleteSessionModal";
import useChatActions from "@/hooks/useChatActions";

const truncateTitle = (text: string, limit: number) => {
  if (text) {
    return text.length > limit ? `${text.slice(0, limit)}...` : text;
  }
  return "";
};

export const SessionItem = ({ title, session_id }: SessionEntry) => {
  const [agentId] = useQueryState("agent");
  const { loadSession } = useSessionLoader();
  const [, setSessionId] = useQueryState("session");
  const { selectedEndpoint, historyData, setHistoryData } =
    usePlaygroundStore();
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const { clearChat } = useChatActions();

  const handleLoadSession = async () => {
    if (agentId) {
      await loadSession(session_id, agentId);
      setSessionId(session_id);
    }
  };

  const handleDeleteSession = async () => {
    if (agentId) {
      try {
        const response = await deletePlaygroundSessionAPI(
          selectedEndpoint,
          agentId,
          session_id
        );
        if (response.status === 200 && historyData) {
          setHistoryData(
            historyData.filter((session) => session.session_id !== session_id)
          );
          clearChat();
          toast.success("Session deleted");
        } else {
          toast.error("Failed to delete session");
        }
      } catch {
        toast.error("Failed to delete session");
      } finally {
        setIsDeleteModalOpen(false);
      }
    }
  };

  return (
    <>
      <div
        className="flex w-full items-center h-11 justify-between rounded-lg bg-background-secondary px-3 cursor-pointer group py-2"
        onClick={handleLoadSession}
      >
        <div className="flex flex-col gap-1">
          <h4 className="text-sm font-medium">{truncateTitle(title, 20)}</h4>
        </div>
        <Button
          variant="ghost"
          size="icon"
          className="transform transition-all duration-200 ease-in-out opacity-0 group-hover:opacity-100"
          onClick={(e) => {
            e.stopPropagation();
            setIsDeleteModalOpen(true);
          }}
        >
          <Icon type="trash" size="xs" />
        </Button>
      </div>
      <DeleteSessionModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onDelete={handleDeleteSession}
        isDeleting={false}
      />
    </>
  );
};
