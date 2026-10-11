// Proxies the Voice Agents signed-URL request so SAMVAAD_API_KEY never reaches the browser.
// Set SAMVAAD_API_KEY in Netlify → Site configuration → Environment variables.
const ALLOWED = /^\/api\/(orgs\/[\w-]+\/workspaces\/[\w-]+\/apps\/[\w-]+\/url)$/;

export default async (req) => {
  const url = new URL(req.url);
  const m = url.pathname.match(ALLOWED);
  if (req.method !== "GET" || !m) return new Response("Not found", { status: 404 });
  const r = await fetch(`https://apps.sarvam.ai/api/app-runtime/${m[1]}${url.search}`, {
    headers: { "X-API-Key": process.env.SAMVAAD_API_KEY },
  });
  return new Response(await r.text(), { status: r.status, headers: { "Content-Type": "application/json" } });
};

export const config = { path: "/api/*" };
