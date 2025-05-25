import { useState } from 'react'
import useCollab from './api/useCollab'
import { useI18n } from './i18n'

export default function Collab({ onBack }: { onBack: () => void }) {
  const { t } = useI18n()
  const [room, setRoom] = useState('default')
  const [text, setText] = useState('')
  const { messages, send } = useCollab(room)

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t('collaboration')}</h1>
      <div className="mb-2">
        <label className="mr-2">{t('room')}</label>
        <input
          className="border rounded px-2 py-1"
          value={room}
          onChange={(e) => setRoom(e.target.value)}
        />
      </div>
      <div className="border h-40 overflow-y-auto mb-2 p-1" aria-label="messages">
        {messages.map((m, i) => (
          <div key={i}>{m.text}</div>
        ))}
      </div>
      <div className="flex space-x-2">
        <input
          className="border flex-1 rounded px-2 py-1"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-3 py-1 rounded"
          onClick={() => {
            send(text)
            setText('')
          }}
          aria-label="send"
        >
          {t('send')}
        </button>
      </div>
      <button className="mt-6 text-blue-600 underline" onClick={onBack} aria-label="back">
        {t('back')}
      </button>
    </main>
  )
}
