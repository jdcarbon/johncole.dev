# johncole.dev

Personal professional website for John Cole, built with Astro and deployed as static assets to Cloudflare Workers.

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

## Deploy

```bash
npm run build
npx wrangler login
npx wrangler deploy
```

Alternatively, connect this GitHub repository in Cloudflare Workers and set build command to `npm run build` and deploy command to `npx wrangler deploy`.

## First edits

- `src/pages/index.astro`: homepage introduction
- `src/pages/work.astro`: project summaries
- `src/pages/teaching.astro`: education and teaching interests
- `src/pages/hdse.astro`: HDSE overview
- `src/styles/global.css`: visual design

No contact form, analytics, private documents, or public resume PDFs are included by default. Do not commit academic transcripts or personal information to the public repo.

## Notes

Content is a first draft based on the user's supplied resume and project descriptions. Review all public claims and project confidentiality before deploying.
