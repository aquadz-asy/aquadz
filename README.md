# aquadz.com

The AQuadZ LLC website: a static one-page site plus a privacy page. It uses plain HTML and CSS, with no build step, no cookies, no analytics and nothing loaded from other websites (the Roboto Flex font is served from this site).

| File | What it is |
|---|---|
| `index.html` | Home: services, how it works, industries, approach, FAQ, contact |
| `privacy.html` | Privacy notice |
| `styles.css` | Styles (light and dark follow the visitor's system setting) |
| `favicon.svg` | Square logo for the browser tab |
| `brand/index.html` | Brand page: the animated logo, the logo with the name, small sizes, colours (not linked from the site; `noindex`) |
| `brand/logo-mark.svg`, `brand/logo-mark-animated.svg` | Still and animated logo |
| `brand/make_logo.py` | Generates every logo file and the logos inside the pages: run `python3 brand/make_logo.py` after changing the logo |
| `CNAME` | Custom domain for GitHub Pages |
| `fonts/` | Roboto Flex (Material 3's typeface), self-hosted, with its open font licence (OFL-1.1) |

## Preview locally

```bash
python3 -m http.server 8080
```

Then open http://localhost:8080.

## Publish

The repository is private and the GitHub account is on the free plan, which can't serve GitHub Pages from a private repository. There are two options.

### Option A: GitHub Pages (simplest; the repository becomes public)

A website is public anyway, so a public repository exposes nothing extra. Keep secrets out of it.

1. GitHub → repository Settings → General → Change visibility → Public.
2. Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. At your domain registrar, add these DNS records for `aquadz.com`:
   - `A` records to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`;
   - a `CNAME` record for `www` to `aquadz-asy.github.io`.
4. Back in Settings → Pages, once the DNS check passes, tick **Enforce HTTPS**.

### Option B: Cloudflare Pages (the repository stays private; free)

1. Create a free Cloudflare account and add the site `aquadz.com`. Cloudflare shows two nameservers; set them at your registrar. Before switching, copy the existing **MX, SPF, DKIM and DMARC** records for Google Workspace into Cloudflare, so mail keeps working.
2. Workers & Pages → Create → Pages → Connect to Git → `aquadz-asy/aquadz`. Framework preset: None; build command empty; output directory `/`.
3. Custom domains → add `aquadz.com` and `www.aquadz.com`.
4. Delete the `CNAME` file (it's only for GitHub Pages).

## Email checks (Google Workspace on asy@aquadz.com)

The mail itself is set up already. Check these DNS records, because they decide whether your invoices and quotes land in inboxes or in spam:

- **MX:** `smtp.google.com` (priority 1).
- **SPF:** a TXT record on `aquadz.com` of `v=spf1 include:_spf.google.com ~all` (exactly one SPF record).
- **DKIM:** Google Admin → Apps → Google Workspace → Gmail → Authenticate email → generate the key → add the TXT record `google._domainkey` → click **Start authentication**.
- **DMARC:** a TXT record on `_dmarc.aquadz.com`: start with `v=DMARC1; p=none; rua=mailto:asy@aquadz.com`, then move to `p=quarantine` after a few weeks of clean reports.

Send a test mail to a Gmail address and open "Show original": SPF, DKIM and DMARC should all say PASS.

## Before you publish

- The site uses no customer data. The hero examples are made up: "Northwind Trading" (a classic sample-company name), products A-120, B-310, C-045, and the WhatsApp and phone-call snippets. Add a case study only after a customer agrees to it in writing.
- The clinic app is described as a pilot in India; no clinic is named.
- Add a partner logo or name (for example a reseller partnership) only if the partner agreement allows it.
