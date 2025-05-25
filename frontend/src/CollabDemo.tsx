import { useState, useEffect } from "react";
import { useI18n } from "./i18n";
import { queueCollab, processCollabQueue } from "./lib/collabQueue";

interface Props {
  onBack: () => void;
}

export default function CollabDemo({ onBack }: Props) {
  const { t } = useI18n();
  const [room, setRoom] = useState("");
  const [message, setMessage] = useState("");
  const [log, setLog] = useState<string[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    if (!room) return;
    const socket = new WebSocket(`ws://${location.host}/ws/${room}`);
    socket.onopen = () => {
      processCollabQueue((r, d) => {
        if (r === room) socket.send(d);
      });
    };
    socket.onmessage = (ev) => {
      setLog((l) => [...l, ev.data]);
      if (navigator.serviceWorker.controller) {
        navigator.serviceWorker.controller.postMessage({
          type: "collab_update",
          body: ev.data,
        });
      }
    };
    setWs(socket);
    return () => socket.close();
  }, [room]);

  async function send() {
    if (!message) return;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(message);
    } else if (room) {
      await queueCollab({ room, data: message });
    }
    setLog((l) => [...l, `You: ${message}`]);
    setMessage("");
  }

  if (!room) {
    return (
      <main className="p-6 max-w-xl mx-auto font-sans">
        <h1 className="text-2xl font-bold mb-4">{t("collabDemo")}</h1>
        <label className="block mb-2">
          {t("roomId")}
          <input
            className="border rounded w-full px-2 py-1"
            value={room}
            onChange={(e) => setRoom(e.target.value)}
          />
        </label>
        <button
          className="bg-blue-600 text-white px-3 py-1 rounded"
          onClick={() => setRoom(room.trim())}
        >
          {t("send")}
        </button>
        <button className="ml-4 underline" onClick={onBack} aria-label="back">
          {t("back")}
        </button>
      </main>
    );
  }

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">{t("collabDemo")}</h1>
      <div className="mb-4">
        <input
          className="border rounded w-full px-2 py-1"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-3 py-1 rounded mt-2"
          onClick={send}
        >
          {t("send")}
        </button>
      </div>
      <ul className="border p-2 h-40 overflow-auto mb-4">
        {log.map((m, i) => (
          <li key={i}>{m}</li>
        ))}
      </ul>
      <button className="underline" onClick={onBack} aria-label="back">
        {t("back")}
      </button>
    </main>
  );
}
