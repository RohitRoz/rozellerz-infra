# rozellerz-infra

Infrastructure and site code for [rozellerz.com](https://www.rozellerz.com).

## Architecture

```
CloudFront (CDN + WAF)
├── /          → S3 (static site)
└── /api/*     → API Gateway → Lambda → DynamoDB
```

**Security layers:**
- **WAF** — AWS Managed Rules (common exploits, bad inputs) + IP rate limiting (2000 req/5min)
- **Security headers** — HSTS, CSP, X-Frame-Options, XSS Protection, Referrer Policy
- **S3** — Encrypted at rest (AES-256), versioned, all public access blocked, OAC-only
- **CloudFront** — TLS 1.2+, HTTP/2+3, HTTPS redirect
- **Lambda** — Least-privilege IAM (DynamoDB access only)
- **DynamoDB** — Encrypted at rest, PITR enabled (prod)

## Branches & Environments

| Branch | Environment | URL |
|--------|-------------|-----|
| `main` | prod | https://www.rozellerz.com |
| `dev` | dev | CloudFront default domain |

## Workflows

### Deploy (`deploy.yml`)
- Push to `main` → deploys to **prod**
- Push to `dev` → deploys to **dev**
- Manual trigger: **Actions → Deploy → Run workflow** (pick env, optionally seed DB)

### Teardown (`teardown.yml`)
- Manual only — type `DESTROY` to confirm
- Empties buckets, deletes CloudFormation stack and all resources

## First-Time Setup

### 1. Clean up existing manual resources
```bash
pip install boto3
python scripts/cleanup_manual.py
```
This deletes the existing S3 bucket and CloudFront distribution so CloudFormation can recreate them.

### 2. GitHub Secrets
Add to **Settings → Secrets → Actions**:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### 3. GitHub Environments
Create under **Settings → Environments**: `prod` and `dev`

### 4. First Deploy
```bash
git remote add origin https://github.com/YOUR_USERNAME/rozellerz-infra.git
git push -u origin main
git push -u origin dev
```
Then run the deploy workflow manually with **seed_db = true** to populate DynamoDB.

## Project Structure

```
├── .github/workflows/
│   ├── deploy.yml              # CI/CD: CF stack + site + Lambda + cache
│   └── teardown.yml            # Destroy an environment
├── api/
│   └── handler.py              # Lambda: REST API for page content
├── cloudformation/
│   └── stack.yml               # S3 + CloudFront + WAF + Lambda + API GW + DynamoDB
├── scripts/
│   ├── cleanup_manual.py       # One-time: remove manually-created AWS resources
│   └── seed.py                 # Populate DynamoDB with page content
├── site/
│   └── index.html              # Frontend (fetches /api/pages dynamically)
└── README.md
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/pages` | List all pages (slug, title, subtitle, tags) |
| GET | `/api/pages/{slug}` | Get full page content |
| PUT | `/api/pages/{slug}` | Create/update a page |
| DELETE | `/api/pages/{slug}` | Delete a page |
