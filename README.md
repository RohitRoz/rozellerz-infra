# rozellerz-infra

Infrastructure and site code for [rozellerz.com](https://www.rozellerz.com).

## Architecture

- **S3** — Static site hosting
- **CloudFront** — CDN with HTTPS
- **ACM** — SSL certificate (*.rozellerz.com)
- **CloudFormation** — Infrastructure as code

## Branches & Environments

| Branch | Environment | URL |
|--------|-------------|-----|
| `main` | prod | https://www.rozellerz.com |
| `dev` | dev | CloudFront default domain |

## Deployment

Deployments happen automatically via GitHub Actions:

- Push to `main` → deploys to **prod**
- Push to `dev` → deploys to **dev**
- Manual trigger via **Actions → Deploy rozellerz.com → Run workflow**

## Setup

### 1. GitHub Secrets

Add these to your repo under **Settings → Secrets → Actions**:

| Secret | Value |
|--------|-------|
| `AWS_ACCESS_KEY_ID` | IAM access key |
| `AWS_SECRET_ACCESS_KEY` | IAM secret key |

### 2. GitHub Environments

Create two environments under **Settings → Environments**:
- `prod` (optional: add protection rules / required reviewers)
- `dev`

### 3. First Deploy

```bash
git checkout -b dev
git push origin dev    # creates dev stack
git checkout main
git push origin main   # creates prod stack
```

## Project Structure

```
├── .github/workflows/
│   └── deploy.yml          # GHA deploy workflow
├── cloudformation/
│   └── stack.yml           # S3 + CloudFront + OAC
├── site/
│   └── index.html          # the website
└── README.md
```
