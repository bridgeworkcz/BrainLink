# BrainLink Architecture Summary

- **NeuroCore**: Single persistent DB (Postgres + pgvector)
- **Episodic Archive**: Event memory with 6-dimension scoring (-25 to +25)
- **Agents**: Trait agents (OCEAN), Needs (SDT), Moral Filter (toggleable), Executive, Metacognition
- **Persistence**: Full state survives app restarts
- **Personality Map**: Ultra-detailed JSON dossiers (example: Churchill)

Next steps: FastAPI backend, agent prompts, memory retrieval, iOS client.