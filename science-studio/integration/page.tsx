"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api/client";

type Project = { id: string; topic: string; profile: string; preview: boolean; job: { status: string; action?: string; result?: unknown } };
const checks = ["science", "visual", "voice", "subtitles", "rights"] as const;
const labels: Record<string, string> = { science: "Fontes e afirmações científicas", visual: "Arte, camadas e movimentos", voice: "Voz PT-BR e pronúncia", subtitles: "Legendas e sincronização", rights: "Licenças e direitos" };

export default function ScienceStudioPage() {
  const [topic, setTopic] = useState("");
  const [profile, setProfile] = useState("short");
  const [projects, setProjects] = useState<Project[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [review, setReview] = useState<string[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [configured, setConfigured] = useState(false);
  async function refresh() {
    try {
      const [data, capability] = await Promise.all([
        api<{ projects: Project[] }>("/api/science-studio/projects"),
        api<{ provider_configured: boolean }>("/api/science-studio/capabilities"),
      ]);
      setProjects(data.projects);
      setConfigured(capability.provider_configured);
      setError("");
    } catch (e) { setError(e instanceof Error ? e.message : "Falha ao consultar projetos"); }
  }
  useEffect(() => { void refresh(); const timer = setInterval(() => void refresh(), 5000); return () => clearInterval(timer); }, []);
  const current = projects.find((p) => p.id === selected);
  async function create() {
    setBusy(true); setError("");
    try {
      const item = await api<{ id: string }>("/api/science-studio/projects", { method: "POST", body: { topic, profile } });
      setSelected(item.id); setReview([]); await refresh();
    } catch (e) { setError(e instanceof Error ? e.message : "Falha ao criar projeto"); }
    finally { setBusy(false); }
  }
  async function action(name: string) {
    if (!current) return;
    setBusy(true); setError("");
    try {
      await api(`/api/science-studio/projects/${current.id}/jobs`, { method: "POST", body: { action: name, checks: name === "review" ? review : [] } });
      if (name === "generate" || name === "render") setReview([]);
      await refresh();
    } catch (e) { setError(e instanceof Error ? e.message : "Falha na produção"); }
    finally { setBusy(false); }
  }
  const working = busy || current?.job.status === "queued" || current?.job.status === "running";
  const approved = current?.job.action === "review" && current?.job.status === "done";
  const control = "rounded-lg border border-white/20 bg-zinc-900 p-3 text-white disabled:opacity-40";
  return <main className="mx-auto max-w-5xl space-y-6 p-6">
    <header><p className="text-sm text-zinc-400">Science Studio AI · v0.2</p><h1 className="text-3xl font-semibold">Ciência em movimento</h1><p className="mt-2 text-zinc-400">Motion Comic, narração documental masculina em PT-BR e revisão antes da entrega.</p></header>
    {!configured && <p role="status" className="rounded-lg border border-amber-500/40 p-4">A geração automática aguarda a configuração dos motores locais. Você pode criar e preparar seu projeto.</p>}
    <form className="grid gap-3" onSubmit={(e) => { e.preventDefault(); void create(); }}>
      <label htmlFor="science-topic">Qual história a ciência vai contar?</label>
      <input id="science-topic" className={control} value={topic} onChange={(e) => setTopic(e.target.value)} minLength={3} maxLength={500} required placeholder="Como um buraco negro deforma a luz?" />
      <label htmlFor="science-profile">Duração e formato</label>
      <select id="science-profile" className={control} value={profile} onChange={(e) => setProfile(e.target.value)}><option value="short">60 segundos · TikTok, Shorts e Reels</option><option value="youtube">10 minutos · YouTube</option><option value="documentary">60 minutos · Documentário</option><option value="full-documentary">90 minutos · Documentário completo</option></select>
      <button className={control} disabled={busy} type="submit">Criar projeto</button>
    </form>
    {error && <p role="alert" className="text-red-300">{error}</p>}
    <section className="grid gap-5 md:grid-cols-[240px_1fr]">
      <div className="space-y-2"><h2 className="font-semibold">Projetos locais</h2>{projects.map((p) => <button key={p.id} onClick={() => { setSelected(p.id); setReview([]); }} aria-pressed={selected === p.id} className={`${control} block w-full text-left`}><span className="block">{p.topic}</span><span className="text-xs text-zinc-400">{p.profile} · {p.job.status}</span></button>)}</div>
      {current && <div className="space-y-4"><h2 className="text-xl font-semibold">{current.topic}</h2>
        <p role="status">Etapa: {current.job.action ?? "preparação"} · {current.job.status}</p>
        {current.job.status === "blocked" && <pre className="whitespace-pre-wrap text-sm text-amber-200">{JSON.stringify(current.job.result, null, 2)}</pre>}
        <div className="flex flex-wrap gap-2"><button className={control} disabled={working || !configured} onClick={() => void action("generate")}>Preparar vídeo automaticamente</button><button className={control} disabled={working} onClick={() => void action("render")}>Renderizar ativos preparados</button></div>
        {current.preview && <><video key={`${current.id}-${current.job.status}`} controls className="max-h-[580px] w-full rounded-lg bg-black" src={`/api/science-studio/projects/${current.id}/files/preview.mp4`} />
          <div className="flex gap-4 text-sm underline"><a href={`/api/science-studio/projects/${current.id}/files/project.json`} target="_blank" rel="noreferrer">Projeto e fontes</a><a href={`/api/science-studio/projects/${current.id}/files/subtitles.srt`}>Legendas</a></div>
          <fieldset className="space-y-2"><legend>Após assistir ao vídeo completo, confirme sua revisão</legend>{checks.map((check) => <label key={check} className="block"><input type="checkbox" checked={review.includes(check)} onChange={(e) => setReview((old) => e.target.checked ? [...old, check] : old.filter((v) => v !== check))} /> {labels[check]}</label>)}</fieldset>
          <button className={control} disabled={working || review.length !== 5} onClick={() => void action("review")}>Registrar minha aprovação</button>
          <button className={`${control} ml-2`} disabled={working || !approved} onClick={() => void action("export")}>Preparar entrega local</button>
          {current.job.action === "export" && current.job.status === "done" && <a className="block underline" href={`/api/science-studio/projects/${current.id}/files/final.mp4`}>Baixar vídeo final revisado</a>}
        </>}
        <p className="text-sm text-zinc-400">A entrega fica local. A publicação nas redes é uma etapa posterior.</p>
      </div>}
    </section>
  </main>;
}
