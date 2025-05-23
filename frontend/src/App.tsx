import { useState, FormEvent } from "react";
import useGenerate from "./api/useGenerate";
import LDrawViewer from "./LDrawViewer";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [seed, setSeed] = useState("");
  const [request, setRequest] = useState<{ p: string; s: number | null } | null>(
    null
  );

  const { data, loading, error } = useGenerate(
    request?.p ?? null,
    request?.s ?? null
  );

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setRequest({ p: prompt, s: seed ? Number(seed) : null });
  }

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">Lego GPT Demo</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-semibold mb-1">Prompt</label>
          <input
            className="w-full border rounded px-2 py-1"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            required
          />
        </div>

        <div>
          <label className="block font-semibold mb-1">Seed (optional)</label>
          <input
            className="w-full border rounded px-2 py-1"
            value={seed}
            onChange={(e) => setSeed(e.target.value)}
            type="number"
            min="0"
          />
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Generating…" : "Generate"}
        </button>
      </form>

      {error && <p className="mt-4 text-red-600">{error}</p>}

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
                View in AR
              </a>
            </div>
          )}
        </>
      )}
    </main>
  );
}
