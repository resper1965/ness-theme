import { memo } from "react";
import { useQueryState } from "nuqs";
import MarkdownRenderer from "@/components/ui/typography/MarkdownRenderer";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";
import Icon from "@/components/ui/icon";
import type { PlaygroundChatMessage } from "@/types/playground";
import { Loader } from "lucide-react";

interface MessageProps {
  message: PlaygroundChatMessage;
}

export const AgentMessage = ({ message }: MessageProps) => {
  const { streamingError } = usePlaygroundStore();
  const [selectedAgent] = useQueryState("agent");
  let messageContent;
  if (message.content) {
    messageContent = (
      <div className="flex w-full flex-col gap-4">
        <MarkdownRenderer>{message.content}</MarkdownRenderer>
      </div>
    );
  } else if (streamingError) {
    messageContent = (
      <p className="text-destructive">
        Oops! Something went wrong with the stream. Please try again, or refresh
        the page.
      </p>
    );
  } else {
    messageContent = (
      <div className="flex items-center justify-center text-md gap-4">
        <Loader
          size={16}
          className="animate-spin [animation-duration:2s] text-brand"
        />
        <p className="text-muted">Thinking...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-start gap-4 font-geist">
      <div className="flex items-center gap-x-2 text-sm font-medium font-geist uppercase text-brand">
        <Icon type="agent" size="xs" /> 
        {selectedAgent}
      </div>
      {messageContent}
    </div>
  );
};

export const UserMessage = memo(({ message }: MessageProps) => {
  return (
    <div className="flex items-start pt-4 text-start max-md:break-words">
      <div className="flex flex-col gap-y-3">
        <p className="text-muted flex items-center gap-x-2 text-sm font-medium">
          <Icon type="user" size="xs" /> 
          <span className="uppercase">you</span>{" "}
        </p>
        <div className="text-md text-secondary py-1 rounded-lg font-geist">
          {message.content}
        </div>
      </div>
    </div>
  );
});

UserMessage.displayName = "UserMessage";
