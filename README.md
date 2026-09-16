<div align="center">
    <img src="apps/web/public/logo.svg" alt="Logo" width="120" height="120">
    <h1>Voxlway</h1>
</div>

[![CI](https://img.shields.io/github/actions/workflow/status/alexchoukeir/voxlway/ci.yml?branch=main&label=CI)](https://github.com/alexchoukeir/voxlway/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Voxlway ([voxlway.com](https://www.voxlway.com)) is a semantic search engine and discovery platform to help users find Roblox games. It utilizes LLMs and vector embeddings to make game discovery much quicker and more accurate. Instead of endlessly scrolling, users can describe gameplay, mechanics, or vibe and get relevant results instantly.

## 🚀 Key Features

- **Natural Language Search**: Users can search for games using full descriptions of the vibe or gameplay instead of exact titles (e.g. "cozy building game with friends").

- **Instant Filtering**: Allows users to narrow down and refine search results using filters like category and tags.

- **LLM Data Enrichment**: Fetches raw game data and passes it through an LLM to generate metadata.

- **Vector Similarity Search**: Translates natural language into vector embeddings and uses cosine similarity to measure how well a game matches the meaning of a user's search query.

## 📸 Screenshots

<img width="2508" height="1636" alt="image" src="https://github.com/user-attachments/assets/ad76fce5-45c0-4281-84d0-17706a281835" />
<img width="2508" height="1660" alt="image" src="https://github.com/user-attachments/assets/a30295f5-830c-4548-a990-de39c64d5e99" />

## 🛠️ Tech Stack

- **Frontend**: Next.js
- **Backend**: FastAPI
- **Database**: PostgreSQL with pgvector hosted on AWS RDS
- **DevOps and Infrastructure**: Docker, AWS (S3, CloudFront, ECR, EC2, SQS, Route 53), GitHub Actions
- **Tooling and Workspace**: pnpm, Turborepo, uv

## 📁 Project Structure

```plaintext
voxlway/
│
├── apps/
│   ├── api/        # FastAPI backend
│   └── web/        # Next.js frontend
│
├── package.json    # Project configuration file
├── turbo.json      # Turborepo configuration file
└── README.md       # README file
```

## 🚀 Getting Started

### Prerequisites

- **Python (3.10 or higher)**
- **uv**
- **pnpm**
- **Node.js**
- **Docker & Docker Compose**

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/alexchoukeir/voxlway.git
cd voxlway
```

2. **Install Dependencies**
   - **Frontend & Monorepo**:

   ```bash
   pnpm install
   ```

   - **Backend**: Setup local python environment

   ```bash
   cd apps/api
   uv sync --frozen
   ```

3. Start Docker

```bash
cd apps/api
docker compose up --build
cd ../..
```

4. Running the project

```bash
pnpm dev
```

- **Next.js frontend**: `localhost:3000`
- **FastAPI backend**: `localhost:8000`
- **ElasticMQ**: `localhost:9324` and `localhost:9325`
- **PostgreSQL database**: `localhost:5432`

## 🧠 Team

| Member                 | Position                     | Responsibilities                                                                                                              |
| ---------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Alexander Choukeir** | Lead Developer               | Full-stack architecture, frontend & backend implementation, database design & management, CI/CD, DevOps, Cloud Infrastructure |
| **Hadi Mansour**       | UI/UX Designer and 3D Artist | Brand identity, wireframing, high-fidelity page designs, asset modeling                                                       |
