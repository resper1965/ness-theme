import { memo } from "react";
import dayjs from "dayjs";
import { UserIcon } from "@/components/ui/Icons";

import MarkdownRenderer from "@/components/ui/typography/MarkdownRenderer";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";

import type { PlaygroundChatMessage } from "@/types/playground";
import { Sparkles } from "lucide-react";

interface MessageProps {
  message: PlaygroundChatMessage;
}

export const AgentMessage = ({ message }: MessageProps) => {
  const { streamingError } = usePlaygroundStore();

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
      <div className="flex items-start text-md">Thinking...</div>
    );
  }

  return (
    <div className="flex flex-row items-start gap-4">
      <div className="shrink-0">
        <div className="bg-brand text-secondary rounded-full p-1">
          <Sparkles size={16} />
        </div>
      </div>
      {messageContent}
    </div>
  );
};

export const UserMessage = memo(({ message }: MessageProps) => {
  return (
    <div className="flex items-start pt-4 text-start max-md:break-words">
      <div className="flex flex-col gap-y-3">
        <p className="text-muted flex items-center gap-x-2 text-xs font-medium">
          <UserIcon /> <span className="uppercase">you</span>{" "}
          <span>[{dayjs().format("HH:mm")}]</span>
        </p>
        <div className="text-sm text-secondary py-1 rounded-lg">
          {message.content}
        </div>
      </div>
    </div>
  );
});

UserMessage.displayName = "UserMessage";
