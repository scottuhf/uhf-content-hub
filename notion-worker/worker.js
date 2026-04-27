// Cloudflare Worker — Ideation Framework → Notion proxy
// Holds the Notion integration token as a secret so the static GitHub Pages site
// can create pages in the shared content calendar without exposing credentials.
//
// Required secrets / vars (set via `wrangler secret put` or the Cloudflare dashboard):
//   NOTION_TOKEN  — secret. The internal integration token (starts with `secret_` or `ntn_`).
//   DATABASE_ID   — var.    The content calendar database ID.
//   ALLOWED_ORIGIN — var.   Optional. The origin allowed to call this worker
//                           (e.g. https://USER.github.io). Defaults to "*".
//
// Notion property names must match the database exactly:
//   Title, Status, Topic, Topic Categories, Idea/Concept, 70/20/10 Rule,
//   CCN Considered?, Notes, Pre-Validated?, TAM, Format, Recording Style

const NOTION_VERSION = '2022-06-28';

export default {
  async fetch(request, env) {
    const origin = env.ALLOWED_ORIGIN || '*';
    const cors = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }
    if (request.method !== 'POST') {
      return json({ error: 'Method not allowed' }, 405, cors);
    }
    if (!env.NOTION_TOKEN || !env.DATABASE_ID) {
      return json({ error: 'Worker missing NOTION_TOKEN or DATABASE_ID' }, 500, cors);
    }

    let body;
    try { body = await request.json(); }
    catch { return json({ error: 'Invalid JSON' }, 400, cors); }

    const properties = {
      // Title — page name
      'Title': { title: [{ text: { content: body.title || 'Untitled' } }] },

      // Status — auto-set so it lands in the Content Ideas group
      'Status': { status: { name: 'Content Ideas' } },

      // Step 1
      'Topic': richText(body.topic),
      'Topic Categories': multiSelect(body.topicCategories),

      // Step 2 — Idea
      'Idea/Concept': richText(body.idea),
      '70/20/10 Rule': body.contentMix ? { select: { name: body.contentMix } } : { select: null },
      'CCN Considered?': { checkbox: !!body.ccnConsidered },
      'Notes': richText(body.notes),
      'Pre-Validated?': { url: body.preValidatedUrl || null },
      'TAM': { number: body.tam ?? null },

      // Step 2 — Format
      'Format': multiSelect(body.format),

      // Step 3 — Recording
      'Recording Style': multiSelect(body.recordingStyle),
    };

    const res = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.NOTION_TOKEN}`,
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        parent: { database_id: env.DATABASE_ID },
        properties,
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      return json({ error: data.message || 'Notion API error', details: data }, res.status, cors);
    }
    return json({ ok: true, id: data.id, url: data.url }, 200, cors);
  },
};

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors },
  });
}

function richText(value) {
  const text = (value || '').toString();
  return { rich_text: text ? [{ text: { content: text.slice(0, 2000) } }] : [] };
}

function multiSelect(arr) {
  const items = (arr || [])
    .map(v => (v || '').toString().trim())
    .filter(Boolean)
    .map(name => ({ name: name.replace(/,/g, ' ') })); // commas not allowed in select names
  return { multi_select: items };
}
