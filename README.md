# johncole.dev

Personal professional website for John Cole — software engineering, teaching interests, Human-Directed Software Engineering (HDSE), and independent products.

Built with Astro (static output) and deployed to Cloudflare Workers.

## Requirements

- Node.js 22 or later
- npm
- Git
- Cloudflare account for deployment

## Run locally

```bash
npm install
npm run dev
```

Open http://localhost:4321.

Useful commands:

```bash
npm run build      # production build → dist/
npm run preview    # serve the production build
npm run deploy     # build + wrangler deploy
```

For background Astro development, see `AGENTS.md`.

## Site structure

| Route | Purpose |
|---|---|
| `/` | Homepage |
| `/work` | Client/professional work and independent products |
| `/teaching` | Teaching philosophy, instructional areas, sample lessons |
| `/teaching/lessons/...` | Full sample lessons with downloadable materials |
| `/hdse` | Human-Directed Software Engineering methodology |
| `/about` | Biography and contact |

### Sample lessons

1. `/teaching/lessons/functions-and-testing/` — Functions, Decomposition, and Testing (introductory Python)
2. `/teaching/lessons/modeling-an-application/` — Modeling a Real-World Application (SQL / SQLite)
3. `/teaching/lessons/evaluating-ai-code/` — Evaluating AI-Generated Code (verification and judgment)

Supporting files live under `public/teaching/lessons/`.

## Project layout

```
src/
  pages/                 # Routes (Astro pages)
  layouts/               # Base.astro, LessonLayout.astro
  components/lessons/    # Shared lesson UI
  data/lessons.ts        # Lesson metadata / navigation
  styles/global.css      # Design tokens, typography, responsive layout
public/
  favicon.svg / .ico
  teaching/lessons/      # Downloadable lesson assets
```

Primary content and design files:

- `src/pages/index.astro` — homepage
- `src/pages/work.astro` — project portfolio (client names anonymized)
- `src/pages/teaching.astro` — teaching overview
- `src/pages/hdse.astro` — HDSE methodology
- `src/pages/about.astro` — about
- `src/styles/global.css` — visual system

## Deploy

```bash
npm run build
npx wrangler login
npx wrangler deploy
```

Or connect this repository in Cloudflare Workers with:

- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`

## Privacy and content review

- No contact form, analytics, private documents, or public resume PDFs by default
- Do not commit academic transcripts or other sensitive personal information
- Client/company identities in portfolio content must remain anonymized
- Review public claims (degrees, project descriptions, teaching experience) before deploying

## Notes

Visual QA helpers (optional): `scripts/visual-qa.mjs` uses Playwright against a local preview server. Screenshots land in `tmp/` (gitignored).
