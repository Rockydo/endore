# AGENTS.md — ENDÓRË
Source of truth: `docs/ENDORE_MASTER_PLAN.md` (read fully once per session start).
Loop: pick the top unblocked task in `docs/TODO.md` → implement a large coherent batch →
`make validate` green → if game-visible, `make smoke` green → milestone verification when
due → commit and push → update TODO/PROGRESS and any judged DECISIONS/ASSUMPTIONS.
Never commit red. Never edit GAME_DIR. Blocked twice → `BLOCKERS.md` → next task.
No human-in-the-loop steps exist: automate launcher, console, tests, and screenshots with
`tools/gamedriver.py`. M1 Proof of Arda blocks all faction, mechanic, art, and lore work.
Real EU5 sessions share the machine lease at `G:\eu5_runtime\slot` with ANTIQVITAS.
Exit 75 means DEFERRED, not red: do not wait, poll, count it as a blocker, claim the gate,
or commit game-visible content. Record the pending gate (the tools do this), continue the
next compatible static TODO task, and retry at the next natural checkpoint. `make validate`
never needs the lease. Before a game-visible commit, `tools/eu5_slot.py assert-smoked`
must prove the last green smoke covers the current game-visible tree fingerprint.
