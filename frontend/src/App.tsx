import { useState, useEffect, FormEvent, ChangeEvent } from "react";
import { Link } from "react-router-dom";
import useGenerate from "./api/useGenerate";
import useDetectInventory from "./api/useDetectInventory";
import LDrawViewer from "./LDrawViewer";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [seed, setSeed] = useState("");
  const [photo, setPhoto] = useState<string | null>(null);
  const [inventory, setInventory] = useState<Record<string, number> | null>(null);
  const [request, setRequest] = useState<{ p: string; s: number | null } | null>(
    null
  );

  const detect = useDetectInventory(photo);

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

  return (
    <main className="p-6 max-w-xl mx-auto font-sans">
      <h1 className="text-2xl font-bold mb-4">Lego GPT Demo</h1>
      <nav className="mb-4">
        <Link to="/settings" className="text-blue-600 underline">
          Settings
        </Link>
      </nav>

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

        <div>
          <label className="block font-semibold mb-1">Inventory Photo</label>
          <input type="file" accept="image/*" onChange={handleFile} />
          {detect.loading && <p className="text-sm">Detecting…</p>}
          {detect.error && <p className="text-red-600 text-sm">{detect.error}</p>}
        </div>

        {inventory && (
          <div className="mt-2 text-sm">
            <p className="font-semibold">Detected Inventory:</p>
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
