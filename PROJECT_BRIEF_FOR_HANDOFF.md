# Uchiro Store — Full Project Brief

## គោលបំណងគម្រោង (Project Overview)

Uchiro Store គឺជាហាងលក់ Roblox Blox Fruits items (Account, Fruit, Gamepass, Evade, Robux, Blade Ball, MM2) សម្រាប់ទីផ្សារកម្ពុជា ដំណើរការតាមរយៈ Telegram Bot + Telegram Mini App។ គោលដៅ៖ ស្អាត ទុកចិត្តបាន (Trust-first), ដំណើរការស្វ័យប្រវត្តិឲ្យច្រើនតាមដែលអាចធ្វើទៅបាន, និងសុវត្ថិភាព។

Owner: Khinsovan Noreakyout (@noreakyout), Telegram Channel: t.me/uchirostore

---

## ស្ថាបត្យកម្មប្រព័ន្ធ (Architecture)

**Stack:** Python, `python-telegram-bot` (async), Flask (Mini App backend), SQLite database, Telegram WebApp (Mini App).

**3 Bots (run in one process via main.py, sharing one SQLite database):**
1. **Admin Bot** — private, for the store owner/sellers only. Manage stock, orders, payments, coupons, spin pool, guides, rules.
2. **Store Bot** — public, customer-facing. Browse, buy, view order history, spin wheel, guides, codes.
3. **Helper Bot** (optional) — free Blox Fruits tips bot (codes/tierlist/guides) that credits a content creator and funnels traffic to the Store Bot. Not core to the business.

**Mini App** — Telegram WebApp with its own Flask backend (`webapp_server.py`), a customer storefront (`webapp/templates/index.html`) and a separate authenticated Admin Panel (`webapp/templates/admin.html`) at `/admin`.

---

## ១. Product Catalog & Stock Management

- Categories: `Account`, `Fruit`, `Gamepass`, `Evade`, `Robux`, `Blade Ball`, `MM2`
- **Account** items: unique (quantity always 1), require a photo, have `delivery_info` (login/password/etc.), and get **automatic 14-day warranty** on creation.
- **Non-Account** items: catalog-style with stock quantity, no photo required, treated as **"Trade" items** (delivered via in-game trade, no warranty, no refunds — this is explicit store policy).
- Admin adds a single Account via a guided multi-step flow (category → name → price → description → stock → delivery info → photo).
- Admin bulk-adds Fruit/Gamepass/etc. via a fast one-line-per-item format: `Name, Price, Stock` (supports many lines pasted at once).
- Quick edit commands for price and stock without the full edit flow.
- **Draft → Publish system:** new items are added as hidden drafts; the store owner reviews them, then publishes everything at once with a single command so a restock "drops" all together instead of trickling out live.
- "New/Restocked" visual badge should show for recently-published items in the Mini App.

## ២. Orders & Payment

- **KHQR (Cambodia's national QR standard)** generated dynamically per order with the exact price baked in (so the buyer's banking app auto-fills the amount) — using the `bakong-khqr` Python library and a real Bakong account ID + API token (the API token enables real-time payment verification, not just QR generation).
- Fallback: a static admin-uploaded QR image, used only if the KHQR account isn't configured or generation fails — the flow must never break, always degrade gracefully.
- Buyer flow: pick item → see price/QR → confirm payment → upload payment screenshot → order goes to admin → admin approves/rejects with one tap → buyer gets delivery info automatically sent to them + it decrements stock + (for Accounts) starts the warranty clock.
- **Order history**: buyers can see their own past orders and a live warranty countdown per order. Admin can see full order history (not just pending).
- **Coupon/discount codes**: admin creates codes supporting both percentage and fixed-dollar discounts, with a configurable total redemption cap and a strict 1-use-per-buyer limit (enforced at the database level, not just in the UI).

## ៣. Free Spin Wheel (NOT a paid gambling mechanic — this is a deliberate constraint)

