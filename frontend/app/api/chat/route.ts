import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { message } = body

    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      )
    }

    // Get session ID from cookie if present
    const sid = request.cookies.get('sid')?.value

    // Forward request to backend
    const response = await fetch(`${BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(sid && { Cookie: `sid=${sid}` }),
      },
      credentials: 'include', // Include cookies in request
      body: JSON.stringify({ message, sid }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`Backend error: ${response.status} - ${errorText}`)
    }

    const data = await response.json()

    // Create response and forward session cookie if set by backend
    const nextResponse = NextResponse.json(data)
    
    // Forward set-cookie header from backend
    const setCookieHeader = response.headers.get('set-cookie')
    if (setCookieHeader) {
      nextResponse.headers.set('set-cookie', setCookieHeader)
    }

    return nextResponse
  } catch (error) {
    console.error('Error proxying chat request:', error)
    return NextResponse.json(
      { 
        error: 'Failed to process chat request',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}

