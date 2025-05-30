import { useState, useEffect } from "react";
import type { FormEvent, ChangeEvent } from "react";
import { useI18n } from "./i18n";
import Examples from "./Examples";

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed"; platform: string }>;
}
import useGenerate from "./api/useGenerate";
import useDetectInventory from "./api/useDetectInventory";
import LDrawViewer from "./LDrawViewer";
import Settings from "./Settings";
import { processPending } from "./lib/offlineQueue";
import { processDetectQueue } from "./lib/detectQueue";
import CollabDemo from "./CollabDemo";
import Moderation from "./Moderation";
import Analytics from "./Analytics";
import Reports from "./Reports";
import Tutorial from "./Tutorial";
import ImportExamples from "./ImportExamples";

export default function App() {
  const { t } = useI18n();
  const [page, setPage] = useState<
    | "main"
    | "settings"
    | "examples"
    | "collab"
    | "moderation"
    | "analytics"
    | "reports"
    | "import"
  >("main");
  const [prompt, setPrompt] = useState("");
  const [seed, setSeed] = useState("");
  const [photo, setPhoto] = useState<string | null>(null);
  const [inventory, setInventory] = useState<Record<string, number> | null>(null);
  const [request, setRequest] = useState<{ p: string; s: number | null } | null>(
    null
  );
  const [installEvent, setInstallEvent] = useState<BeforeInstallPromptEvent | null>(null);
  const [showInstall, setShowInstall] = useState(false);
  const [showPush, setShowPush] = useState(false);
  const [showTutorial, setShowTutorial] = useState(
    () => !localStorage.getItem("tutorialSeen")
  );

  const detect = useDetectInventory(photo);

  useEffect(() => {
    function handleOnline() {
      processPending();
      processDetectQueue();
    }
    processPending();
    processDetectQueue();
    window.addEventListener("online", handleOnline);
    return () => window.removeEventListener("online", handleOnline);
  }, []);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setInstallEvent(e as BeforeInstallPromptEvent);
      setShowInstall(true);
    };
    window.addEventListener("beforeinstallprompt", handler);
    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);

  useEffect(() => {
    if (
      "Notification" in window &&
      Notification.permission === "default" &&
      !localStorage.getItem("pushPrompted")
    ) {
      setShowPush(true);
    }
  }, []);

  useEffect(() => {
    if (detect.data) {
      setInventory(detect.data.brick_counts);
    }
  }, [detect.data]);

  const { data, loading, error } = useGenerate(
    request?.p ?? null,
    request?.s ?? null,
    inventory
  );

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setRequest({ p: prompt, s: seed ? Number(seed) : null });
  }

  function handleFile(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onloadend = () => {
      const result = reader.result as string;
      const b64 = result.split(",", 2)[1] ?? result;
      setPhoto(b64);
    };
    reader.readAsDataURL(file);
  }

  function handleInstall() {
    if (!installEvent) return;
    installEvent.prompt();
    installEvent.userChoice.finally(() => {
      setShowInstall(false);
      setInstallEvent(null);
    });
  }

  function handlePushAccept() {
    Notification.requestPermission().finally(() => {
      localStorage.setItem("pushPrompted", "1");
      setShowPush(false);
    });
  }

  if (page === "settings") {
    return <Settings onBack={() => setPage("main")} />;
  }

  if (page === "examples") {
    return (
      <Examples
        onBack={() => setPage("main")}
        onSelect={(p) => setPrompt(p)}
      />
    );
  }

  if (page === "collab") {
    return <CollabDemo onBack={() => setPage("main")} />;
  }

  if (page === "moderation") {
    return <Moderation onBack={() => setPage("main")} />;
  }

  if (page === "analytics") {
    return <Analytics onBack={() => setPage("main")} />;
  }

  if (page === "reports") {
    return <Reports onBack={() => setPage("main")} />;
  }

  if (page === "import") {
    return <ImportExamples onBack={() => setPage("main")} />;
  }

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      {showTutorial && (
        <Tutorial
          onClose={() => {
            localStorage.setItem("tutorialSeen", "1");
            setShowTutorial(false);
          }}
        />
      )}
      <h1 className="text-2xl font-bold mb-4">{t("title")}</h1>
      {showInstall && (
        <button
          onClick={handleInstall}
          aria-label="install"
          className="mb-4 mr-4 bg-green-600 text-white px-3 py-1 rounded"
        >
          {t("installApp")}
        </button>
      )}
      {showPush && (
        <button
          onClick={handlePushAccept}
          aria-label="enable push"
          className="mb-4 mr-4 bg-blue-600 text-white px-3 py-1 rounded"
        >
          Enable Notifications
        </button>
      )}
      <button
        className="text-sm underline mb-4"
        onClick={() => setPage("settings")}
        aria-label="settings"
      >
        {t("settings")}
      </button>
      <button
        className="text-sm underline mb-4 ml-4"
        onClick={() => setPage("examples")}
        aria-label="examples"
      >
        {t("examples")}
      </button>
      <button
        className="text-sm underline mb-4 ml-4"
        onClick={() => setPage("collab")}
        aria-label="collaboration demo"
      >
        {t("collabDemo")}
      </button>
      <button
        className="text-sm underline mb-4 ml-4"
        onClick={() => setPage("moderation")}
        aria-label="moderation"
      >
        {t("moderation")}
      </button>
      <button
        className="text-sm underline mb-4 ml-4"
        onClick={() => setPage("analytics")}
        aria-label="analytics"
      >
        Analytics
      </button>
      <button
        className="text-sm underline mb-4 ml-4"
        onClick={() => setPage("reports")}
        aria-label="reports"
      >
        {t("reports")}
      </button>
      <button
        className="text-sm underline mb-4 ml-4"
        onClick={() => setPage("import")}
        aria-label="import examples"
      >
        {t("importExamples")}
      </button>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-semibold mb-1">{t("prompt")}</label>
          <input
            className="w-full border rounded px-2 py-1"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block font-semibold mb-1">{t("seedOptional")}</label>
          <input
            className="w-full border rounded px-2 py-1"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            type="number"
            min="0"
          />
        </div>

        <div>
          <label className="block font-semibold mb-1">{t("inventoryPhoto")}</label>
          <input type="file" accept="image/*" onChange={handleFile} aria-label="inventory photo" />
          {detect.loading && <p className="text-sm">{t("detecting")}</p>}
          {detect.error && (
            <p className="text-red-600 text-sm" role="alert">{detect.error}</p>
          )}
        </div>

        {inventory && (
          <div className="mt-2 text-sm">
            <p className="font-semibold">{t("detectedInventory")}</p>
            <ul className="list-disc list-inside">
              {Object.entries(inventory).map(([part, qty]) => (
                <li key={part}>
                  {part}: {qty}
                </li>
              ))}
            </ul>
          </div>
        )}

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={loading}
        >
          {loading ? t("generating") : t("generate")}
        </button>
      </form>

      {error && (
        <p className="mt-4 text-red-600" role="alert">{error}</p>
      )}

      {data?.png_url && !loading && (
        <>
          <img
            src={data.png_url}
            alt="Lego preview"
            className="mt-6 w-full h-auto border"
          />
          {data.ldr_url && (
            <div className="mt-6">
              <LDrawViewer url={data.ldr_url} />
            </div>
          )}
          {data.gltf_url && (
            <div className="mt-4">
              <a
                href={data.gltf_url}
                rel="ar"
                className="text-blue-600 underline"
              >
                {t("viewInAR")}
              </a>
            </div>
          )}
          {data.instructions_url && (
            <div className="mt-2">
              <a href={data.instructions_url} className="text-blue-600 underline">
                PDF Instructions
              </a>
            </div>
          )}
          <div className="mt-2">
            <button
              onClick={() => {
                if (navigator.share) {
                  navigator.share({ title: "Lego build", url: data.png_url });
                } else {
                  window.open(
                    `https://twitter.com/intent/tweet?url=${encodeURIComponent(data.png_url)}`,
                    "_blank"
                  );
                }
              }}
              className="text-blue-600 underline"
              aria-label="share build"
            >
              Share
            </button>
          </div>
        </>
      )}
    </main>
  );
}
