# Raw evidence record — Armoo/Fortune article reconstruction

Session evidence for `REPORT.md`, all gathered **2026-08-31** from the
Claude Code remote session on branch `claude/ai-wealth-generation-article-9g0q00`.
This file is the raw artifact the report cites. Quotes are short excerpts
(fair-use scale) as returned by the search tool; the full article text was
**not** captured — see "Fetch attempts" for why, and REPORT.md Bounds/A4 for
the deliberate copyright deviation from the raw-artifact convention.

## Fetch attempts (all failed — receipts)

Every direct fetch returned `EGRESS_BLOCKED` from the session's network
proxy (`"Access to <domain> is blocked by the network egress proxy"`),
2026-08-31:

| # | URL | Purpose |
|---|---|---|
| 1 | `https://fortune.com/2026/08/31/timothy-armoo-millionaire-unemployed-gen-z-ai-scarily-easy-get-rich/` | Primary article |
| 2 | `https://finance.yahoo.com/small-business/articles/31-old-millionaire-zero-sympathy-070200908.html` | Syndicated full copy |
| 3 | `https://www.cnbc.com/2024/08/30/how-a-29-year-old-became-a-millionaire-after-growing-up-poor-in-london.html` | Background verification |
| 4 | `https://theboldnews.com/31-year-old-millionaire-tells-gen-z-its-scarily-easy-to-get-rich-with-ai-right-now-no-excuses/` | Syndicated full copy |
| 5 | `https://news.ssbcrack.com/timothy-armoo-the-easiest-era-in-history-to-build-wealth-for-gen-z/` | Derivative coverage |
| 6 | `https://www.newyorkfed.org/research/college-labor-market` | Primary source for grad-labor stats |

Proxy status check (`$HTTPS_PROXY/__agentproxy/status`, 2026-08-31):
policy is non-selective allow-list; only package registries and Anthropic
endpoints exempted. Conclusion: full-text access is environmentally
impossible this session, not merely unattempted.

## Search passes (WebSearch, 2026-08-31)

Eight queries (count corrected from an initial "five" during the
adversarial-verify pass — the first tally was recalled, not recounted;
rule-7 case in miniature). Content below is what the search tool returned
(result titles, URLs, and its content summaries with embedded quotes).
Quotes recurred verbatim across independent syndications, which is the
basis for treating them as faithful to the article (REPORT.md assumption A1).

### Q1 — `Timothy Armoo AI "scarily easy" get rich Fortune unemployed millionaire`

Result set located the primary article and four syndicated/derivative
copies (Yahoo Finance, NewsBeep ×2, The Bold News, SSBCrack), plus a Muck
Rack profile for Fortune success journalist **Orianna Rosa Royle** (byline
lead, not confirmed from the article page itself).

Returned content: Armoo became a millionaire before 30; told Fortune
"it is scarily easy" to build wealth right now; called this "the greatest
era of wealth creation ever"; counters Gen Z blaming "a brutal job market
and AI"; recommends that "one of the most obvious things is to build
relatively small projects with AI" in 2026. Background: sent to live with
his grandmother in Ghana as a baby; arrived in the U.K. with no money or
network; tutoring business at 14 scaled to 65 tutors in six weeks; sold
publication Entrepreneur Express by 17; founded Fanbytes 2017; Brainlabs
acquired it 2022 for an eight-figure sum at age 27.

### Q2 — `Timothy Armoo Fanbytes sold Brainlabs age 27 millionaire` (background corroboration)

Independent outlets agreeing on the sale facts:

- CNBC (2024-08-30): "This 29-year-old from one of London's poorest
  neighborhoods became a millionaire after selling his influencer marketing
  firm" — grew up on a council estate, Old Kent Road, Southwark.
- theygotacquired.com: "Influencer marketing firm Fanbytes acquired by
  Brainlabs".
- Built to Sell podcast ep. 346: "How Timo Armoo Sold Fanbytes to Brainlabs
  For 3x Revenue".
- Face2Face Africa: "started his first business at 14 and became a
  multi-millionaire at 27".