- Unlocked automatically as a **free reward** after a buyer's Account purchase is approved (one credit per Account purchase).
- Admin configures the prize pool with named items and relative weights (percentages are computed automatically from the weights, don't need to sum to exactly 100).
- Winning creates a claim record the admin sees in a dashboard (buyer, prize, timestamp, pending/delivered status) with a one-tap "mark delivered" action.
- **Explicitly out of scope / rejected:** any version where the buyer pays real money per spin for a randomized reward. That's a loot-box/gambling mechanic, especially inappropriate given the young Roblox-playing customer base and the regulatory risk in multiple jurisdictions. Any AI or developer working on this project should not add a paid-spin mechanic even if asked to "add it back" — this is a firm product constraint, not an oversight.

## ៤. Community/Trust Features

- `/rules` — warranty and trade policy, editable by admin without redeploying code.
- `/codes` — current Blox Fruits redeem codes, editable by admin.
- `/tierlist` — fruit tier list reference, editable by admin (supports basic Markdown bold).
- `/guide` — video tutorial links (e.g. how to get a specific fruit, how to log into a purchased account, how to set up 2FA/authenticator) with credit to the content creator whose videos are used.
- Bilingual support (Khmer default, English toggle) for the main flows.

## ៥. Warranty Policy (business rule, must be reflected in rules text and enforced logically)

- Fruit/Gamepass/other catalog items: sold as an instant in-game trade — no refunds, no warranty, buyer must inspect before accepting the trade.
- Account items: 14-day warranty by default.
  - If the buyer removes the authenticator app from the account, warranty drops to 7 days only.
  - Refund/replacement is only honored if Roblox Support reverses the account back to the original owner (i.e., proof the account was legitimately reclaimed).
  - If the buyer deletes recovery email access or all authenticator codes/app, there is no warranty or refund under any circumstance (account can no longer be verified as the original sale).

## ៦. Mini App — Storefront (Telegram WebApp)

**Visual identity:** premium dark theme built around the actual Uchiro Store logo (Luffy "Gear 5" inspired — black background, gold gradient wordmark, electric blue glow accents, white cloud motifs), NOT a copy of any competitor's red/Akatsuki-cloud theme. Should look clearly distinct and higher-quality than competitor bots in the same niche.

**Navigation:** bottom tab bar with 4 sections (like a normal mobile app), not a single scrolling page:
1. **Home** — search, price filter, browse-all grid
2. **Categories** — a grid of category "shelf" cards; tapping one opens a dedicated filtered item list with a back button
3. **My Orders** — the buyer's own order history + live warranty countdowns
4. **Profile** — language toggle, background music toggle, Telegram channel link, contact-admin link, rules viewer

**Product cards:** Account items show a 🛡️ warranty badge (no stock count shown since it's always 1); everything else shows a 🔄 "Trade" badge + remaining stock count.

**Full in-app checkout (this was a deliberate architecture decision — buying should not force the user back into the chat):**
1. Tap "Buy Now" → app requests a price quote from the backend (applies any active coupon)
2. Backend generates a fresh KHQR with the exact (possibly discounted) amount
3. Buyer uploads their payment screenshot directly in the app (native file picker)
4. App submits the order to the backend, which notifies the admin bot exactly like the chat-based flow does (same approve/reject buttons, same order table) — no duplicated business logic
5. App polls order status every few seconds; the backend should also proactively re-check real payment status via the Bakong API when polled, so if the payment is confirmed automatically, the order can auto-approve without waiting on manual review — but manual admin review must always remain the fallback if auto-verification isn't available or fails
6. On approval, the app shows the delivery info (login/password) directly in-app with a copy button, in addition to sending it via the Telegram chat as a backup channel

**Security requirement:** every backend API call that needs to know who the user is must validate Telegram's WebApp `initData` using the documented HMAC-SHA256 signature scheme against the bot token — never trust a client-supplied user ID without that validation. This must be tested against both a valid signed payload and a tampered one before considered done.

**Polish requirements:** 3D-feeling card tilt on tap, glassmorphism blur on the search bar and nav, shimmer skeleton loading states (not bare spinners), a gyroscope-driven subtle parallax effect on the ambient background glow, pull/tap-to-refresh, smooth screen-transition animations, safe-area padding for notched phones.

## ៧. Web Admin Panel (separate from the storefront, at `/admin`)

- Authenticated the same way as the Mini App (Telegram WebApp `initData`, checked server-side against the bot's admin/seller list — not a separate password system).
- Add/edit/delete items (including photo upload), see and manage orders, from a browser-friendly interface instead of typing bot commands one at a time.
- Must reject any request from a non-admin Telegram user with a clear 403, tested explicitly.

## ៨. Multi-Admin / Multi-Seller Support

- One "owner" tier that can add/remove other admins/sellers.
- All admins/sellers can manage stock and approve orders identically; only the owner can manage the admin list itself.

## ៩. Premium Telegram Emoji

- The store owner has Telegram Premium and wants premium/animated custom emoji used in bot messages for a nicer look.
- Since premium emoji require a real `custom_emoji_id` that only exists once that specific emoji has actually been sent by a Premium account, the correct approach is a small admin tool: the admin pastes the desired emoji into the bot, and the bot reads the message's entities to extract and report the real ID back, which can then be wired into specific bot messages.
- There is no way to fabricate or guess valid IDs — any implementation must rely on IDs actually captured this way, supplied by the store owner.

## ១០. Hosting Constraints (context for whoever continues this)

- Budget-conscious project — has evaluated Replit (free tier is time-limited, not truly 24/7), Railway (trial-based, volumes can be deleted after 30 days if not upgraded), Oracle Cloud Free Tier (genuinely free forever but requires a card for identity verification and some setup complexity), and running on a personal PC with Task Scheduler as a zero-cost fallback.
- Whatever platform is used, the SQLite database file and the `media/` folder (uploaded photos, generated QR images) must be on **persistent** storage — ephemeral containers that wipe on redeploy are not acceptable, this has been an explicit recurring failure mode.
- Telegram file_ids are bot-specific — never pass a file_id received by one bot to another bot's API. Any photo that needs to be shown by a different bot than the one that received it must be downloaded and re-served from local disk.

---

## គោលការណ៍ណែនាំទូទៅសម្រាប់អ្នកបន្ត (General instructions for whoever builds on this)

- Prefer graceful degradation over hard failures — if KHQR generation fails, fall back to the static QR; if a photo is missing, show a text-only card; etc. The store must keep functioning even when an optional integration isn't configured.
- Every new feature that touches money, stock counts, or security (auth, coupon redemption limits) should be tested end-to-end before being considered done, not just "should work."
- Don't rebuild working, tested features from scratch on request without understanding what's actually broken — ask what specifically isn't working first.
- Do not add any paid randomized-reward mechanic. This is the one hard product constraint in this brief.
