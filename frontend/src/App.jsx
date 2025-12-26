import { useState } from "react";

export default function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    if (!image) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("image", image);

    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    // TEMP mock until real ML output arrives
    const enriched = {
      ...data,
      verdict:
        data.visual_blur_ok && data.batch_id_valid
          ? "LEGALLY AUTHENTIC"
          : "SUSPICIOUS",
      reasons: [
        ...(data.visual_blur_ok ? [] : ["Packaging appears blurred or tampered"]),
        ...(data.batch_id_valid ? [] : ["Batch ID missing or inconsistent"])
      ]
    };

    setResult(enriched);
    setLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#020617]">
      <div className="w-110 rounded-2xl border border-slate-800 bg-[#020617] p-10 shadow-2xl">
        <h1 className="text-3xl font-semibold text-sky-400 text-center">
          TrueMed
        </h1>
        <p className="text-sm text-slate-400 text-center mt-2 mb-8">
          AI-powered medicine authenticity verification
        </p>

        <input
          type="file"
          accept="image/*"
          id="upload"
          className="hidden"
          onChange={(e) => setImage(e.target.files[0])}
        />

        <label
          htmlFor="upload"
          className="block cursor-pointer rounded-lg border border-dashed border-sky-400 px-4 py-3 text-center text-sm text-sky-400 hover:bg-sky-400/10 transition"
        >
          {image ? "Change Image" : "Upload Medicine Image"}
        </label>

        {image && (
          <p className="mt-2 text-xs text-slate-300 text-center">
            {image.name}
          </p>
        )}

        <button
          onClick={analyze}
          disabled={!image || loading}
          className="mt-6 w-full rounded-xl bg-sky-400 py-3 font-semibold text-[#020617]
                     disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {loading ? "Analyzing…" : "Analyze Authenticity"}
        </button>

        {/* RESULTS */}
        {result && (
          <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900/40 p-5">
            <p className="text-center text-lg font-semibold">
              Verdict:{" "}
              <span
                className={
                  result.verdict === "LEGALLY AUTHENTIC"
                    ? "text-emerald-400"
                    : "text-rose-400"
                }
              >
                {result.verdict}
              </span>
            </p>

            <p className="text-center text-sm text-slate-400 mt-1">
              Confidence: {result.confidence}%
            </p>

            {result.reasons.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-medium text-slate-300 mb-2">
                  Detected Issues:
                </p>
                <ul className="space-y-2">
                  {result.reasons.map((r, i) => (
                    <li
                      key={i}
                      className="text-xs text-amber-300 bg-amber-500/10 rounded-md px-3 py-2"
                    >
                      {r}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        <p className="mt-6 text-[11px] text-slate-500 text-center">
          Secure • Private • Medical-grade AI
        </p>
      </div>
    </div>
  );
}
