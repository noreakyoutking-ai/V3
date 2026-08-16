# Uchiro Store — Master Spec (សរុបទាំងអស់)

## ⚠️ សំខាន់ជាមុនអ្វីទាំងអស់ — ការសុវត្ថិភាព Token

អ្នកបានផ្ញើ Bakong API Token និង Account ID ក្នុង Chat។ ខ្ញុំនឹង**មិនដាក់ Token នេះចូល Code ដោយផ្ទាល់ទេ** (Hardcode) ព្រោះមិនសុវត្ថិភាព — នរណាម្នាក់ឃើញ Code នេះនឹងអាចប្រើ Token របស់អ្នកបាន។ ជំនួសវិញ អ្នកនឹងដាក់វាជា **Environment Variable** (`BAKONG_API_TOKEN`) លើ Railway ផ្ទាល់ (ដូច Token Bot ដែរ) — Code នឹងអានពី Environment មិនមែនសរសេរជាប់ជានិច្ចទេ។

**សូមពិចារណា Regenerate Token ថ្មី** ពី Bakong Developer Portal ព្រោះ Token ចាស់នេះបានបង្ហាញក្នុង Chat History ស្រេចហើយ — ជាការប្រុងប្រយ័ត្នស្តង់ដារ (មិនចាំបាច់ប្រញាប់ ប៉ុន្តែគួរធ្វើនៅពេលងាយស្រួល)។

---

## ១. អ្វីដែលបានសាងសង់ + Test រួច ✅ (ដំណើរការស្រាប់)

| Feature | Command/Location | ស្ថានភាព |
|---|---|---|
| Admin Bot — បន្ថែម Account (មានរូបភាព) | `/additem` | ✅ |
| Admin Bot — បន្ថែម Fruit/Gamepass/Evade/ល ច្រើនក្នុងម្តង | `/addstock`, `/addfruit`, `/addgamepass` | ✅ |
| កែស្តុក/តម្លៃលឿន | `/setstock`, `/setprice` | ✅ |
| Multi-Seller (Owner បន្ថែម Admin ថ្មី) | `/addseller`, `/removeseller`, `/sellers` | ✅ |
| QR ទូទាត់ស្តាទិច | `/setpayment`, `/showpayment` | ✅ |
| **KHQR ស្វ័យប្រវត្តិ** (តម្លៃពិត auto-generate) | `/setkhqr`, `/showkhqr` | ✅ (ត្រូវការ account_id របស់អ្នក) |
| Warranty ស្វ័យប្រវត្តិ (Account = 14ថ្ងៃ) | Auto នៅ `/additem` | ✅ |
| Order History + Warranty Countdown | `/myorders` (Store Bot), `/orderhistory` (Admin) | ✅ |
| Redeem Codes | `/setcodes` → `/codes` | ✅ |
| Fruit Tier List | `/settierlist` → `/tierlist` | ✅ |
| Video Guides (login/2FA tutorials) | `/addguide` → `/guide` | ✅ |
| វិធាន/Warranty Policy | `/setrules` → `/rules` | ✅ |
| ស្ថិតិហាង + អ្នកប្រើប្រាស់ | `/stats`, `/users` | ✅ |
| Premium Emoji ID Finder | `/findemoji` | ✅ |
| ភាសា Khmer/English | `/language` | ✅ |
| Helper Bot (Bot ទី៣ ជំនួយ Player ឥតគិតថ្លៃ + Credit) | Optional, `HELPER_BOT_TOKEN` | ✅ |
| **Mini App** — Bottom Tab Nav (ដើម/ប្រភេទ/Order/គណនី) | `/shop` ឬប៊ូតុងលើ `/start` | ✅ |
| Mini App — 3D Card Tilt, Glassmorphism, Shimmer Loading, Gyroscope Parallax | ក្នុង Mini App | ✅ |
| Mini App — ទិញពេញលេញក្នុង App (QR→Upload→Poll→Auto-delivery) | ក្នុង Mini App | ✅ |
| Mini App — Security (HMAC initData validation) | Backend | ✅ Test ជាមួយ Attack case |
| **Web Admin Panel** (បន្ថែម/កែ/លុប ទំនិញ, មើល Order លើ Browser) | `/panel` | ✅ Test ជាមួយ Auth + Unauthorized case |
| Warranty Badge (Account) vs Trade Badge (ផ្សេងទៀត) | Mini App Cards | ✅ |

