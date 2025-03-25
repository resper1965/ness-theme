"use client";

import ChatInput from "./ChatInput";
import MessageArea from "./MessageArea";
const ChatArea = () => {
  return (
    <main className="relative flex flex-col flex-grow bg-background rounded-xl m-1.5">
      <MessageArea />
      <div className="sticky bottom-0 px-4 pb-2 ml-9">
        <ChatInput />
      </div>
    </main>
  );
};

export default ChatArea;
