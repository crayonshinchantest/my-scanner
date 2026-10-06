# Job Scanner — twice-daily Business Analyst / Consulting / Digital Transformation job list

Twice a day (~6 AM and ~3 PM IST) it scans **LinkedIn** (and **Adzuna**, if
keyed) for jobs posted in the **last 24 hours**, scores each one against your
resume set (Business Analyst / Consulting / Digital Transformation track),
builds an Excel of the best matches with clickable apply links, and emails it
to you. Each run only sends listings it hasn't sent you before — a URL once
emailed is never repeated in a later run.

## How matching works

It queries the **public** LinkedIn (and Adzuna) job-search endpoints (no
login, so your accounts are never touched or at risk) filtered to the last 24
hours, then scores every posting 0–100 by how much its title and description
overlap with keywords pulled from your resume set (see
`job_scanner/profile.py`). It also flags jobs at companies on your own
researched shortlist (`job_scanner/companies.py` `_TARGET_*` sets, sourced
from `COS.xlsx`) with a High/Medium/Low priority — those sort to the top of
the list regardless of score. Higher score = better fit; the email lists best
matches first. It ranks fit — it can't literally guarantee you'll be selected.
Tune the keywords, roles, and thresholds in `config.yaml` and `profile.py`
anytime.

### Resume recommendation
`job_scanner/resumes.py` picks which of your 7 tailored resumes (in the local,
gitignored `resumes/` folder) best fits each job — e.g. the McKinsey-style
resume for strategy/case-style roles, the SCG-style resume for digital
transformation/ERP roles, the Glide Brands-style resume for founder's-office/
CEO-office roles. The Excel's "Recommended resume" column names the file; you
still attach it yourself when applying.

## Setup (3 steps)

### 1. Create a Gmail App Password (so it can send the email)
Google no longer allows normal passwords for scripts. Create a 16-char app
password (2‑Step Verification must be on):
<https://myaccount.google.com/apppasswords> → app "Mail" → copy the 16 chars.

### 2. Give it the credentials
- **Local (Mac):** `cp .env.example .env` and paste your app password into `.env`.
- **GitHub Actions:** in your repo → Settings → Secrets and variables → Actions →
  add `GMAIL_ADDRESS` and `GMAIL_APP_PASSWORD`.

### 3. Choose how it runs twice daily (6 AM / 3 PM IST)

**Option A — GitHub Actions (recommended, always-on, nothing to keep running).**
The workflow `.github/workflows/daily.yml` already runs at 00:30 UTC (~6 AM IST)
and 09:30 UTC (~3 PM IST). Just push this repo to GitHub and add the two
secrets above. Run it once manually from the **Actions** tab → *Daily job
list* → *Run workflow* to test.

**Option B — Your Mac (launchd).** Runs at 6 AM and 3 PM local time whenever the Mac is awake:
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp launchd/com.ajinkya.jobscanner.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.ajinkya.jobscanner.plist
```

## Run it manually right now
```bash
python3 -m pip install -r requirements.txt
# Test without sending an email (just writes the Excel):
SKIP_EMAIL=1 python3 -m job_scanner.main
# Full run (needs .env with the app password):
set -a; source .env; set +a; python3 -m job_scanner.main
```

## Dashboard (Streamlit web app)

A private, password-gated web dashboard to track applications: see every job the
scanner found, click **✅ Applied**, record **which resume** you used, and move
each role through a pipeline (New → Applied → Interview → Offer/Rejected). Your
history is saved in `data/applications.json` in this repo, so it persists forever
and stays private to you. All free — no database or extra service.

**How data flows:** the daily Action saves scanned jobs to `data/jobs.json` and
commits it. The dashboard reads that plus `data/applications.json` (your status
choices) live from the repo via a token.

### Deploy it (one-time, ~10 min, all free)

1. **Make the repo Private** (Settings → General → Change visibility). It holds
   your job-search activity.
2. **Create a fine-grained Personal Access Token** so the app can save your
   application status: GitHub → Settings → Developer settings → *Fine-grained
   tokens* → Generate. Repository access = only `job-scanner`. Permissions →
   **Contents: Read and write**. Copy the token.
3. **Deploy on Streamlit Community Cloud** (free): <https://share.streamlit.io>
   → sign in with GitHub → **Create app** → pick this repo, branch `main`, main
   file `app.py`.
4. In the app's **Advanced settings → Secrets**, paste:
   ```toml
   GITHUB_REPO = "your-username/job-scanner"
   GITHUB_TOKEN = "github_pat_...."     # the token from step 2
   GITHUB_BRANCH = "main"
   APP_PASSWORD = "pick-a-password"     # you'll type this to open the app
   ```
5. Deploy. Open the URL, enter your password — that's your private dashboard.
   Bookmark it on your phone. It auto-updates after each scan.

Run it locally instead (uses the local `data/` files, no token needed):
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `config.yaml` — search keywords (your Tier 1/2/3 roles), locations, thresholds, email subject.
- `job_scanner/profile.py` — resume keywords used for scoring.
- `job_scanner/companies.py` — company tiers + your target-company priority list (from `COS.xlsx`).
- `job_scanner/resumes.py` — the 7-resume catalog and which keywords pick each one.
- `resumes/` — your actual resume PDFs (local only, gitignored — never pushed to the public repo).
- `job_scanner/sources/` — LinkedIn + Adzuna fetchers.
- `job_scanner/matcher.py` — the 0–100 scoring.
- `job_scanner/report.py` — Excel builder + Gmail sender.
- `job_scanner/store.py` — writes `data/jobs.json` for the dashboard and tracks which URLs were already emailed (so nothing repeats).
- `.github/workflows/daily.yml` — the twice-daily schedule for GitHub Actions.
- `launchd/…plist` — the twice-daily schedule for macOS.
- `app.py` — the Streamlit tracking dashboard.
- `gh_api.py` — reads/writes the JSON data files in your repo (dashboard persistence).
- `data/jobs.json` — scanned jobs (written by the Action).
- `data/applications.json` — your Applied status + resume used (written by the dashboard).

## Notes / honesty
- These are public endpoints; they can rate-limit or change their markup, in
  which case a source is skipped for that run (the other still works). If matches
  ever drop to zero for days, the site likely changed — ping and it's a quick fix.
- Built for **your personal** job search, not bulk/commercial scraping.
