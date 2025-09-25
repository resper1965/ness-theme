'use client'

import ChatInput from './ChatInput'
import MessageArea from './MessageArea'
const ChatArea = () => {
  return (
    <main className="relative flex flex-grow flex-col bg-background overflow-hidden">
      <div className="flex-1 overflow-y-auto">
        <MessageArea />
      </div>
      <div className="sticky bottom-0 bg-background/80 backdrop-blur-sm border-t border-border px-4 py-4">
        <ChatInput />
      </div>
    </main>
  )
}

export default ChatArea
