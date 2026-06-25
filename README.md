# SME Insight Hub

> **A full-stack business intelligence platform for Small and Medium Enterprises — built with SvelteKit, FastAPI, and PostgreSQL.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-sme--insight--hub.vercel.app-blue?style=flat-square)](https://sme-insight-hub.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Svelte](https://img.shields.io/badge/Frontend-SvelteKit-orange?style=flat-square)](https://kit.svelte.dev)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2016-336791?style=flat-square)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED?style=flat-square)](https://www.docker.com)

---

## What is SME Insight Hub?

SME Insight Hub is a web application designed to help small and medium-sized businesses gain actionable insights from their data. It provides a centralized dashboard where SME owners and managers can upload documents, extract key information (including via OCR in English and Bengali), and monitor business metrics — all through a clean, responsive interface.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | SvelteKit + TypeScript + CSS |
| Backend | Python / FastAPI (async) |
| Database | PostgreSQL 16 |
| Auth | JWT (access + refresh tokens) |
| OCR | Tesseract (`eng+ben`) |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Hosting | Vercel (frontend) |

---

## Project Structure

```
SME-Insight-Hub/
├── frontend/          # SvelteKit application
│   ├── src/           # Components, pages, stores
│   └── static/        # Public assets
├── backend/           # FastAPI application
│   ├── src/           # API routes, models, services
│   └── uploads/       # File upload storage
├── .github/workflows/ # CI/CD pipelines
├── docker-compose.yml # Multi-service Docker setup
├── .env.example       # Environment variable template
└── LICENSE
```

---



## Key Features

- **Document Upload & OCR** — Upload business documents and extract text automatically, with support for both English and Bengali (`eng+ben` Tesseract).
- **JWT Authentication** — Secure login with short-lived access tokens and rotating refresh tokens.
- **Async API** — FastAPI with `asyncpg` for non-blocking database queries.
- **Containerized** — Full Docker Compose setup for reproducible local development and deployment.
- **Rate Limiting** — Built-in per-route rate limiting to protect API endpoints.
- **CI/CD** — Automated workflows via GitHub Actions.


## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

© 2026 Md Readus Shalehin
