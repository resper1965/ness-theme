"use client";
import Sidebar from "@/components/playground/Sidebar/Sidebar";
import { ChatArea, ChatInput } from "@/components/playground/ChatArea";
import { Suspense } from "react";

export default function Home() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div className="flex h-screen bg-background/80">
        <Sidebar />
        <main className="relative flex flex-col flex-grow bg-background rounded-xl m-1.5">
          <ChatArea />
          <div className="sticky bottom-0 px-4 pb-2 ml-9">
            <ChatInput />
          </div>
        </main>
      </div>
    </Suspense>
  );
}
