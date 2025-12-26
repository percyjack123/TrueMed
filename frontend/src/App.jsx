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

    const enriched = {
      ...data,
      verdict:
        data.visual_blur_ok && data.batch_id_valid
          ? "LEGALLY AUTHENTIC"
          : "SUSPICIOUS",
      reasons: [
        ...(data.visual_blur_ok ? [] : ["Blur / tampering detected in packaging"]),
        ...(data.batch_id_valid ? [] : ["Batch ID missing or inconsistent"])
      ]
    };

    setResult(enriched);
    setLoading(false);
  };

  return (
    <div className="relative min-h-screen text-slate-200 overflow-hidden">
      {/* Background */}
      <div className="ai-lab-bg" />
      <div className="ai-orb-corner" />

      {/* Foreground */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-4 py-10">
        <div className="w-full max-w-6xl">

          {/* Header */}
          <div className="text-center mb-10">
            <h1 className="text-4xl md:text-5xl font-semibold text-sky-400">
              TrueMed
            </h1>
            <p className="mt-3 text-slate-400">
              AI-powered medicine authenticity verification
            </p>
          </div>

          {/* Two Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

            {/* INPUT CARD */}
            <div className="rounded-2xl border border-slate-800 bg-black/40 backdrop-blur-xl p-8 shadow-xl">
              <p className="text-xs uppercase tracking-widest text-slate-500 mb-6">
                Input
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
                className="flex flex-col items-center justify-center rounded-xl border border-dashed border-sky-400/40 px-6 py-12 cursor-pointer transition hover:border-sky-400 hover:bg-sky-400/5"
              >
                <span className="text-sky-400 font-medium">
                  {image ? "Change image" : "Upload medicine image"}
                </span>
                <span className="mt-2 text-xs text-slate-500">
                  Clear photo of packaging
                </span>
              </label>

              {image && (
                <p className="mt-4 text-xs text-slate-400 truncate text-center">
                  {image.name}
                </p>
              )}

              <button
                onClick={analyze}
                disabled={!image || loading}
                className="mt-8 w-full rounded-xl bg-sky-400 py-4 text-lg font-semibold text-[#020617]
                           transition hover:bg-sky-300 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {loading ? "Analyzing…" : "Analyze Authenticity"}
              </button>
            </div>

            {/* OUTPUT CARD */}
            <div className="rounded-2xl border border-slate-800 bg-black/40 backdrop-blur-xl p-8 shadow-xl">
              <p className="text-xs uppercase tracking-widest text-slate-500 mb-6">
                Output
              </p>

              {!result && (
                <div className="h-full flex items-center justify-center text-slate-500 text-sm">
                  Awaiting analysis results
                </div>
              )}

              {result && (
                <div className="space-y-6">
                  <div>
                    <p className="text-lg font-semibold">
                      Verdict:
                      <span
                        className={`ml-2 ${
                          result.verdict === "LEGALLY AUTHENTIC"
                            ? "text-emerald-400"
                            : "text-rose-400"
                        }`}
                      >
                        {result.verdict}
                      </span>
                    </p>
                    <p className="text-sm text-slate-400 mt-1">
                      Confidence score: {result.confidence}%
                    </p>
                  </div>

                  {result.reasons.length > 0 ? (
                    <ul className="space-y-3">
                      {result.reasons.map((r, i) => (
                        <li
                          key={i}
                          className="rounded-lg border border-amber-500/20 bg-amber-500/10 px-4 py-3 text-xs text-amber-300"
                        >
                          {r}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-sm text-emerald-400">
                      No anomalies detected. Packaging appears authentic.
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Footer */}
          <p className="mt-12 text-center text-xs text-slate-500">
            Secure • Explainable • Medical-grade AI
          </p>
        </div>
      </div>
    </div>
  );
}
