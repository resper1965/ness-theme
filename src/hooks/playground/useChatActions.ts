import { useCallback } from "react";
import { toast } from "sonner";

// import { useParams } from 'next/navigation'
// import { useQueryState } from 'nuqs'
// import { toast } from 'react-toastify'

// import { deletePlaygroundSessionAPI } from '@/api/playground'
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
// import { type DefaultPageParams } from '@/types/globals'
import { type PlaygroundChatMessage } from "@/types/playground";
import {
  getPlaygroundAgentsAPI,
  getPlaygroundStatusAPI,
} from "@/api/playground";
// import { constructEndpointUrl } from '@/utils/playgroundUtils'
// import useUser from '../useUser'

const useChatActions = () => {
  // const params = useParams<DefaultPageParams>()
  // const [sessionId, setSessionId] = useQueryState('session')
  // const [selectedAgent] = useQueryState('agent')
  const selectedEndpoint = usePlaygroundStore(
    (state) => state.selectedEndpoint,
  );
  const setMessages = usePlaygroundStore((state) => state.setMessages);
  const setIsEndpointActive = usePlaygroundStore(
    (state) => state.setIsEndpointActive,
  );
  const setAgents = usePlaygroundStore((state) => state.setAgents);
  // const setHistoryData = usePlaygroundStore((state) => state.setHistoryData)
  // const historyData = usePlaygroundStore((state) => state.historyData)
  // const username = useUser()?.username

  // const teamURL = params.account !== username ? params.account : undefined
  // const userId = teamURL ? `${username}__${teamURL}` : username

  const getStatus = useCallback(async () => {
    try {
      const status = await getPlaygroundStatusAPI(selectedEndpoint);
      return status;
    } catch {
      toast.error("Error fetching status");
      return 503;
    }
  }, [selectedEndpoint]);

  const getAgents = useCallback(async () => {
    try {
      const agents = await getPlaygroundAgentsAPI(selectedEndpoint);
      return agents;
    } catch {
      toast.error("Error fetching agents");
      return [];
    }
  }, [selectedEndpoint]);

  const clearChat = useCallback(() => {
    setMessages([]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const addMessage = useCallback(
    (message: PlaygroundChatMessage) => {
      setMessages((prevMessages) => [...prevMessages, message]);
    },
    [setMessages],
  );

  const loadData = useCallback(async () => {
    const status = await getStatus();
    if (status === 200) {
      setIsEndpointActive(true);
      const agents = await getAgents();
      setAgents(agents);
      return agents;
    } else {
      setIsEndpointActive(false);
      setAgents([]);
      return [];
    }
  }, [getStatus, getAgents, setIsEndpointActive, setAgents]);

  // const deleteSession = useCallback(
  //   async (sessionIdToDelete: string) => {age
  //     if (!selectedAgent || !selectedEndpoint) {
  //       throw new Error('Selected agent or endpoint is missing')
  //     }
  //     try {
  //       const response = await deletePlaygroundSessionAPI(
  //         sessionIdToDelete,
  //         selectedAgent,
  //         constructEndpointUrl(selectedEndpoint),
  //         userId!
  //       )
  //       if (response.status === 200) {
  //         setHistoryData(
  //           historyData.filter(
  //             (entry) => entry.session_id !== sessionIdToDelete
  //           )
  //         )
  //         toast.success('Session deleted successfully')
  //       }
  //       if (sessionIdToDelete === sessionId) {
  //         clearChat()
  //       }
  //     } catch {
  //       toast.error('Failed to delete session')
  //     }
  //   },
  //   [
  //     selectedAgent,
  //     selectedEndpoint,
  //     userId,
  //     sessionId,
  //     setHistoryData,
  //     historyData,
  //     clearChat
  //   ]
  // )

  return {
    clearChat,
    addMessage,
    getAgents,
    loadData,
  };
};

export default useChatActions;
