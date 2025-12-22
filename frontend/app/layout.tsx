import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Insurance Quote Bot',
  description: 'Get insurance quotes through conversation',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

