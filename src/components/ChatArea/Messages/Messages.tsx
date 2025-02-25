import { memo } from "react";
import { AgentIcon, UserIcon } from "@/components/ui/Icons";
import { useQueryState } from "nuqs";
import MarkdownRenderer from "@/components/ui/typography/MarkdownRenderer";
import { usePlaygroundStore } from "@/stores/PlaygroundStore";

import type { PlaygroundChatMessage } from "@/types/playground";
import Videos from "./Multimedia/Videos";
import Images from "./Multimedia/Images";
import Audios from "./Multimedia/Audios";


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
        {message.videos && message.videos.length > 0 && (
          <Videos videos={message.videos} />
        )}
        {message.images && message.images.length > 0 && (
          <Images images={message.images} />
        )}
        {message.audio && message.audio.length > 0 && (
          <Audios audio={message.audio} />
        )}
      </div>
    );
  } else if (message.response_audio) {
    if (!message.response_audio.transcript) {
      messageContent = (
        <div className="mt-2 flex items-start">
          {/* <AgentThinkingLoader /> */}
          thinking...
        </div>
      );
    } else {
      messageContent = (
        <div className="flex w-full flex-col gap-4">
          <MarkdownRenderer>
            {message.response_audio.transcript}
          </MarkdownRenderer>
          {message.response_audio.content && message.response_audio && (
            <Audios audio={[message.response_audio]} />
          )}
        </div>
      );
    }
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
    <div className="flex flex-col items-start gap-4 font-geist">
      <div className="flex items-center gap-x-2 text-sm font-medium font-geist uppercase text-brand">
        <AgentIcon /> {selectedAgent}
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
          <UserIcon /> <span className="uppercase">you</span>{" "}
        </p>
        <div className="text-md text-secondary py-1 rounded-lg font-geist">
          {message.content}
        </div>
      </div>
    </div>
  );
});

UserMessage.displayName = "UserMessage";
