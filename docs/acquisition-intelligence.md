# Acquisition Intelligence

This layer tracks how ADE competitors appear to acquire developer attention:
paid ads, launch channels, sponsored distribution, and adjacent demand signals.
It is separate from benchmark evidence. A product can have strong acquisition
signals without being better in a reproducible task run.

## Scope

Track acquisition evidence for the same software ADE roster used by
`competitors/`:

- Tachyon
- Orca
- HiveTerm
- T3 Code
- Hive
- AgentsRoom
- Augment Code
- OpenADE / ADE App
- Kandev

LandingAI remains out of the software ADE benchmark roster. If it appears in
marketing research, keep it in an excluded or adjacent-products section.

## Evidence Rules

- Prefer first-party transparency tools, official ad libraries, official launch
  pages, and vendor-owned landing pages.
- Record only what the source actually exposes: creative, headline, body copy,
  CTA, landing URL, platform, visible dates, region, and advertiser identity.
- Do not infer spend, CAC, conversion rate, targeting, or ROI unless a platform
  explicitly exposes it.
- Treat screenshots, newsletters, podcasts, and social posts as campaign
  evidence, not product capability evidence.
- Keep acquisition claims separate from `competitors/*.json` technical facts
  until a schema exists for marketing data.

## Primary Paid Channels

These are the first channels to check for repeatable competitor campaign scans.

| Channel | Source | What to capture | Limitations |
| --- | --- | --- | --- |
| Meta / Facebook / Instagram | Meta Ad Library and Meta Ad Library API | Active ads, creative copy, CTA, landing URLs, advertiser/page identity, countries when exposed | API coverage is strongest for politics/social issues and UK/EU all-ad access; performance and spend are generally unavailable |
| Google / YouTube / Display / Search | Google Ads Transparency Center | Verified advertiser ads across Google surfaces, creative variants, landing domains, visible date/context fields | Thin records; no reliable performance, budget, keyword, or full targeting data |
| LinkedIn | LinkedIn ad transparency/library surfaces and manual company/page review | B2B positioning, promoted content, gated demo motions, enterprise messaging | Often harder to automate; access and fields vary by region and login state |
| X.com | X Ads Repository / DSA repository and historical archives | Commercial communications where available, political/issue archives, advertiser search outputs | Coverage is uneven outside DSA surfaces; historical ATC archives are not equivalent to current global commercial ad coverage |

## Secondary Paid Channels

These are useful, but should not block the first version of the acquisition map.

| Channel | Source | Why it matters | Limitation |
| --- | --- | --- | --- |
| TikTok | TikTok Creative Center and Commercial Content Library | Can reveal awareness creatives, short-form positioning, and consumer-style developer acquisition experiments | ADE/B2B signal may be sparse; fields and access vary by country and library |
| Reddit Ads | Reddit Ads Inspiration Library and r/RedditPoliticalAds for political transparency | Developer audiences are active on Reddit; ads can reveal community-specific positioning | General competitive ad transparency is less complete than Meta/Google; political transparency is a separate use case |
| Snapchat | Snap Political and Advocacy Ads Library | Useful mainly if a competitor tests broad consumer or hiring-style campaigns | Mostly political/advocacy transparency; unlikely to be a core ADE channel |
| Pinterest | Pinterest Ads Repository | Useful only if a competitor targets visual/productivity discovery | EU/DSA-oriented and likely low relevance for ADEs |

## Adjacent Signals

These are not ads, but they help explain distribution, narrative, and community
traction.

| Signal | Source | What to capture | How to use |
| --- | --- | --- | --- |
| Product Hunt launches | Product Hunt product/launch pages and launch guide context | Launch date, tagline, maker comments, upvotes, launch assets, first landing URL | Treat as launch/distribution evidence, not paid acquisition |
| Sponsored newsletters | Newsletter issues, sponsorship pages, archive pages, UTM landing URLs | Sponsor copy, audience, issue date, CTA, landing page, discount or waitlist offer | Good for developer-market positioning and message testing |
| Podcasts and video sponsorships | Episode pages, YouTube descriptions, transcript snippets, sponsor reads | Sponsor message, creator/audience fit, date, landing URL, promo code | Good for narrative and channel fit; usually no spend/performance |
| GitHub Sponsors | GitHub Sponsors profiles and docs | Sponsorship status, tiers, public sponsor CTA, funding model | Not advertising; use as open-source sustainability or community signal |
| GitHub repository traffic proxies | Stars, releases, discussions, issues, sponsor links | Momentum around launch/campaign windows | Not acquisition proof; correlate only as context |
| YouTube search ads | Google Ads Transparency Center | Video/display creative, advertiser, landing URLs, visible ad variants | Treat as Google channel evidence; no performance metrics |

## Initial Data Shape

Do not create a scoring model until the first scans are collected. A future
tracked record can use this shape:

```json
{
  "product_id": "agentsroom",
  "platform": "meta",
  "channel_class": "primary-paid",
  "advertiser_name": "AgentsRoom",
  "status": "active",
  "first_seen": "2026-07-07",
  "last_seen": "2026-07-07",
  "countries": ["US", "BR"],
  "creative_type": "video",
  "headline": "...",
  "body": "...",
  "cta": "Sign Up",
  "landing_url": "https://...",
  "claims": ["multi-agent", "desktop cockpit"],
  "positioning_tags": ["orchestration", "local-agents"],
  "source_url": "https://...",
  "confidence": "official-library",
  "notes": "No spend or conversion data exposed."
}
```

Recommended future layout:

```text
marketing/
  advertisers/
    agentsroom.json
    augment-code.json
  scans/
    2026-07-07/
      meta.json
      google.json
      linkedin.json
      x.json
      secondary.json
  creatives/
    <platform>/<advertiser>/<ad-id>.md
  schema/
    ad-snapshot.schema.json
```

## Collection Workflow

1. Build an advertiser alias list for each competitor: product name, company
   name, domain, known social handle, GitHub org, and founder/company page.
2. Search primary paid channels first: Meta, Google, LinkedIn, and X.
3. Search secondary paid channels: TikTok, Reddit, Snapchat, and Pinterest.
4. Search adjacent signals: Product Hunt, newsletters, podcasts, YouTube
   descriptions, GitHub Sponsors, and launch posts.
5. Save one raw source URL per claim and note the date checked.
6. Tag each finding by message: local-first, multi-agent orchestration,
   enterprise governance, open source, bring-your-own-agent, mobile/remote, or
   pricing.
7. Keep "not found" results. Absence of visible ads is useful but should be
   recorded as "no public library result found", not "no ads running".

## Public Source Starting Points

- Meta Ad Library: https://www.facebook.com/ads/library/
- Meta Ad Library API: https://www.facebook.com/ads/library/api/
- Google Ads Transparency Center: https://adstransparency.google.com/
- TikTok Creative Center: https://ads.tiktok.com/business/creativecenter
- TikTok Commercial Content Library: https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/commercial-content-library
- X Ads Transparency: https://business.x.com/en/help/ads-policies/product-policies/ads-transparency
- X Ads Repository: https://ads.twitter.com/ads-repository
- Reddit Ads Inspiration Library: https://business.reddithelp.com/s/article/ads-inspiration-library
- Reddit Political Ads Transparency: https://www.reddit.com/r/RedditPoliticalAds/
- Product Hunt Launch Guide: https://www.producthunt.com/launch
- Product Hunt: https://www.producthunt.com/
- GitHub Sponsors: https://docs.github.com/en/sponsors
- Snap Political Ads Library: https://www.snap.com/political-ads
- Pinterest Ads Repository: https://ads.pinterest.com/ads-repository/
