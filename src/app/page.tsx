"use client";
import Sidebar from "@/components/Sidebar";
import ChatArea from "@/components/ChatArea/ChatArea";
import ChatInput from "@/components/ChatArea/ChatInput/ChatInput";

export default function Home() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="relative flex flex-col flex-grow bg-background rounded-xl m-1.5">
        <ChatArea />
        <div className="sticky bottom-0 px-4 pb-2">
          <ChatInput />
        </div>
      </main>
    </div>
  );
}
