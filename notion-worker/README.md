# UHF Notion Import Worker

Cloudflare Worker that lets the Ideation Framework page (hosted on GitHub Pages)
create cards in the shared Notion content calendar without exposing the Notion
token in client-side code. Anyone on any computer who opens the GitHub-hosted
HTML can click **Import to Notion** — the Worker is the single shared backend.

## One-time setup

### 1. Create a Notion internal integration
1. Go to https://www.notion.so/profile/integrations → **+ New integration**.
2. Name: `UHF Ideation Import`. Associated workspace: Faraz's workspace.
3. Type: **Internal**. Capabilities: Read, Update, Insert content.
4. Copy the **Internal Integration Secret** (looks like `ntn_...` or `secret_...`).
5. Open the content calendar database in Notion → **⋯** menu → **Connections** →
   add **UHF Ideation Import**. Without this step the Worker will get a 404.

### 2. Add the missing properties to the database
Open the test card and ensure these properties exist with these exact names + types:

| Property name      | Type           | Notes                                           |
|--------------------|----------------|-------------------------------------------------|
| Title              | Title          | (Notion's default title column)                 |
| Status             | Status         | Must have a `Content Ideas` option              |
| Topic              | Text           |                                                 |
| Topic Categories   | Multi-select   | Options are created on the fly                  |
| Idea/Concept       | Text           |                                                 |
| 70/20/10 Rule      | Select         | Options: `Proven (70%)`, `Iteration (20%)`, `Experimental (10%)` |
| CCN Considered?    | Checkbox       |                                                 |
| Notes              | Text           |                                                 |
| Pre-Validated?     | URL            |                                                 |
| TAM                | Number         |                                                 |
| Format             | Multi-select   |                                                 |
| Recording Style    | Multi-select   |                                                 |

Property names are case-sensitive and must match exactly. If you rename anything,
update the matching key in `worker.js`.

### 3. Deploy the Worker
Install Wrangler once: `npm install -g wrangler` then `wrangler login`.

From `notion-worker/`:

```bash
wrangler secret put NOTION_TOKEN     # paste the integration secret when prompted
wrangler deploy
```

Wrangler prints the deployed URL, e.g.
`https://uhf-notion-import.scott-uhf.workers.dev`.

### 4. Wire the URL into the HTML
Edit `ideation-framework.html`, find:

```js
const NOTION_WORKER_URL = 'https://uhf-notion-import.YOUR-SUBDOMAIN.workers.dev';
```

Replace it with the URL Wrangler printed. Commit and push to GitHub.

### 5. (Optional) Lock down the origin
Once the GitHub Pages URL is known, edit `wrangler.toml`:

```toml
ALLOWED_ORIGIN = "https://scottuhf.github.io"
```

Run `wrangler deploy` again. The Worker will then refuse browser calls from any
other origin.

## How it works for other users
There's nothing to install. Anyone who opens the GitHub Pages URL — on any
computer, any browser — gets the same `Import to Notion` button. They all hit
the same Worker, which uses the one shared integration token to write to the
shared database. As long as the integration is connected to the database
(step 1.5), every teammate's import lands in the same content calendar.

## Updating the Worker later
Edit `worker.js`, then `wrangler deploy`. No GitHub Pages redeploy needed —
the static page just calls the same Worker URL.
