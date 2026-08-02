# Shared EU5 Test Coordination

ENDÓRË and ANTIQVITAS use separate repositories, playsets, user directories, logs, and
runtime-state directories. They share one installed `eu5.exe`, one desktop, and one GPU.
Only real game sessions are therefore serialized; static validation remains concurrent.

## Protocol

Both repositories vendor the same `tools/eu5_slot.py` protocol implementation. The
machine lease is an atomically created directory at:

`G:\eu5_runtime\slot\lease`

Its `owner.json` identifies the protocol version, random token, repository, operation,
game build, working-tree fingerprint, PID, and PID creation time. PID creation time
prevents a reused process identifier from inheriting ownership. A dead owner is reclaimed
automatically; a live unmanaged EU5 process is never killed.

The shared Python 3.11 runtime on this machine exposes `G:\antiqvitas\tools` on its base
search path. Every coordination entry point explicitly prepends its own repository's
`tools` directory before importing `runtime_state` or the slot module. Session records
also carry and verify both repository and user-directory identity, so an import-path
regression cannot authorize one project to control the other's PID.

A smoke lease covers the entire vanilla-control followed by mod-test transaction. A direct
driver launch hands its session lease to the exact EU5 process. All later driver commands
validate the tokenized repository session and select only a window owned by that PID.
`gamedriver stop` terminates only that process.

## Deferred work

Contention returns exit status 75 immediately and writes
`pending_eu5_gate.json` under the requesting repository's runtime-state directory. This
means DEFERRED, not FAIL:

- do not wait or poll;
- do not count it under the two-strike blocker rule;
- do not claim the game gate or commit game-visible content;
- continue the next compatible static TODO task;
- retry at the next natural checkpoint.

`make validate` does not acquire the slot. `make smoke` does. A successful smoke records
the current game-visible tree fingerprint in `last_smoke.json`. The fingerprint hashes
the actual bytes under `.metadata/`, `in_game/`, `main_menu/`, and `loading_screen/`;
it does not depend on `HEAD`, staging state, or Git LFS pointers. A smoke therefore stays
valid when identical game-visible bytes move from dirty to staged to committed state,
while any actual byte change still invalidates it. Before a game-visible commit, run:

```powershell
.\.venv\Scripts\python.exe tools\eu5_slot.py assert-smoked
```

Useful inspection commands:

```powershell
.\.venv\Scripts\python.exe tools\eu5_slot.py status
.\.venv\Scripts\python.exe tools\eu5_slot.py fingerprint
.\.venv\Scripts\python.exe tools\test_eu5_slot.py
```

Smoke uses a deliberately cheap graphics profile, but snapshots and restores the prior
player settings around the complete vanilla/mod transaction. If a legacy or interrupted
run left manual gameplay without close-zoom terrain, close EU5 and restore only the
player-facing visual keys with:

```powershell
.\.venv\Scripts\python.exe tools\gamedriver.py profile visual
```

For a direct player-quality launch through the leased driver:

```powershell
.\.venv\Scripts\python.exe tools\gamedriver.py launch --mode mod --visual-map --no-debug-mode
```

For renderer evidence that must not inherit map-derived state from an old save, use the
bounded fresh-game route:

```powershell
.\.venv\Scripts\python.exe tools\gamedriver.py new-observer --visual-map --session <name>
```

It acquires the same shared session lease, drives Main Menu -> New Game -> country
selection -> live Observer, and records each transition under `docs/screens/<name>/`.
If the slot is occupied it returns the protocol's deferred status without launching or
touching the other project's process.

Fresh-game completion is dual-proven. Normally the driver observes state 4, cache
recalculation completion, and a quiet debug log. If build 24187685 omits or rotates those
markers, five continuous seconds of the calibrated country-selection top bar on the
responsive owned EU5 window release the log wait; the next stage independently requires
the same interactive signature for another five seconds. A menu, loading bar, merely
non-black frame, or window owned by the other project cannot satisfy this fallback.

No vanilla-control cache or background job queue is used. An automatically queued test
could otherwise run against a worktree that changed after submission.
