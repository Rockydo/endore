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

IMPORTANT NOTE FOR THE IMAGE GENERATION : GPT IMAGES 2 IS CAPABLE OF HANDLING A LOT OF DETAIL. INSTEAD OF GENERATING IMAGES ONE BY ONE, YOU WILL GENERATE 4 DIFFERENT ICONS WITHIN A SINGLE IMAGE EACH TIME AND THEN SPLIT THESE INTO INDIVIDUAL FILES WITH LOCAL TOOLS
PLEASE MAKE SURE THE IMAGES DON'T LOOK GENERIC, DON'T HAVE A CHEAP YELLOW FILTER OVER THEM. REALLY PASS REAL ASSETS OF VANILLA EUV TO EACH IMAGE GENERATION REQUEST AS A STYLE REFERENCE SO IT GETS IT RIGHT AND MAKES BEAUTIFUL NON GENERIC HIGHLY AUTHENTIC THINGS
IT IS CRITICAL TO REALLY PASS ACTUAL PRECISE REFERENCES OF REAL EUV ASSETS TO THE IMAGE GENERATOR OR ELSE THE STYLE IS JUST TOO DIFFERENT AN IMMERSION BREAKING. REALLY FOCUS ON THE VISUAL STYLE
PLEASE HEAVILY REFERE TO PETER JACKSON'S TRILOGY FOR THE SPECIFICS OF HOW THINGS LOOK (buildings, units, advances, etc etc). SEND REAL REFERENCE IMAGES FROM THE FILMS YOU FIND ONLINE. THE FILMS REALLY NAILED THE MIDDLE EARTH AESTHETIC
Specific notes of things that were messed up in the past that I want you to watch out for :
	- Building images which are not properly round to fit the UI format (LOOK AT THE VANILLA FORMAT, DON'T IMPROVISE)
	- New trade goods that didn't have an empty background (LOOK AT THE VANILLA FORMAT, DON'T IMPROVISE)
	- Improperly cropped images
Having good icons and art style is critical to really selling the high quality of the mod. Formatting issues kill credibility and really tarnish the image of the mod.