---

## ២. បដិសេធជាស្ថាពរ ❌ (មិនផ្លាស់ប្តូរទោះសុំម្តងទៀត)

**Paid Gacha/Spin System** ($0.75/Spin ចាប់ Fruit ចៃដន្យ) — នេះជា Gambling Mechanic ពិតប្រាកដ (Loot Box + Real Money) ដែល៖
- ខុសច្បាប់ក្នុងប្រទេសខ្លះទាំងស្រុង (Belgium, Netherlands ចាត់ទុកជា Gambling)
- គោលដៅអតិថិជនភាគច្រើនជាកុមារ/យុវជនលេង Roblox — គ្រោះថ្នាក់ខ្ពស់
- ជំនួសវិញ: **Spin Wheel ឥតគិតថ្លៃ** (unlocked ក្រោយទិញ Account) — Reward ជា Discount Code ឬ Fruit តូចៗ

---

## ៣. កំពុងសាងសង់ឥឡូវនេះ 🚧

### A. KHQR Auto-Verify (ប្រើ Token ដែលអ្នកផ្ញើ)
- ពេលអតិថិជនស្កេន KHQR ក្នុង Mini App ហើយបង់ប្រាក់ពិត Bakong API នឹងផ្ទៀងផ្ទាត់ស្វ័យប្រវត្តិ (មិនចាំបាច់រង់ចាំ Admin ចុច Approve ដោយដៃទៀត ក្នុងករណីនេះ)
- បើ Bakong មិនអាចផ្ទៀងផ្ទាត់បាន (Token ផុតកំណត់ ឬបញ្ហា Network) → Fallback ទៅ Manual Screenshot Review ធម្មតា (មិនបាត់ Order ណាមួយឡើយ)

### B. Draft → Publish (`/release`)
- Admin បន្ថែមទំនិញជាមុន (មិនទាន់បង្ហាញអតិថិជន) រួច `/release` ដើម្បីបង្ហាញម្តងតែម្តង

### C. Coupon System
- `/addcoupon CODE 20% max:10 limit:1` (% ឬ $ ក៏បាន)
- កំណត់ចំនួន Redeem សរុប + 1ដងក្នុងម្នាក់

### D. Free Spin Wheel
- Unlock ក្រោយទិញ Account (មិនគិតលុយ)
- Reward: Discount Code ឬ Fruit តូចៗ

---

## ៤. សំណួរដែលនៅសល់ត្រូវឆ្លើយ (ដើម្បីខ្ញុំបញ្ចប់ត្រឹមត្រូវ)

1. **`/release`**: ចង់ Publish ម្តងមួយ (`/release <id>`) ឬ ទាំងអស់ម្តងតែម្តង (`/release all`) ឬចង់បានទាំង២?
2. **Coupon**: ចង់បានតែ % ឬ ចង់បានទាំង % និង $ ?
3. **Spin Wheel**: Reward គួរជា Discount Code, Fruit តូច, ឬទាំងពីរ (ចៃដន្យ)?

---

## ៥. Deploy Checklist (ក្រោយខ្ញុំបញ្ចប់)

Environment Variables ត្រូវកំណត់លើ Railway:
```
ADMIN_BOT_TOKEN=...
STORE_BOT_TOKEN=...
HELPER_BOT_TOKEN=... (optional)
OWNER_IDS=...
STORE_BOT_USERNAME=...
WEBAPP_URL=...
BAKONG_API_TOKEN=... (Token ថ្មីដែលអ្នកគួរ Regenerate)
```
Admin Command បន្ថែម:
```
/setkhqr khinsovan_noreakyout@bkrt | Uchiro Store | Phnom Penh
```
