import { useState, FormEvent } from "react";
import { generateLego } from "./api/lego";

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [seed, setSeed] = useState("");
  const [imgSrc, setImgSrc] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    setImgSrc(null);

    try {
      const res = await generateLego({
        prompt,
        seed: seed ? Number(seed) : null,
      });

      setImgSrc(res.png_url);
    } catch (err: any) {
      setError(err.message ?? "Unknown error");
    } finally {
      setLoading(false);
    }
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

      {imgSrc && !loading && (
        <img
          src={imgSrc}
          alt="Lego preview"
          className="mt-6 w-full h-auto border"
        />
      )}
    </main>
  );
}