Returned content: sale to Brainlabs was **May 2022**, "eight-figure deal",
Armoo was 27, made him and co-founders multi-millionaires; Fanbytes founded
2017, software + services helping brands run influencer campaigns aimed at
Gen Z (YouTube, TikTok, Instagram, Snapchat); clients included Estée Lauder
and Samsung.

### Q3 — `"Timothy Armoo" "build relatively small projects with AI" advice examples`

Returned content (article specifics):

- "In 2026 … one of the most obvious things is to build relatively small
  projects with AI."
- "AI enables you to think of an idea and put it out into the world."
- "Social media means that you don't need to pay someone in order to do it.
  You just need to spend time on the platform and just keep posting."
- ChatGPT and Claude named as lowering startup barriers; build a website on
  Squarespace, sell directly on TikTok, meet contractors/clients on Zoom —
  without leaving home.
- Legon Fund: £5M (~$6.7M) of his own money for AI startups founded by
  minority entrepreneurs.

### Q4 — `"Timothy Armoo" "greatest era of wealth creation" quotes what he recommends Gen Z build`

Returned content (the wealth-wave rationale):

- "This is the greatest era of wealth creation ever."
- On Legon Fund: "The reason I did that was that my wealth wave was social
  media. Now I think the wealth wave is AI, and I don't want anyone to say,
  'Well, I had the idea, but I didn't have the money to distribute it.'"

### Q5 — `newsbeep.com Timothy Armoo scarily easy get rich AI article details`

Returned content overlapped Q1 and Q3 (same claims, same quotes, from the
NewsBeep syndication) plus one addition: Entrepreneur Express sold "to
Horizon Media" by 17 — the single-sourced buyer detail flagged below.

### Q6 + Q7 — `Fortune Timothy Armoo Gen Z unemployment job market statistics August 2026 "no excuses" article` and SSBCrack variant

Returned content (the article's framing context + funding line):

- Article frames Armoo against a genuinely weak entry-level market:
  entry-level hiring slowed sharply as companies lean on AI; Gen Z grads
  applying to hundreds, sometimes thousands, of roles without an offer.
- Recent-grad figures attributed to the period through Q2 2026:
  unemployment ≈ **5.6%**, underemployment ≈ **42%** (NY Fed
  college-labor-market series; primary page fetch blocked — figure
  UNVERIFIED against primary, carried as reported).
- A "242,000 / highest since 2016" recent-grad unemployment figure appeared
  in one search summary with garbled attribution — **excluded** from the
  report as unreliable.
- "ChatGPT and Claude are virtually free — and if you've got something
  that's working, here's the money to get more customers for it" (Legon
  Fund pitch framing).
- Related Fortune links surfaced by the same pass (leads, not analyzed):
  July 2026 jobs-report coverage; "Gen Z men with college degrees now have
  the same unemployment rate as non-grads"; a 2024 Fortune "The Good Life"
  Armoo profile.

### Q8 — `Timothy Armoo "scarily easy" Fortune article criticism counterpoint economists survivorship pushback Gen Z reaction`

Run during the adversarial-verify pass to convert the "does pushback
exist?" gap. Returned:

- **No published criticism or reaction piece targeting this article was
  located as of 2026-08-31** (day-of-publication search; result set was the
  article's own syndication cluster plus generic survivorship-bias
  explainers).
- Base-rate material (secondary aggregators relaying BLS business-survival
  data — leads, primaries not fetched, egress-blocked): first-year failure
  ≈ 20.4%, five-year ≈ 49.4%, ten-year ≈ 65.3% (attributed to 2024 BLS
  data by the aggregators).
- A circulating "90% of AI startups fail" figure and a "42% fail from
  insufficient market demand" figure appeared in aggregator blogs —
  **excluded** from the report: provenance untraceable this session.

## Single-sourced items (flagged)

- Entrepreneur Express buyer named as **Horizon Media** in one snippet only.
- Byline **Orianna Rosa Royle** inferred from a Muck Rack result adjacent
  to the article listing, not read off the article.

Both are carried in REPORT.md as single-sourced with these receipts.
