import { useEffect, useRef, useState } from 'react'
import { addPendingEdit, PendingEdit } from '../lib/db'
import { processPendingEdits } from '../lib/collabQueue'

const COLLAB_URL = import.meta.env.VITE_COLLAB_URL ?? `ws://${location.host}`

export interface CollabMessage {
  id: string
  text: string
}

export default function useCollab(room: string) {
  const [messages, setMessages] = useState<CollabMessage[]>([])
  const wsRef = useRef<WebSocket | null>(null)
  const clientIdRef = useRef<string>(() => {
    const stored = localStorage.getItem('collab_id')
    if (stored) return stored
    const id = Math.random().toString(36).slice(2)
    localStorage.setItem('collab_id', id)
    return id
  }) as React.MutableRefObject<string>

  useEffect(() => {
    function connect() {
      const ws = new WebSocket(`${COLLAB_URL}/ws/${room}`)
      wsRef.current = ws
      ws.onopen = () => {
        processPendingEdits((e) => ws.send(e.data))
      }
      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data) as CollabMessage
          setMessages((m) => [...m, msg])
          if (
            msg.id !== clientIdRef.current &&
            Notification.permission === 'granted'
          ) {
            new Notification('Lego GPT', { body: msg.text })
          }
        } catch {
          // ignore malformed
        }
      }
    }
    connect()
    window.addEventListener('online', connect)
    return () => {
      window.removeEventListener('online', connect)
      wsRef.current?.close()
    }
  }, [room])

  async function send(text: string) {
    const payload = JSON.stringify({ id: clientIdRef.current, text })
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(payload)
    } else {
      const edit: PendingEdit = { room, data: payload }
      await addPendingEdit(edit)
    }
  }

  return { messages, send }
}
