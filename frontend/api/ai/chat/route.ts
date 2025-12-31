import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  try {
    const body = await req.json()

    // You host your AI agent here (FastAPI recommended)
    // Example: http://localhost:8000/chat
    const base = process.env.AI_BACKEND_URL
    if (!base) {
      return NextResponse.json(
        { reply: 'AI_BACKEND_URL is not set in environment.' },
        { status: 500 }
      )
    }

    const upstream = await fetch(`${base}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })

    if (!upstream.ok) {
      const text = await upstream.text()
      return NextResponse.json({ reply: `Model backend error: ${text}` }, { status: 502 })
    }

    const data = await upstream.json()
    // expected: { reply: "..." }
    return NextResponse.json({ reply: data.reply ?? 'No reply from model.' })
  } catch (e: any) {
    return NextResponse.json({ reply: `Route error: ${e?.message ?? 'unknown'}` }, { status: 500 })
  }
}
