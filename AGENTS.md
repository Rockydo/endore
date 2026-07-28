# AGENTS.md — ENDÓRË
Source of truth: `docs/ENDORE_MASTER_PLAN.md` (read fully once per session start).
Loop: pick the top unblocked task in `docs/TODO.md` → implement a large coherent batch →
`make validate` green → if game-visible, `make smoke` green → milestone verification when
due → commit and push → update TODO/PROGRESS and any judged DECISIONS/ASSUMPTIONS.
Never commit red. Never edit GAME_DIR. Blocked twice → `BLOCKERS.md` → next task.
No human-in-the-loop steps exist: automate launcher, console, tests, and screenshots with
`tools/gamedriver.py`. M1 Proof of Arda blocks all faction, mechanic, art, and lore work.
