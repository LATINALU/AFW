"use client";

import React from "react";
import { motion } from "framer-motion";

interface ChatBubbleProps {
  role: "user" | "assistant";
  content: string;
  agentName?: string;
  agentEmoji?: string;
  timestamp?: string;
  isStreaming?: boolean;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  role,
  content,
  agentName,
  agentEmoji,
  timestamp,
  isStreaming = false,
}) => {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : "flex-row"}`}
    >
      {/* Avatar */}
      <div
        className={`
          w-10 h-10 rounded-full flex items-center justify-center text-lg shrink-0
          ${isUser
            ? "bg-gradient-to-br from-primary to-secondary text-white"
            : "bg-gradient-to-br from-card to-muted border border-border"
          }
        `}
      >
        {isUser ? "👤" : agentEmoji || "🤖"}
      </div>

      {/* Message */}
      <div
        className={`
          max-w-[80%] rounded-2xl px-4 py-3
          ${isUser
            ? "bg-gradient-to-br from-primary to-primary/80 text-white rounded-tr-sm"
            : "bg-card border border-border rounded-tl-sm"
          }
        `}
      >
        {!isUser && agentName && (
          <p className="text-xs text-primary font-semibold mb-1 flex items-center gap-1">
            {agentEmoji && <span>{agentEmoji}</span>}
            {agentName}
          </p>
        )}
        
        <div className="text-sm leading-relaxed whitespace-pre-wrap">
          {content}
          {isStreaming && (
            <span className="inline-block w-2 h-4 bg-primary/70 ml-1 animate-pulse" />
          )}
        </div>

        {timestamp && (
          <p className={`text-[10px] mt-2 ${isUser ? "text-white/60" : "text-gray-500"}`}>
            {timestamp}
          </p>
        )}
      </div>
    </motion.div>
  );
};

export default ChatBubble;
