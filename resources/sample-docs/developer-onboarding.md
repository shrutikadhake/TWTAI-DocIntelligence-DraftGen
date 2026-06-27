# Developer Onboarding Guide

Welcome to the engineering team. This guide walks you through everything you need to set up your development environment and start contributing on day one.

---

## Before you begin

> **Important:** Complete all steps in order. Skipping steps may cause issues later in the setup process.

Make sure you have the following ready:

- A laptop with at least 8GB RAM and 50GB free disk space
- A company email address
- Access to the team Slack channel (`#engineering-onboarding`)
- Admin rights on your machine

---

## Step 1: Install required tools

Install the following tools in this exact order.

### 1.1 Install Git

Download Git from the official website and follow the installer instructions.

```bash
git --version
```

Expected output:

```
git version 2.40.0
```

### 1.2 Install Node.js

Use the LTS version (v20 or higher).

```bash
node --version
npm --version
```

### 1.3 Install Docker

Docker is required for running local services.

```bash
docker --version
docker compose version
```

> **Note:** On Windows, make sure WSL2 is enabled before installing Docker Desktop.

---

## Step 2: Clone the repositories

You will need three repositories to get started.

```bash
git clone https://github.com/company/backend-api.git
git clone https://github.com/company/frontend-app.git
git clone https://github.com/company/shared-utils.git
```

After cloning, set up your Git identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
```

---

## Step 3: Set up environment variables

Each repository has a `.env.example` file. Copy it and fill in the values.

```bash
cp .env.example .env
```

The following variables are required for the backend:

| Variable | Description | Example value |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@localhost:5432/db` |
| `JWT_SECRET` | Secret key for signing tokens | `your-secret-key-here` |
| `PORT` | Port the server runs on | `3000` |
| `NODE_ENV` | Environment name | `development` |
| `LOG_LEVEL` | Logging verbosity | `debug` |

---

## Step 4: Run the services

Start all services using Docker Compose.

```bash
cd backend-api
docker compose up -d
```

Verify all containers are running:

```bash
docker compose ps
```

You should see three containers with status `Up`:

- `backend-api`
- `postgres`
- `redis`

---

## Step 5: Run database migrations

```bash
npm run migrate
npm run seed
```

> **Warning:** Never run `seed` in production. It will overwrite real data.

---

## Team conventions

### Branch naming

Follow this pattern for all branches:

- `feature/short-description` — new features
- `fix/short-description` — bug fixes
- `docs/short-description` — documentation changes
- `chore/short-description` — maintenance tasks

### Commit messages

Use the [Conventional Commits](https://www.conventionalcommits.org) format:

```
feat: add user authentication endpoint
fix: resolve token expiry bug
docs: update API reference for /users
```

### Code review

Every pull request needs:

1. At least **two approvals** before merging
2. All CI checks passing
3. No unresolved comments
4. A linked Jira ticket in the PR description

---

## Useful commands

| Command | What it does |
|---|---|
| `npm run dev` | Start development server with hot reload |
| `npm run test` | Run the full test suite |
| `npm run lint` | Check code for style issues |
| `npm run build` | Build the production bundle |
| `npm run migrate` | Run pending database migrations |

---

## Common issues

### Port already in use

If you see `Error: listen EADDRINUSE`, another process is using the port.

```bash
lsof -i :3000
kill -9 <PID>
```

### Docker container not starting

Check the container logs:

```bash
docker compose logs backend-api
```

### Database connection refused

Make sure the PostgreSQL container is running:

```bash
docker compose restart postgres
```

---

## Support

If you get stuck, reach out through these channels:

- **Slack:** `#engineering-onboarding`
- **Email:** [devteam@company.com](mailto:devteam@company.com)
- **Wiki:** [Internal docs](https://wiki.company.com/engineering)
- **On-call engineer:** Check the [rotation schedule](https://wiki.company.com/oncall)

![Onboarding Checklist](https://via.placeholder.com/800x200.png?text=Onboarding+Checklist)

---

## Checklist

Use this checklist to track your progress:

- Install Git, Node.js, and Docker
- Clone all three repositories
- Set up environment variables
- Run Docker services successfully
- Complete database migrations
- Make your first commit
- Submit your first pull request
- Attend your first team standup
