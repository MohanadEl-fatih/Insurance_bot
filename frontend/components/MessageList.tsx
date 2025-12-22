'use client'

import { Message } from './ChatWindow'

interface MessageListProps {
  messages: Message[]
  isLoading: boolean
}

export default function MessageList({ messages, isLoading }: MessageListProps) {
  return (
    <div className="message-list">
      {messages.length === 0 && (
        <div className="empty-state">
          <p>Start a conversation by asking about insurance quotes!</p>
          <p className="example">Try: &quot;I want full insurance for my car&quot;</p>
        </div>
      )}
      {messages.map((message) => (
        <div key={message.id} className={`message message-${message.role}`}>
          <div className="message-content">{message.content}</div>
          <div className="message-time">
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        </div>
      ))}
      {isLoading && (
        <div className="message message-assistant">
          <div className="message-content typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}
      <style jsx>{`
        .message-list {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        .empty-state {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100%;
          color: #666;
          text-align: center;
        }
        .empty-state .example {
          margin-top: 12px;
          font-style: italic;
          color: #999;
          font-size: 14px;
        }
        .message {
          display: flex;
          flex-direction: column;
          max-width: 75%;
          animation: fadeIn 0.3s ease-in;
        }
        .message-user {
          align-self: flex-end;
        }
        .message-assistant {
          align-self: flex-start;
        }
        .message-content {
          padding: 12px 16px;
          border-radius: 12px;
          word-wrap: break-word;
          line-height: 1.5;
        }
        .message-user .message-content {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom-right-radius: 4px;
        }
        .message-assistant .message-content {
          background: #f0f0f0;
          color: #333;
          border-bottom-left-radius: 4px;
        }
        .message-time {
          font-size: 11px;
          color: #999;
          margin-top: 4px;
          padding: 0 4px;
        }
        .message-user .message-time {
          text-align: right;
        }
        .typing-indicator {
          display: flex;
          gap: 4px;
          padding: 12px 16px;
        }
        .typing-indicator span {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #999;
          animation: typing 1.4s infinite;
        }
        .typing-indicator span:nth-child(2) {
          animation-delay: 0.2s;
        }
        .typing-indicator span:nth-child(3) {
          animation-delay: 0.4s;
        }
        @keyframes typing {
          0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
          }
          30% {
            transform: translateY(-10px);
            opacity: 1;
          }
        }
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  )
}

