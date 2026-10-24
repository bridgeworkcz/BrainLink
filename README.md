# BrainLink

**Multi-agent AI shell simulating human psyche with persistent NeuroCore.**

First fully loaded personality: **Winston Churchill**.

## Quick Start (local)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Open http://localhost:8000 — chat interface with Churchill, Moral Filter toggle, NeuroCore memory.

## Architecture
- `personalities/winston_churchill.json` — full Personality Map (traits, traumas, Black Dog, SDT needs, Haidt foundations, episodic samples)
- FastAPI backend with modular context injection (ready for real Grok/Gemini agents)
- Simple NeuroCore (in-memory → replace with Postgres + pgvector)
- Toggleable Moral Filter
- Event scoring ready for expansion

## Next (production)
- Wire real LLM calls (Grok + Gemini Pro)
- Postgres + pgvector for true episodic/semantic memory
- Full multi-agent orchestration (trait agents, needs agent, executive)
- iOS SwiftUI client
- Personality generator script

Repo: https://github.com/bridgeworkcz/BrainLink
