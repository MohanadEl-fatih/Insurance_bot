'use client'

import { useState, KeyboardEvent } from 'react'

interface ComposerProps {
  onSend: (message: string) => void
  disabled: boolean
}

export default function Composer({ onSend, disabled }: ComposerProps) {
  const [input, setInput] = useState('')

  const handleSubmit = () => {
    if (input.trim() && !disabled) {
      onSend(input)
      setInput('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="composer">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message... (Press Enter to send)"
        disabled={disabled}
        rows={1}
        style={{
          resize: 'none',
          minHeight: '50px',
          maxHeight: '120px',
        }}
      />
      <button onClick={handleSubmit} disabled={disabled || !input.trim()}>
        Send
      </button>
      <style jsx>{`
        .composer {
          padding: 16px;
          border-top: 1px solid #e0e0e0;
          display: flex;
          gap: 12px;
          align-items: flex-end;
        }
        textarea {
          flex: 1;
          padding: 12px;
          border: 1px solid #ddd;
          border-radius: 8px;
          font-family: inherit;
          font-size: 14px;
          outline: none;
          transition: border-color 0.2s;
        }
        textarea:focus {
          border-color: #667eea;
        }
        textarea:disabled {
          background: #f5f5f5;
          cursor: not-allowed;
        }
        button {
          padding: 12px 24px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: opacity 0.2s, transform 0.1s;
        }
        button:hover:not(:disabled) {
          opacity: 0.9;
          transform: translateY(-1px);
        }
        button:active:not(:disabled) {
          transform: translateY(0);
        }
        button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  )
}

