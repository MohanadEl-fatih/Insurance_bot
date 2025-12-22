'use client'

import { useState, useRef, useEffect } from 'react'
import MessageList from './MessageList'
import Composer from './Composer'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: content.trim() }),
        credentials: 'include', // Include cookies for session
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.message || 'I apologize, but I could not generate a response.',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h1>Insurance Quote Assistant</h1>
        <p>Ask me about insurance quotes for your vehicle</p>
      </div>
      <MessageList messages={messages} isLoading={isLoading} />
      <div ref={messagesEndRef} />
      <Composer onSend={handleSendMessage} disabled={isLoading} />
      <style jsx>{`
        .chat-window {
          width: 100%;
          max-width: 800px;
          height: 90vh;
          max-height: 800px;
          background: white;
          border-radius: 16px;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }
        .chat-header {
          padding: 24px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          text-align: center;
        }
        .chat-header h1 {
          font-size: 24px;
          margin-bottom: 8px;
        }
        .chat-header p {
          font-size: 14px;
          opacity: 0.9;
        }
      `}</style>
    </div>
  )
}

