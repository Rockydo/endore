# ENDÓRË — MASTER PLAN
## A total conversion of Europa Universalis V to Middle-earth on the eve of the War of the Ring

> **Read this document fully once per session start.** It is the single design source of truth
> for the Codex agent executing this project under `/goal`. Precedence when facts conflict:
> **installed game files > the ANTIQVITAS reference repo > this document > your own knowledge.**
> When Tolkien canon conflicts internally, see §4.2 (canon precedence).

---

# PART 0 — MISSION AND PRIME DIRECTIVES

## 0.1 Mission

Build **ENDÓRË**, a complete, polished, lore-faithful total conversion of Europa Universalis V
that recreates north-western Middle-earth on **1 January, Third Age 3018** — the last months
of the uneasy peace, just before the War of the Ring erupts. Gandalf has not yet proven
what Bilbo's ring is. Sauron has declared himself in Mordor and rebuilt Barad-dûr. Saruman
plots in Isengard, still trusted by the Wise. Théoden withers under Gríma's whispers.
Osgiliath's garrison watches the fords. The player takes any realm — Gondor, Rohan, Mordor,
the Woodland Realm, a Haradrim kingdom, the Shire — into the great war and the age that follows.

The bar is: **as detailed as the vanilla game**. A new hand-crafted map at EU5 granularity,
full pop/economy setup, bespoke factions, characters, faiths, goods, advances, events,
situations, missions, and 2D art — with **every anachronism removed or replaced**: no
gunpowder, no printing press, no Reformation, no New World, no Renaissance, nothing that
smells of historical Earth 1337–1836. Reuse vanilla *mechanics* freely where they fit the
setting; replace their *skin, names, art and text* everywhere.

## 0.2 Prime directives (non-negotiable)

1. **Fully autonomous.** There are no human-in-the-loop steps. None. Automate the launcher,
   the console, playtests, screenshots, everything — via the ported gamedriver (§1.2). If
   something resists automation twice, log it in `BLOCKERS.md` with evidence and move on.
   Never wait for, or ask for, user input.
2. **Never write to drive C:.** The repo, the relocated user dir, caches, venv, temp files,
   generated art — all live on `G:\`. The Steam client itself is on C: and is only *run*,
   never modified.
3. **Never edit GAME_DIR** (`G:\SteamLibrary\steamapps\common\Europa Universalis V`). It is
   read-only reference material and the test target.
4. **Never commit red.** `make validate` green before every commit; `make smoke` green before
   every commit that touches game-visible content. Commit **large, coherent batches** — a
   milestone slice, a whole subsystem, a full art set. No drive-by one-file commits.
5. **Zero anachronisms.** §12 and Appendix A are the purge contract. A shipped mod where the
   player can see the word "colonialism", a cannon icon, or a Pope is a failed mod.
6. **Lore accuracy over invention, invention over gaps.** Canon first (§4.2). Where canon is
   silent (populations, minor borders, eastern lands), invent boldly but plausibly, in
   Tolkien's registers, and log every judgement call in `docs/ASSUMPTIONS.md` with a `†`.
7. **Visual authenticity.** Every generated 2D asset must pass a style gate against real
   vanilla EU5 assets (§15). Nothing generic, no cheap warm-yellow AI filter, no flat
   clip-art. If it wouldn't fool a Paradox artist at 128px, regenerate it.
8. **The map is the riskiest system — prove it before ALL else.** ANTIQVITAS kept vanilla
   Earth; you are replacing the planet. By owner's explicit order, milestone M1 ("Proof of
   Arda", §5.4) — a rough Middle-earth-shaped map confirmed in-game by test — is the
   project's first priority and hard gate: no mechanics, factions, or content work of any
   kind before it is green.

## 0.3 What "done" means

The Definition of Done for v0.1.0 is milestone M12 (§18): a player can pick any of the ~38
first-class realms (§8 roster; plus generated minors)
in TA 3018, see a beautiful hand-authored Middle-earth at vanilla-like location density for
the covered extent, play 150 in-game years without a single mod-caused error.log line, watch
the War of the Ring situation resolve one way or another, and never once see a word, icon, or
mechanic that belongs to post-medieval Earth.

---

# PART 1 — ENVIRONMENT AND GROUND TRUTH

## 1.1 Fixed paths (verify with tools/find_game.py at bootstrap; refuse C: installs)

| Thing | Path |
|---|---|
| Game install (READ-ONLY) | `G:\SteamLibrary\steamapps\common\Europa Universalis V` |
| Game exe | `...\Europa Universalis V\binaries\eu5.exe` |
| Game content | `...\Europa Universalis V\game\{in_game, main_menu, loading_screen}` |
| Steam app id | `3450310` |
| **This repo (the mod)** | `G:\endore` |
| Relocated user dir | `G:\endore_user_data` (created via `--user_dir=`) |
| Junction the game reads | `G:\endore_user_data\mod\endore` → `G:\endore` |
| Reference repo (READ-ONLY) | `G:\antiqvitas` — the completed 1 AD total conversion |
| Reference user dir | `G:\antiqvitas_user_data` (do not touch; study only) |

The game version to declare in metadata: read the installed build the way ANTIQVITAS does
(`docs/ENGINE_FACTS.md` there records `1.3.11`, checksum "Pavia"); re-verify at bootstrap,
do not copy blindly.

## 1.2 The ANTIQVITAS reference repo — your quarry, not your prison

`G:\antiqvitas` is a finished, working EU5 total conversion (Earth, AD 1–476) built by an
agent under the same constraints as you. **Read `G:\antiqvitas\AGENTS.md`,
`docs\ANTIQVITAS_MASTER_PLAN.md`, `docs\ENGINE_FACTS.md`, `docs\BLOCKERS.md` skim, and
`tools\` in your first session.** It has already solved: game discovery, mod junction +
playset activation without the launcher, autonomous game driving on this exact machine
(French keyboard scan codes, DX12 quirks, Steam DRM), the error.log-diff smoke test with a
vanilla control, the BOM/encoding matrix, DDS conversion contracts, and the `--check/--write`
generator pattern. **Port these tools; do not reinvent them.** Copy, rename, strip the
Roman-specific parts, keep the architecture.

Also under `G:\antiqvitas\external\` (read-only clones): `eu5-1444-start-date` (precedent for
moving the start date — you are moving it to year 3018) and `eu5-modding-mcp` (EU5 modding
documentation server; mine its docs corpus directly as files if running it is inconvenient).

What ANTIQVITAS **did not do** — where you are on your own:
- **A custom map.** Its `in_game/map_data/` holds only `location_templates.txt`. You will
  author the full `map_data` + terrain stack (§5). Budget the most engineering care here.
- A fantasy setting: multi-species pops, magic-adjacent mechanics, invented toponymy.
- Start-date year far outside vanilla range in the *future* direction (3018+). The
  1444-start-date mod and ANTIQVITAS (year 1) prove the year is a free variable; verify
  early that year 3018 and an end date near 3160 behave (M1).

## 1.3 Tooling

Mirror the ANTIQVITAS stack: Python venv at `G:\endore\.venv` (Pillow, numpy, PyAutoGUI,
psutil — copy `requirements.txt` and pin), `.tools\ImageMagick\magick.exe` and
`.tools\DirectXTex\texconv.exe` copied from `G:\antiqvitas\.tools\` (they are gitignored
there; copy the binaries, don't re-download), `make.cmd` + `Makefile` delegating to
`tools/run_checks.py`. `gh` CLI is available and authenticated for github.com/Rockydo.

Image generation: you (Codex) have native GPT-Image generation. Protocol in §15 — it is
strict about style references and 4-up sheet generation.

---

# PART 2 — BOOTSTRAP (Milestone M0, first sessions)

Do these in order; each is a `--check`-able state.

1. **Repo.** `git init` at `G:\endore`, default branch `main`. Copy and adapt from
   ANTIQVITAS: `.gitignore` (venv, .tools, .cache, .tmp, runtime baselines, external,
   `*.log` except committed baselines), `.gitattributes` (no LFS — DDS/PNG at this scale
   committed directly, matching ANTIQVITAS), `make.cmd`, `Makefile`, `requirements.txt`.
   Create `docs/` with: this file (copy verbatim as `docs/ENDORE_MASTER_PLAN.md`),
   `PROGRESS.md`, `TODO.md`, `DECISIONS.md`, `ASSUMPTIONS.md`, `ENGINE_FACTS.md`,
   `BLOCKERS.md`, `KNOWN_ISSUES.md`, `CREDITS.md` (crediting Tolkien's works as the source
   material, the film trilogy as visual inspiration, ANTIQVITAS as engineering base; state
   plainly this is a non-commercial fan work). Write `AGENTS.md` at root — adapt the
   ANTIQVITAS 13-liner, pointing at this plan.
2. **GitHub remote.** `gh repo create Rockydo/endore --public --source G:\endore --push`
   (same general config as `Rockydo/antiqvitas`: public, `main`, no LFS). If `gh` auth is
   missing, log a blocker and continue locally; retry each session — never stall on this.
3. **Ported toolchain.** Port from `G:\antiqvitas\tools\`: `find_game.py`, `link_mod.ps1`,
   `steam_ensure.ps1`, `enable_mod.py` (playsets.json writer — playset name `ENDORE`),
   `gamedriver.py`, `smoketest.py`, `runtime_state.py`, `pdxlint.py`, `dds.py`,
   `asset_manifest.py`, `extract_vanilla.py`, `run_checks.py`. Adaptations:
   - all `antiqvitas` literals → `endore`; user dir `G:\endore_user_data`.
   - playset DLC set: decide deliberately which DLC entries to enable (ANTIQVITAS enables
     `d000_shared` + the ancient-monuments pack, disables the rest — monuments machinery
     is attractive for Orthanc/Barad-dûr/the Argonath §10.2). Record the choice + why in
     DECISIONS.md and encode it in the ported `enable_mod.py`.
   - `pdxlint.py` date window: accept content years **2800–3200** (matching §4.4's policy;
     backstory anchors reach to 2941) instead of AD 1–476; biography/birth years bounded by
     the empirically verified engine minimum. Keep the BOM matrix exactly (it is engine
     law, not an ANTIQVITAS choice).
   - Keep the vanilla-control smoke design and `baselines/` layout unchanged.
4. **Mod skeleton.** `.metadata/metadata.json`: name `ENDÓRË`, id `endore`, version `0.1.0`,
   supported_game_version as verified, short_description mentioning "Middle-earth total
   conversion, TA 3018", tags `["Total Conversion", "Fantasy"]`. Thumbnail: generated per
   §15 (One Ring motif over a parchment map, EU5 UI painting style), exactly 512×512,
   <1 MB, at both `.metadata/thumbnail.png` and root `thumbnail.png`. Content roots:
   `in_game/`, `main_menu/`, `loading_screen/` mirroring vanilla's layout.
5. **Green baseline.** Run vanilla smoke to capture `baselines/vanilla_error.log`; junction +
   playset the empty skeleton mod; `make smoke` must pass with zero new lines. Record
   engine facts learned (`docs/ENGINE_FACTS.md`). **Commit: `feat(bootstrap): ...` — this is
   the only permitted small-ish commit of the project.**

---

# PART 3 — THE OPERATING LOOP

```
Loop: read docs/TODO.md → pick top unblocked task → implement as a large coherent batch
      → make validate (green) → if game-visible: make smoke (green) → for milestone ends:
      driver-run in-game verification (observer run + screenshots + in-game tests §16)
      → commit the batch → push → update PROGRESS/TODO (+ DECISIONS/ASSUMPTIONS if judged)
      → next task. Blocked twice → BLOCKERS.md with evidence → next task.
```

**Session-start ritual**: re-read this plan; check the installed game build id against
`docs/ENGINE_FACTS.md` — if Steam auto-updated EU5, re-capture the vanilla error.log
baseline, delta-check ENGINE_FACTS, bump `supported_game_version`, and log it in
DECISIONS.md before any content work.

**Cadence contract** (the user explicitly wants speed with checkpoints, not test-thrash):
- `make validate` (static, no game launch, seconds-to-minutes): run freely while working,
  and **mandatorily before every commit**.
- `make smoke` (real game launch to menu, minutes): **only before commits** that change
  game-visible content, not during exploratory editing.
- Tier-3 in-game verification (observer runs, in-game test scripts §16, screenshot review):
  at **milestone boundaries** and after map/setup overhauls.
- Commits: **large batches only** — "the Rohan mission tree + its art + loc" is one commit;
  "the entire pop census for Eriador" is one commit. Conventional Commits style, terse,
  scope-tagged: `feat(map): ...`, `feat(world): ...`, `feat(art): ...`, `fix(smoke): ...`.
  Push to `origin main` after every commit (the remote is the off-site backup).
- Every historical/lore claim in content gets a source (book + chapter) in the generator's
  data tables or a `†` entry in `docs/ASSUMPTIONS.md`.

**Generators over hand edits.** Follow the ANTIQVITAS pattern: bulk content (map hierarchy,
pop censuses, location names, icon sets) is emitted by Python generators in `tools/` from
explicit data tables, each with `--write` and `--check`; every `--check` is registered in
`tools/run_checks.py` so `make validate` re-verifies the whole world forever. Hand-write only
genuinely bespoke script (events, situations, missions).

---

# PART 4 — WORLD CANON

## 4.1 The moment: 1 January, Third Age 3018

The start date sits in the taut year before open war — after Gandalf's seventeen years of
doubt, before the assault on Osgiliath (June 3018). State of the world the setup must encode:

- Sauron declared himself in **2951**; Barad-dûr is rebuilt, Mount Doom burns, Mordor teems.
  Three Nazgûl hold **Dol Guldur**; Minas Morgul (Witch-king) has held Gondor's east bank
  hostage for centuries; **Ithilien is emptied** (last inhabitants fled 2954) — a no-man's-land.
- **Saruman** seized Isengard as his own (2953), used the Orthanc palantír (~3000) and is
  secretly Sauron's rival-servant. Publicly he is still head of the White Council. His
  Uruk-hai breeding and Dunland agitation are underway but hidden (start him formally
  non-aligned, with hostile-to-Rohan opinion drift and scripted treachery, §13).
- **Gondor**: Steward Denethor II (since 2984), no King for 968 years. Boromir (b. 2978)
  and Faramir (b. 2983) lead its captains. Osgiliath a ruined fortified crossing. Pelargir,
  Dol Amroth, Lossarnach etc. are its fiefs. Umbar corsairs raid the coasts.
- **Rohan**: Théoden King (since 2980), sunk in decline under **Gríma's** counsel (start:
  ruler incapacitated modifier, Saruman spy-network events). Théodred and Éomer marshal
  the Mark. Orc raids on the Westfold are rising.
- **The Shire**: fat, oblivious, guarded secretly by the **Rangers of the North**. Frodo
  holds the Ring (hidden flag; nobody knows, §13.2). Bilbo dwells in Rivendell.
- **Eriador** else: Bree-land tiny and sleepy; Rivendell (Elrond) and the Grey Havens/Lindon
  (Círdan) fading but potent; Tharbad ruined; Angmar long fallen but **Mount Gram, Goblin-town
  and Gundabad** orcs infest the mountains; **Moria** is an orc-hold over Durin's Bane
  (Balin's colony destroyed 2994 — a fresh wound for Erebor).
- **Wilderland**: Woodland Realm (Thranduil) besieged by Mirkwood's darkness spreading from
  Dol Guldur; **Lothlórien** (Galadriel & Celeborn) sealed and timeless; Beornings hold the
  Carrock and High Pass tolls; Woodmen in western Mirkwood; **Erebor** (Dáin II Ironfoot) and
  **Dale** (King Brand) prosperous allies; Esgaroth a merchant republic; **Dorwinion** vineyards
  by the Sea of Rhûn.
- **The East and South**: Rhûn's Easterling confederations and Khand's Variags are mustering
  under Sauron's envoys; Near Harad's kingdoms (old Númenórean-tinged Umbar among them) owe
  him fealty or tribute; Far Harad musters mûmakil. These are playable, fleshed-out realms
  (§8), not painted wastes — canon is thin here, so invent richly per §4.3.
- Aragorn ranges as **Strider**; Gollum sits captive in Thranduil's halls (event fuse);
  Gandalf rides between Bree, the Shire and Minas Tirith's archives.

Timeline anchors the mod scripts against (for scheduled/probabilistic events, §13):
2941 Five Armies · 2951 Sauron declares · 2953 Saruman takes Isengard · 2994 Balin's colony
destroyed · 3000 Saruman ensnared via palantír · 3001 Bilbo's party · 3009–3017 hunt for
Gollum · 3017 Gollum freed, caught by Aragorn, held by Thranduil · **3018.6 assault on
Osgiliath; attack on Thranduil; Gollum escapes** · 3018.9 Black Riders in Eriador; Frodo
departs · 3018.10 Council of Elrond · 3018.12 Fellowship departs · 3019.1 Moria/Durin's Bane ·
3019.3 Helm's Deep, Ents take Isengard, Pelennor Fields, Black Gate, **3019.3.25 Ring
destroyed** · 3019.5 Aragorn crowned · 3019.11 Scouring of the Shire · 3021 Ring-bearers sail,
Fourth Age begins.

## 4.2 Canon precedence

1. *The Lord of the Rings* text + Appendices (incl. the Tale of Years) — binding fact.
2. *The Hobbit*, then *Unfinished Tales* / *The Silmarillion* / HoME — binding where not
   contradicted by (1).
3. The Peter Jackson trilogy — **aesthetic and mood reference only** (armor silhouettes,
   architecture vibes, palettes), never for facts, dates, or invented characters (no film-only
   characters as content; a hidden easter egg is acceptable).
4. Other adaptations/games — ignore.

Write all player-facing text in Tolkien's register (§14). This is a non-commercial fan work;
never copy any published text, map scan, or film frame into the repo — everything is restated,
redrawn, regenerated.

## 4.3 Assumption policy

Canon is silent about most numbers this game needs (populations, harvest yields, army sizes,
eastern polities). Decide like a good DM: extrapolate from canon hints (Gondor can field
armies in the low tens of thousands; the Shire ~lots of small villages; Mordor's Nurn feeds
its hosts with slave-fields), from medieval-Europe analogues, and from gameplay balance.
Every such call: one line in `docs/ASSUMPTIONS.md` with a `†` and the reasoning. Never let a
missing fact block a milestone — invent, log, move on.

## 4.4 Calendar and dates

- Engine year = Third Age year. **Start 3018.1.1**; end date **3200.1.1** (Fourth Age 179 —
  display stays simple; localize era text as "Third Age" and let the epilogue ages of §12
  reframe post-3021 as the Fourth Age narratively). Verify both bounds in M1 and record in
  ENGINE_FACTS; the `eu5-1444-start-date` clone shows the technique.
- `tools/pdxlint.py` date window: 2800–3200 for content dates; character birth years may go
  lower — set the linter's biography window from the empirically verified engine minimum.
- **Immortals** (Elves, Sauron, Nazgûl, wizards, Ents): test engine support for
  immortality/no-natural-death (traits/defines/character flags) in the M1 spike. If unsupported, give
  them birthdates yielding dignified ages plus scripted death-prevention and age-display loc.
  Mortal long-livers (Dúnedain, Dwarves, Hobbits) get lifespan-extending traits (§9).
  Record whichever mechanism works in ENGINE_FACTS and standardize.

---

# PART 5 — THE MAP (the crown jewel and the critical path)

## 5.1 Extent and scale

Covered extent — the classic north-west, generously margined: **west** Forlindon/Harlindon
coasts; **north** the Icebay of Forochel, Carn Dûm, the Grey Mountains and Withered Heath;
**east** past the Sea of Rhûn to include Dorwinion and the western Rhûn steppes (playable
Easterlings); **south** through Near Harad past Umbar to a northern-Far-Harad fringe
(mûmakil country). Beyond-edge lands (deep Rhûn, deep Harad) are handled by the map border,
not painted wasteland.

Canvas: `locations.png` **8192×4096** RGB (half vanilla, which is 16384×8192 for the whole
planet — our extent is a subcontinent; this gives *denser* pixels-per-mile than vanilla).
Heightmap 16-bit grayscale at the vanilla locations:heightmap ratio (vanilla: 16384×8192 vs
8192×4096, i.e. 2:1 — so ours 4096×2048), **unless** the M1 spike shows the engine wants
another relationship; engine evidence wins. Vanilla `map_data/default.map` declares the
authored file set and is your contract:
`provinces = "locations.png"`, `rivers = "rivers.png"`, `topology = "heightmap.heightmap"`,
`adjacencies`, `setup = "definitions.txt"`, `ports.csv`, `location_templates.txt`, plus
`equator_y` and **`wrap_x = yes`** — set `wrap_x = no` for Middle-earth (verify in the M1
spike) and pick an `equator_y` well south of the canvas (Harad is subtropical; Forodwaith
arctic). `nodes.dat` (11 MB binary) and `generated_locators_port.txt` are the prime
"derived?" suspects for the spike (§5.4).

Target: **≈4,500–6,000 land locations** (count vanilla's `definitions.txt` for calibration —
match vanilla *Europe's* density in settled lands: the Shire alone ≈ 12–18 locations, Gondor's
fiefs each a province, Mordor's Udûn/Gorgoroth/Nurn distinct). Wilderness (Forodwaith,
Enedwaith, deep Mirkwood) sparser but never single-blob. Impassable ranges and dead zones
(the high Misty Mountains, Ephel Dúath crests, the Dead Marshes as near-impassable wetland)
carve the strategic geography: **the passes must matter** — Redhorn Gate, High Pass,
Gap of Rohan, Cirith Ungol, the Morannon, the Paths of the Dead as a scripted route (§13).

## 5.2 Geographic hierarchy

`definitions.txt` nesting (continent → region → area → province → locations), e.g.:

```
eriador = {
  arnor_region = {
    shire_area = {
      westfarthing_province = { hobbiton bywater michel_delving waymeet tuckborough ... }
      ...
    }
    breeland_area = { ... } ...
  }
  lindon_region = { ... } rhudaur_region = { ... } ...
}
rhovanion = { anduin_vale_region, mirkwood_region, dale_region, brown_lands_region ... }
gondor = { belfalas_region, anorien_region, ithilien_region, ... }
mordor = { udun_region? — or mordor as region under a southlands continent; decide & log }
harad  = { umbar_region, near_harad_region, far_harad_region ... }
rhun   = { dorwinion_region, sea_of_rhun_region, ... }
forodwaith = { ... }
```

Continent split proposal: `eriador`, `rhovanion`, `gondor` (incl. Rohan? no — Rohan under
`rhovanion` or its own region under `gondor`... decide by strategic-UI usefulness, log the
call), `mordor_and_rhun`, `harad`. Keep it navigable in map modes; mirror how vanilla sizes
regions/areas.

Naming: every canonically named place is an anchor (several hundred across the texts and the
book map). All fill locations get invented names from per-culture lexicons (§14.3) —
Sindarin in elven/Gondorian lands (with Westron doublets where canon does it: Imladris/
Rivendell), Rohirric (Old-English-flavored) in the Mark, Hobbitish homeliness in the Shire,
harsh Black Speech/Orkish in Mordor, Haradric and Easterling coinages from the scant canon
seeds (log constructed-language conventions in `docs/world/lexicons/`).

## 5.3 Production pipeline (generator-driven, like everything else)

1. **Control layers** (`docs/world/control/`, committed): authored vector/raster layers —
   coastline, elevation ridge splines, river polylines with widths, biome/climate zones,
   realm borders, and a `settlements.csv` of every anchor (name, culture, realm, rank,
   x,y on the canvas, source citation or †). Geometry is *restated from lore knowledge*
   (relative positions, travel times in the text) — never traced from a scanned published map.
   The Anduin, Misty Mountains, White Mountains, Mirkwood must land where every reader
   expects them.
2. **Derivation generators** (each `--write`/`--check`, registered in `make validate`):
   - `gen_heightmap.py`: ridge splines → mountain masses; biome-based base elevation; fBm
     detail; river valleys incised; 16-bit source PNG, packaged into the engine's
     `heightmap.heightmap` topology format (reverse the vanilla file's container in the M1
     spike; `gfx/terrain2/heightmap.png` 8192×4096 16-bit is its visible sibling). Mount
     Doom, the Argonath gorge, Helm's Deep valley get hand-tuned masks.
   - `gen_rivers.py`: vanilla `rivers.png` palette conventions (copy exact indexed colors/
     source-marker pixels from vanilla; document in ENGINE_FACTS) — trace Anduin, Baranduin,
     Greyflood, Bruinen, Isen, Entwash, Celduin, Carnen, Harnen, Poros et al.
   - `gen_locations.py`: Poisson-disc seeds weighted by a density map (anchors pinned) →
     Voronoi → unique RGB per location, hard edges (no anti-aliasing — one stray blended
     pixel breaks the map; check for it), min-area enforcement, islands/lakes handled.
   - `gen_definitions.py`: emits `definitions.txt` hierarchy + `named_locations` + per-location
     data stubs; cross-checks every RGB ↔ entry bijectively.
   - `gen_location_templates.py`: emits `map_data/location_templates.txt` — the per-location
     assignment of `topography`, `vegetation`, `climate`, `culture`, `religion`,
     `raw_material`, `natural_harbor_suitability` (see the ANTIQVITAS/vanilla one-line-per-
     location format). This single file is where §6 (peoples), §7 (faiths) and §10 (goods)
     meet the map; generate it from the control layers + the realm/pop censuses so all
     three stay consistent. Climate spectrum: Forodwaith arctic → Eriador/Rhovanion
     continental/oceanic → Gondor mediterranean-like → Harad arid; vegetation: Mirkwood,
     Fangorn, the Old Forest dense forest; Mordor ash-waste; the Dead Marshes wetland.
     Any engine-side `gfx/map` biome masks discovered in the spike get their own generator.
   - `gen_adjacencies.py`: fords (Tharbad, Fords of Isen, Sarn Ford), ferries (Buckleberry),
     straits; `ports.csv` for Grey Havens, Pelargir, Dol Amroth, Umbar, Esgaroth (lake!) etc.
   - Flatmap/paper-map texture (`gfx/map/flatmap`): render from height+biome in the vanilla
     parchment style (sample vanilla's flatmap for palette; §15 style gate applies).
3. **Water**: the Sea (Belegaer) west, Sea of Rhûn & Núrnen inland, navigable lower Anduin if
   the engine models river navigation — check vanilla's approach and mirror it.

## 5.4 M1 — "PROOF OF ARDA" (the project's absolute first priority)

**Owner's explicit directive: nothing else — no mechanics, no factions, no content of any
kind — begins until a basic world map in the rough shape of Middle-earth loads in-game and
passes an in-game verification. This is the go/no-go gate for the entire project; reach it
as fast as possible.** After M0's minimum bootstrap (just enough repo+toolchain to launch
and smoke-test), all effort goes here.

The M1 deliverable is a **crude but unmistakable Middle-earth**: ~150–400 locations, the
recognizable silhouette — Lindon/Belegaer coast, the Bay of Belfalas, the Misty Mountains
spine, the White and Grey Mountains, Mordor's mountain box, Mirkwood's mass, the Anduin —
with placeholder names allowed everywhere, one dummy tag owning something, and zero care
for balance or beauty. Verification: `make smoke` zero-new-lines, PLUS a gamedriver
map-screen screenshot series showing the shape, PLUS one trivial in-game test (§16.3
framework) executing on this map. Debug stepping-stones on the way (use as needed, throw
away): a rescaled vanilla map; a tiny synthetic island world.

Along the way, prove empirically and record in ENGINE_FACTS:
- Which `map_data/` + `gfx/terrain2` + `gfx/map` files are **authored** vs **derived/baked**
  by the engine or its editor (`nodes.dat`, `generated_locators_port.txt`,
  `location_templates.txt` — the names suggest generation; find the generating pathway. EU5
  ships editor/CLI capabilities — investigate `-mapeditor`-style switches, `binaries/`,
  the modding docs corpus in the MCP clone, and how the game reacts to their absence).
- Whether a **different canvas size** than vanilla loads (try a scaled-down vanilla first,
  then a synthetic 100-location island world).
- Non-wrap behavior, start year 3018, end year 3200 (piggyback on the same spike build).
- Minimum viable file set for a loadable custom map, and every error.log signature map
  errors produce (these become lint rules).
- **The dangling-reference blast radius**: a custom map invalidates every vanilla file that
  names vanilla locations/areas/tags — `scripted_geography`, `area_preferences`,
  `ai_scripted_expansion_target/score`, `holy_sites`, `missions`, `formable_countries`,
  `historical_scores`, `situations`, scenarios/bookmarks, achievements. ANTIQVITAS never
  faced this (it kept the map). Enumerate the error signatures dangling references produce
  and build the **geography-reference quarantine sweep** (empty/neutralizing overlays for
  all such vanilla files) — it is part of the M2 gate, not a M12 afterthought.
- If `nodes.dat`/locators turn out to be baked only by an interactive in-game map editor,
  **automating that editor via gamedriver is in scope** — exhaust it before touching the
  §19 fallback ladder.
- Prove one trivial in-game test (`common/tests` framework, §16.3) runs under observer mode
  and reports parseably — the M10 gate depends on this assumption; verify it now.
The M1 map's *content* is throwaway (M2 regenerates everything through the real pipeline);
the knowledge, the generators' skeletons, and the green gate are the deliverables. Do not
start §5.3 mass production — or any other Part of this plan — before the M1 gate is green.

---

# PART 6 — PEOPLES: CULTURES, LANGUAGES, POPS

EU5's chain is `culture → language → language_family` plus `culture → culture_group`
(formats: see ANTIQVITAS `in_game/common/cultures/antq_m4_cultures.txt`, `languages/`,
`culture_groups/`). **Race is modeled as culture group** — it is the cleanest fit for pops,
and the group level carries shared traits via scripted triggers/modifiers.

## 6.1 Culture groups (≈ races/kindreds) and cultures

Prefix everything `me_`. Proposed roster (adjust counts to map needs; log changes):

- **me_dunedain_group** (High Men): `me_gondorian` (mainline), `me_dol_amrothian`
  (Belfalas, elvish strain), `me_ithilien_ranger`? (no — rangers are a pop/estate flavor,
  not a culture), `me_arnorian` (Rangers of the North, Bree-blended Dúnedain),
  `me_black_numenorean` (Umbar elite).
- **me_northmen_group** (Middle Men of the North): `me_rohirric`, `me_dalish` (Dale/Esgaroth),
  `me_beorning`, `me_woodman` (western Mirkwood), `me_lakeman`? (fold into dalish; log),
  `me_eriadoran` (Bree-land & lowland commons), `me_dorwinrim` (Dorwinion).
- **me_middle_men_group** (unaligned Men): `me_dunlending`, `me_enedwaith_folk`?,
  `me_lossoth`, `me_druedain` (their own tiny group if trait divergence warrants; log).
- **me_southron_group**: `me_near_haradrim`, `me_far_haradrim`, `me_umbarite` (corsair
  commons), `me_khandish` (Variags).
- **me_easterling_group**: `me_rhunnic_balchoth`, `me_rhunnic_wainrider` descendants —
  name 2–3 concrete peoples (invented, †-logged, canon-seeded: Balchoth, Wainriders).
- **me_hobbit_group**: `me_shire_hobbit`, `me_bree_hobbit` (Stoor/Harfoot/Fallohide are
  pre-blended by TA 3018 — flavor text only).
- **me_elven_group**: `me_noldor` (Rivendell/Lindon high elves), `me_sindar` (Thranduil's
  court, Grey Havens), `me_silvan` (Woodland Realm & Lórien commons), `me_galadhrim`
  (Lórien — or Silvan + realm flavor; decide, log).
- **me_dwarven_group**: `me_longbeard` (Durin's Folk: Erebor, Iron Hills, exiles),
  `me_firebeard_broadbeam` (Ered Luin), `me_eastern_dwarf` (far-eastern clans fringe, if
  the map's edge holds any hold; else cut).
- **me_orc_group**: `me_mordor_orc`, `me_mordor_uruk` (fold? one `me_mordor_orc` with unit
  flavor is acceptable; log), `me_isengard_uruk` (bred new — tiny at start, grows via
  Isengard mechanics §13), `me_misty_orc` (Moria/Goblin-town/Gundabad), `me_northern_orc`
  (Grey Mountains/Mount Gram — fold into misty if thin).
- **me_troll_group**? No: trolls are units/flavor, not pops. **me_ent_group**: single
  `me_onodrim` culture for Fangorn's handful of pops (non-growing; scripted).

## 6.2 Languages and families

`language_families`: `me_eldarin_family` (Quenya†, Sindarin, Silvan dialect), `me_mannish_family`
(Westron + Rohirric + Dalish + Haradric… — canon makes most Mannish tongues related;
Haradric/Easterling distinctness † as separate families if gameplay wants it),
`me_khuzdul_family`, `me_black_speech_family` (Black Speech + Orkish dialects).
Languages carry the **name pools** (male/female/dynasty) — this is where the per-culture
lexicons (§14.3) plug in; populate generously (60+ male, 40+ female, 30+ dynasty/house names
per major language, canon names first, invented fills in-register).

## 6.3 Pops and the census

World start lives in `main_menu/setup/start/` mirroring ANTIQVITAS's numbered start-file
layout (02–27; `06_pops.txt` `define_pop` blocks per location; `21_locations.txt`
micro-seeds). Every start file gets a deliberate verdict — the less obvious ones:
`16_wars.txt` (GON–MOR are **not** formally at war on 3018.1.1 — cold-war raiding via
events until §13.1 Phase II), `19_diseases.txt` (seed only §12's reskinned diseases),
`22_situations.txt` (seed the War of the Ring situation §13.1), `23_colonies.txt`
(**empty** — no colonization, §12), `26_ai_personalities.txt` (per-realm temperament:
leash-held MOR, passive LOR/RIV/FAN, raider UMB/KHA), `25_area_preferences.txt`,
`24_town_rights.txt`, `14_development.txt` (align with the census).
Pop types: reuse vanilla types (nobles/clergy/burghers/peasants/laborers/soldiers/tribesmen)
but **relocalize** (§14): clergy → "Loremasters & Keepers", tribesmen → "Wild Folk", etc.
Census principles (all †-logged in one `docs/world/census_notes.md`):
- Total northwest population in the low millions. Gondor the largest Free realm
  (order 1.5–2.5M), Rohan ~0.5M, the Shire ~150–300k hobbits, Eriador else sparse.
  Mordor: orc hosts (1M+?) plus **Nurn slave-fields** (Mannish slave pops — use a
  slave/serf pop type if vanilla has one; else laborers + modifiers). Harad/Rhûn together
  outnumber Gondor (the East is vast) but most of it lies off-map — encode only the on-map
  share. Elves few and potent (Rivendell a few hundred; Lórien and the Woodland Realm low
  tens of thousands); Dwarves tens of thousands in Erebor/Iron Hills.
- Racial demography drives literacy/pop-type splits: elven pops skew to elite/lettered
  types; orc pops to soldiers/laborers; the Shire nearly all peasants/burghers with
  comically low soldiers.
- Empty is content too: Hollin/Eregion, Enedwaith, the Brown Lands, Ithilien carry ruins
  modifiers (§10.4) and near-zero pops — the desolation must read on the pop map mode.

---

# PART 7 — FAITHS (the religion layer, de-churched)

Middle-earth has no churches; it has allegiances of the spirit. Reskin the religion system
accordingly (format: ANTIQVITAS `antq_m4_religions.txt` + `religion_groups`). Purge every
vanilla religious mechanic name (papacy, reformation, holy sites CAN be reused as concept —
renamed) per Appendix A. Proposed set (`me_` prefix):

**Group me_free_faiths** ("The Light of the West"):
- `me_valar_worship` — "The Old Faith of the West" (Elves, Dúnedain, faithful Númenórean
  descent). Religious aspects → **Valar venerations** (Elbereth/Varda, Manwë, Ulmo, Aulë,
  Oromë, Yavanna, Mandos, Estë…) using the aspects/`gods` subsystem for picks.
- `me_mahal_cult` — "The Making of Mahal" (Dwarves: Aulë + ancestor-veneration of Durin).
- `me_northern_ways` — "The Free Ways" (Rohirrim, Dalish, Beornings, Woodmen, hobbits†:
  hearth-customs, no temples; hobbits may instead get their own `me_hearth_ways` if flavor
  pays for it; log).
**Group me_shadow_cults** ("The Shadow"):
- `me_sauron_cult` — "Worship of the Eye" (Mordor's orcs, Black Númenóreans, the
  Sauron-cowed East/South elites): dark tribute, terror mechanics via aspects.
- `me_melkorism` — "The Black Devotion"† (older Morgoth-rooted cults of Rhûn/Harad
  hinterlands) — distinct so the East isn't a monolith and conversion play exists.
**Group me_old_ways**:
- `me_dunland_ways` (ancestor-grudge folk religion), `me_lossoth_ways` (snow-shamanism)†,
  `me_druedain_ways` (watch-stones and wood-sense)†, `me_southron_ways` (Harad folk cults
  under Sauron's overlay — majority commons faith in Harad; their elites hold
  `me_sauron_cult`, which makes Harad *reclaimable* by a liberating Gondor).

Mechanics mapping: religious_influence → "Spiritual Sway"; omens (ANTIQVITAS shows the
subsystem) → "Blessings/Auguries" for Free faiths, "Dark Offerings" for Shadow; holy sites →
**Places of Power** (Meneltarma-facing Hallow of Minas Tirith†, the Grey Havens, Cerin Amroth,
Amon Hen's Seat of Seeing, the Sammath Naur, Mount Gundabad (dwarven holy site under orc
boots — a war-goal that writes itself), the White Tree). Conversion is slow and war-driven;
elves never convert (trigger-block it).

---

# PART 8 — REALMS (the tag roster)

Tag file: `in_game/setup/countries/me_00_world.txt` (ANTIQVITAS format: 3-letter tag,
color/color2, culture_definition, religion_definition, is_historic). COA per §15.6;
ownership via `own_control_core` lists in `10_countries.txt`. ~38 first-class realms below
(+ generated micro-tags where the map wants texture — Harad city-kings, Rhûn hordes).
For each, the setup encodes: government & reform (§12, governments bullet), ruler & court (§9), diplomacy
(§8.2), starting armies (`27_armies.txt`), markets (`03_markets.txt`), IO membership (§13.4).

**The West (Free Peoples):**
| Tag | Realm | Notes at 3018.1.1 |
|---|---|---|
| GON | Gondor | Steward-regency government (unique reform line, §12 governments bullet); fiefs as internal estates; Dol Amroth (DAM) a loyal subject-vassal; at cold war with Mordor; Ithilien contested-empty; garrisons at Osgiliath/Cair Andros. |
| DAM | Dol Amroth | Subject of GON (personal-fealty subject type), Prince Imrahil. |
| ROH | Rohan | Théoden incapacitated (Gríma modifier chain); Westfold raided; oath of Eorl with GON (scripted alliance that CANNOT be broken by AI while both Free). |
| SHI | The Shire | Pacifist smallholder realm; Thain + Mayor government flavor; guarded by RAN (hidden protection mechanic §13.2); absurdly low army cap, high food. |
| BRE | Bree-land | Four-village free league; crossroads market. |
| RAN | Rangers of the North | Tiny realm of the Angle†; Aragorn ruler; special: cheap elite units, huge diplomatic web (Elrond fosterage), Reunited Kingdom formable. |
| RIV | Rivendell (Imladris) | Council government; Elrond; Vilya hidden modifier†; sanctuary mechanics (hosts quest events). |
| LIN | Lindon & the Grey Havens | Círdan; the Havens port (departure of the Elves drain mechanic §13.6). (Narya is Gandalf's — he has borne it since ~TA 1000; model it as a hidden Gandalf-character modifier, not a LIN asset.) |
| BLU | Ered Luin Halls† | Firebeard/Broadbeam + Durin's-folk-exile mining holds in the Blue Mountains (Thorin's old halls); quiet, trade-tied to LIN and the Shire. |
| LOR | Lothlórien | Galadriel & Celeborn co-rule; Nenya veil: near-impassable borders to Shadow until events; timeless-decline mechanics. |
| WOO | The Woodland Realm | Thranduil; besieged-by-forest darkness; holds Gollum (event fuse); wine trade with Dorwinion/Esgaroth. |
| ERE | Erebor | Dáin II; mountain-hold economy (mithril-less but gold-rich); Moria reclamation mission line (Balin grief). |
| IRO | Iron Hills | Longbeard cadet realm, ERE's permanent ally/subject†(choose subject type; log). |
| DAL | Dale | King Brand; twin-city trade with ERE; first target of Rhûn's storm (scripted 3019 Easterling invasion §13). |
| ESG | Esgaroth | Lake-town **Free League** (elected Master; town-moot; §14.2 terminology rulings apply — never the word "republic"). |
| BEO | The Beornings | Carrock toll-lords; shapechanger ruler line (trait); honey/fur economy. |
| WDM | Woodmen of Mirkwood | Forest cantons, spider-haunted borders. |
| DOR | Dorwinion | Wine oligarchy on the Sea of Rhûn; neutral trade pivot between DAL/ESG and Rhûn — survives by balance (mission line: pick a side or profit). |
| FAN | Fangorn | The Onodrim. Non-expansionist tree-realm: cannot be diplomacy'd normally, awakens by event (§13.5) into a briefly unstoppable army. |
| DRU | Drúadan Forest | Ghân-buri-Ghân's folk; hidden paths (Stonewain Valley event for the Pelennor). |
| LOS | Lossoth of Forochel | Ice-bay survivors; totally detached from the war unless dragged. |
| RHO | Rhosgobel† | Radagast's vale: one-location wizard hermitage, event-flavor realm. |

**The Shadow:**
| Tag | Realm | Notes |
|---|---|---|
| MOR | Mordor | Sauron (immortal ruler, never dies except by Ring destruction); government "Dominion of the Eye"; Minas Morgul & the Morannon as fortress-locations; Nurn slave agriculture; Nazgûl as generals; overwhelming but leash-held until the war situations fire. |
| DOL | Dol Guldur | MOR subject in Mirkwood (Khamûl); pressure on WOO/LOR; scripted to strike Lórien thrice in 3019. |
| ISE | Isengard | Saruman: starts formally neutral/White-Council; secret-alignment mechanic flips it Shadow by event window 3018–3019 (§13.3); uruk-hai unit line unlocks on the flip; subverts ROH via Gríma events and DUN feudal calls. |
| MIN | Minas Morgul | Fold into MOR as location+modifier (preferred) or subject tag; decide in **M3, before ownership painting**, log. |
| MOA | Moria | Orc-hold; **Durin's Bane** — any army entering the Deeps risks the Balrog event (army-shattering); blocks the Redhorn passage economy. |
| GUN | Gundabad | Northern orc capital; threatens ERE/DAL from the north (scripted to join the 3019 storm). |
| GOB | Goblin-town & the High Pass | Toll of a darker kind; raids Beornings/Bree-roads. |
| UMB | Umbar | The **Brotherhood of Captains** (corsair council, dark mirror of ESG); raids GON's coast; fleet-heavy. |
| HNE | Harnendor (Near Harad)† | The great Haradrim kingdom behind the Poros; mûmakil; sworn to the Eye. |
| HFA | Far Harad† | Mûmakil-lords of the far south fringe. |
| KHA | Khand | Variag horse-and-axe culture; opportunist raiders (can defect from Sauron if he stumbles — make the Shadow coalition brittle-if-losing). |
| RHU / RH2 | Rhûn confederations† (2–3 tags) | Balchoth-descended kingdoms and **wain-kingdoms of the steppe** by the Sea of Rhûn; invade Dale on schedule; playable horde-flavor. |
| DUN | Dunland | Chiefdoms with a grudge (the Rohirrim took their land — give them real grievance CBs); Saruman's recruiting ground; can be reconciled by a generous Rohan (†mission). |
| ANG | Mount Gram / Angmar remnant† | Petty orc realm menacing Bree/Shire (fuel for Ranger flavor). |

**Off-board powers as forces, not tags:** the Valar/Eagles (event deus ex machina, §13.7),
Tom Bombadil (the Old Forest is impassable terrain with one easter-egg event), the
Dead of Dunharrow (scripted army for the Paths of the Dead questline).

## 8.2 Starting diplomacy (`12_diplomacy.txt`, `18_opinions`, `20_rivals`)

Encode the web: GON–ROH the Oath (unbreakable alliance); GON–DAM overlord; ERE–DAL–ESG–IRO
the northern lattice (alliances + trade); RIV–LOR–LIN elven concord (defensive);
MOR overlord of DOL, suzerain of UMB/HNE/KHA/RHU (tributary-style subject or IO §13.4);
ISE deceptively friendly with ROH/White Council; universal orc-elf eternal war (opinion
floors); DUN hates ROH; UMB rivals GON. Guarantee lines: RAN/GANdalf-flavored protections
over SHI/BRE (invisible until tested — model as RIV+RAN guarantees).

---

# PART 9 — CHARACTERS

Setup: `04_dynasties.txt` + `05_characters.txt` (`character_db`, ANTIQVITAS format), with
rulers, heirs, consorts, cabinet, generals per realm. All named canon figures alive in 3018
must exist with correct ages, houses, and posts (Appendix-datable; else †):

- **Gondor**: Denethor II (b. 2930, Steward-ruler), Boromir (b. 2978, heir & general),
  Faramir (b. 2983, general — Ithilien Rangers unit tie-in), Imrahil (DAM ruler),
  Forlong of Lossarnach, Húrin of the Keys (cabinet).
- **Rohan**: Théoden (b. 2948, "the withered king" start modifier), Théodred (heir, dies by
  event risk at the Fords 3019), Éomer, Éowyn (courtier — general-by-event potential),
  Gríma (cabinet, Saruman's agent — removable via event chain), Erkenbrand, Gamling.
- **Elves** (immortals, §4.4): Elrond + Elladan/Elrohir/Arwen/Glorfindel/Erestor (RIV);
  Galadriel & Celeborn, Haldir (LOR); Thranduil, Legolas (WOO); Círdan, Gildor (LIN).
- **Dwarves**: Dáin II Ironfoot (b. 2767!), Thorin III Stonehelm (heir), Glóin, Gimli (ERE).
- **North**: Brand (DAL, dies at Dale 3019 with Dáin — twin event), Bard II heir;
  the Master of Lake-town (elected, generate†); Grimbeorn son of Beorn (BEO).
- **The Shire/Bree**: Frodo (Ring-bearer flag), Sam, Merry, Pippin, the Thain (Paladin Took),
  Mayor Will Whitfoot, Barliman Butterbur (BRE flavor).
- **Rangers/Wizards**: Aragorn (b. 2931, RAN ruler, ~15 alternate names for loc flavor —
  use "Strider"/"Thorongil" in event text), Halbarad; **Gandalf the Grey** — modeled as a
  wandering character: court guest cycling by event between SHI/BRE/RIV/GON (never a ruler;
  grants temporary bonuses; central to §13.2), Radagast (RHO), **Saruman** (ISE ruler,
  immortal, the traitor arc §13.3).
- **The Shadow**: Sauron (MOR, immortal, un-killable by war), the Witch-king (general +
  Minas Morgul governor flavor), Khamûl (DOL ruler-lieutenant), the Mouth of Sauron
  (cabinet), Gothmog lieutenant of Morgul, Shagrat/Gorbag (flavor), Uglúk (ISE general
  post-flip), the Great Goblin's successor† (GOB), Bolg's line† (GUN); Haradrim &
  Easterling kings invented in-register from canon seeds — Herumor and Fuinur, the Black
  Númenórean lords of Harad, are the naming anchors (never film/game names; log).
- **Fangorn**: Treebeard/Fangorn himself (FAN ruler, eldest of Ents, immortal), Quickbeam,
  Leaflock & Skinbark (flavor).
- **Traits**: build a Middle-earth trait set (§12, sweep): `ringbearer_hidden`, `nazgul_terror`,
  `dunedain_longevity`, `elven_grace`, `dwarven_grudgekeeper`, `wizard_of_the_istari`,
  `shapechanger`, `craven_counselor`… mapped onto vanilla trait slots/effects.
- **Dynasties**: House of Húrin (Stewards), House of Eorl, Line of Isildur, Durin's Line,
  Took/Brandybuck/Baggins, House of Dol Amroth, †-invented houses for the South/East.

---

# PART 10 — ECONOMY: GOODS, BUILDINGS, MARKETS

## 10.1 Trade goods (`common/goods/`, ANTIQVITAS `antq_barley` format)

Audit every vanilla good: **keep** timeless ones under review of name/icon (grain→re-icon,
wool, fish, timber/lumber, iron, copper, gold, silver, gems, stone/marble, salt, furs, wine,
horses, livestock, clay, honey, amber, dyes, wax, hemp/fiber, medicaments→"healing herbs");
**delete/quarantine** every anachronism (tobacco, coffee, tea, cocoa, sugar, cotton†(sub
with fiber), potatoes/maize & all New-World crops, saltpeter/gunpowder, porcelain†, opium,
clocks, books→"lore-scrolls"?, colonial dyes) — mirror ANTIQVITAS's quarantine patterns.
**Add** Middle-earth goods (`me_` prefix, each with icon+1080×440 illustration §15):
- `me_pipeweed` — the Shire's export (Longbottom Leaf!), demanded by hobbits, wizards†,
  Bree, and — post-flip — Isengard (canon wink).
- `me_mithril` — Moria-only, essentially unmined while orcs hold it (near-zero output until
  a Dwarven reconquest — a late-game economic prize), astronomical price.
- `me_athelas` — rare healing herb (Ithilien, the North); demanded by courts & armies.
- `me_dorwinion_wine` — premium wine variant† or keep `wine` with a Dorwinion location
  modifier (prefer the modifier; log).
- `me_mumakil` — war-beasts good of Far Harad (enables mûmakil units, like vanilla
  war-elephant logistics if such exists — check; else unit-recruitment gating modifier).
- `me_slaves_of_nurn`: **decision** — if vanilla has a slaves good, reuse renamed ("thralls");
  Mordor/Umbar/Rhûn economies lean on it; Free Peoples get abolition-flavored modifiers.
- `me_old_forest_timber`†? Only if a goods niche needs it; don't inflate the list. Target:
  a curated ~30–35 goods total, every one iconed, priced, demand-mapped per pop type
  (elves demand gems/wine/lore, orcs demand thralls/iron/meat†→livestock, hobbits demand
  pipeweed/honey/ale†→grain-beer via production method).

RGO placement: via `location_templates.txt` `raw_material =` (§5.3) — Shire farmland,
Rohan horses, Erebor/Iron Hills gold+iron, Aglarond gems, Umbar/Pelargir fish+trade,
Nurn grain(thrall-worked), Mordor iron/ash-waste-nothing, Dorwinion wine, Forochel furs,
Mirkwood timber+spider-silk†?(no — keep silk out; log), Moria `me_mithril`.

## 10.2 Buildings (`common/building_types/`)

Sweep vanilla: kill anachronisms (universities→**Halls of Lore**, churches→**Hallows/
Shrines/Mead-halls** per faith group, printing→gone, manufactories→medieval-plausible
workshops only, no colonial/trade-company buildings). Add signatures: Mathom-house (SHI),
Golden Hall (ROH capital unique), White Tower & Houses of Healing (Minas Tirith), Hornburg
(unique fort), Orthanc & Barad-dûr (unique great-fortresses with palantír slots §13.8),
Grey Havens shipyards, Halls under the Mountain (ERE), Uruk-pits (ISE post-flip; unlocks
uruk levies), Slave-fields of Nurn (MOR farm line), Corsair drydocks (UMB), mallorn-flet
districts (LOR). Reuse the town_setups/town-rank machinery (ANTIQVITAS
`antiqvitas_market_city` pattern) with ME names (Minas Tirith, Edoras, Erebor, Umbar as
metropolis-rank seeds in `07_cities_and_buildings.txt`).

## 10.3 Markets & roads

`03_markets.txt` hubs: Minas Tirith/Pelargir, Edoras, Bree (the crossroads!), Rivendell†
(small), Esgaroth/Dale (the northern engine), Umbar, a Rhûn hub, a Harad hub, Barad-dûr
(command economy). `09_roads.txt`: the Great East Road, Greenway, North-South Road,
Harad Road, the old Gondor road network (Osgiliath spoke) — decayed grades in the wild
stretches; Mordor's interior war-roads.

## 10.4 Ruins & desolations (static modifiers)

A reusable `me_ruin`/`me_desolation` modifier family applied by generator to: Annúminas,
Fornost, Tharbad, Ost-in-Edhil, Amon Sûl, Osgiliath, Minas Ithil (as Morgul-taint),
the Brown Lands, Dagorlad, the Barrow-downs (haunted: hostile-attrition), Dead Marshes.
These carry archaeology-adjacent flavor events (§13) and reconquest/rebuilding missions —
the emotional core of a Fourth-Age campaign (rebuild Annúminas!).

---

# PART 11 — MILITARY

## 11.1 Land (`common/unit_types/`, ANTIQVITAS copy_from pattern; vanilla gunpowder units quarantined wholesale)

Levies/regulars framework is period-perfect — keep mechanics, reskin everything. Archetypes
(copy_from vanilla medieval templates; per-culture `country_potential` gates):
- Line: spear-levies, shield-walls (Northmen), Gondor tower-shield infantry, dwarven
  mattock-guards (Iron Hills!), elven wardens, orc rabble (cheap, morale-brittle, huge),
  black-uruk heavy infantry, uruk-hai pike+crossbow† (ISE only, post-flip).
- Ranged: longbows (Galadhrim — forest combat bonus), Mirkwood archers, Gondor rangers
  (Ithilien terrain bonus), orc short-bows, Haradrim composite bows.
- Cavalry: **éored lancers** (ROH — the best heavy cavalry in the world, plains bonus),
  Dol Amroth swan-knights (elite heavy), warg-riders (orc — attrition/raid bonuses),
  Variag horse (KHA), Haradrim raiders, Rhûn horse-archers, wain-riders†.
- Monsters as units: **mûmakil** (HNE/HFA; gated by `me_mumakil` good; elephant-lineage
  stats), **trolls** (MOR/GUN: siege-shock, daylight-penalty modifier†), **ents** (FAN only,
  event-spawned, building-shredding siege stats). The **Balrog and dragons stay events**,
  not units.
- Named-character armies: Nazgûl as generals with `nazgul_terror` (enemy morale malus aura
  via unit_abilities/traits — verify mechanism, ENGINE_FACTS it); the Grey Company as a
  RAN special unit; the Army of the Dead as a one-shot scripted stack (§13.5).
- Siege: rams/catapults/trebuchets/siege-towers only. **Grond** as a scripted siege bonus in
  the Minas Tirith war events, not a unit. *Artillery category beyond that: quarantined.*
  Isengard's blasting-fire: a single ISE-only "Fire of Orthanc" siege unit/ability unlocked
  by Saruman's advance line (canon: Helm's Deep wall). No general gunpowder, ever.

## 11.2 Naval

Small but flavorful: corsair galleys & great dromons (UMB), Gondor war-fleet (Pelargir),
elven white ships (LIN — few, fast, mostly for the Departure §13.6), Esgaroth lake-barges
(check lake-navy engine support; else abstract), longboats (DAL via Celduin†). Quarantine
all age-of-sail types. The naval war IS canon: Corsair raids and Aragorn's Pelargir stroke.

## 11.3 Balance dial

The Shadow must FEEL like the book: individually cheaper-weaker troops in oceanic numbers,
elite Free units that cannot be everywhere, forts that matter (Helm's Deep, Minas Tirith
must historically hold long enough for relief mechanics — tune fort levels + the war
events so AI-vs-AI reproduces plausible outcomes ~60% of observer runs §16.3).

---

# PART 12 — SYSTEMS CONVERSION SWEEP (`common/` triage)

Rule: every vanilla subsystem under **both** `in_game/common/` (~120 dirs) **and**
`main_menu/common/` — explicitly including `achievements` (QUARANTINE), `game_rules`,
`game_concepts` (the in-game encyclopedia: saturated with Earth-history text — RESKIN),
`scenarios`/bookmarks (REPLACE with the 3018 bookmark), `flag_definitions`, `named_colors`,
`modifier_icons`, `modifier_type_definitions`, `static_modifiers` — gets a triage verdict in
`docs/SURFACE_AREA.md` — **KEEP** (mechanic + skin fine), **RESKIN** (mechanic kept, all
names/icons/text replaced), **REPLACE** (new ME design), **QUARANTINE** (neutralized the
ANTIQVITAS way: `can_start = { always = no }`, `hide = yes`, empty overlays). No verdict, no
milestone-M12. Highlights (non-exhaustive — the sweep itself must be exhaustive):

- **ages** (6 vanilla slots, keys must stay): → RESKIN: `age_1` "The Gathering Shadow"
  (3018 — NOT "Watchful Peace": that term names TA 2063–2460 and would be a lore error), `age_2` "The War of the Ring" (3019 — or situation-triggered if engine allows;
  verify), `age_3` "The Dominion of Men" (3021), `age_4` "The Rebuilding" (~3040),
  `age_5` "The Long Peace"† (~3080), `age_6` "The Fading Years"† (~3140). Each with
  era-appropriate bonuses/objectives; all six needed to span play to 3200.
- **advances** (~360 in ANTIQVITAS): → REPLACE with a lore tree per age: husbandry, wardcraft†,
  siegecraft, herb-lore, mountain-delving, ring-lore (dangerous branch: power at corruption
  cost §13.8), Númenórean restoration (GON/RAN), uruk-breeding (Shadow-only branch),
  shipwright-lore (UMB/LIN/GON). NO printing/gunpowder/compass/banking anachronisms; culture/
  faith-gated branches keep races mechanically distinct.
  MAKE SURE THAT IN 3018 MOST UNITS/BUILDINGS THAT GONDOR OR ANY OTHER REALM WOULD REALISTICALLY HAVE ARE ALREADY AVAILABLE
   - THINGS FOUNTAIN GUARDS, KNIGHTS, ETC. Don't start as if they had nothing
   - You can make Isengard build up and to some smaller extent Mordor but overall most countries already have a lot of tech available, you don't see the same huge tech evolution as vanilla
   - However you can explore other lore friendly paths. Gondor has the tech but is weak overall, advances can make it progressively reclaim strenght, maybe better rely on its various sub fiefs and vassals, even renew with numenorian traditions, etc
   - Same logic for dwarves that reclaim old ruins like Khazad-dûm and maybe get back old tech like mithril armor and more
   - Overall it's more about reclaiming, regaining power and then renewed prosperity for the powers of good. The powers of evil can have more of a technological level up since that's a theme in Tolkien's work (the evils of industry and the price of progress)
   - More neutral/ human primitive factions can definitely get inspiration from other more advanced civilization and have sort of hybrid units/buildings/privileges etc based on that. Perhap conditional to their alliances or something.
   - Neutral factions can be given mutually exclusive paths depending on if they want to be more good or closer to Sauron(if that's possible)
- **institution**: → REPLACE: slow world-currents like "The Shadow's Reach" (spreads from
  Mordor; darkens the East; Free realms resist), "Hope Rekindled" (spawns on war-turn
  events)†. Small set (3–5), silent otherwise.
- **government_reforms/laws/estates**: → RESKIN+REPLACE per §8 (Stewardship line with
  "Await the King"/"Claim the Crown" tension for GON; Thain/Mayor for SHI; free-league and
  captains-council governments for ESG/UMB; Dominion of the Eye with terror-legitimacy for
  MOR). Estates: Lords/
  Loremasters†/Guilds/Commons renames + realm-flavored privileges (Gondor fiefdom charters,
  uruk war-bands as an ISE "estate"†?  — only if the estate math holds; log).
- **parliament_***: → RESKIN narrowly: Esgaroth's Town-moot, the Shire-moot, Gondor's
  Council of the City; QUARANTINE the rest.
- **religion subsystems** (religious_schools/factions/figures/aspects/holy_sites/gods):
  → REPLACE per §7; papacy-analogues QUARANTINE.
- **diseases**: → RESKIN to period-plausible fevers/plagues (the Great Plague of 1636 TA
  precedent), QUARANTINE syphilis-style colonial-era entries; add "Morgul-sickness"†
  near Shadow fronts.
- **casus_belli/wargoals/peace_treaties**: → RESKIN + add: Grudge War (dwarves), Reclamation
  (GON on Ithilien/Umbar), Darkness Unleashed (MOR one-sided annexation CBs), Raid CBs
  (corsairs/orcs), no colonial/trade-company CBs.
- **subject_types**: → RESKIN: Fief (DAM), Tributary of the Eye, Thrall-realm, Protected
  Land (RAN over SHI style)†.
- **hegemons/great powers**: KEEP mechanics, RESKIN names ("Great Powers of the Age" fine).
- **chivalric_orders**†: if the subsystem is present in this build: Swan Knights, Rangers of
  Ithilien, Knights of the White Tower; else fold into units/estates. ENGINE_FACTS first.
- **colonization/exploration/trade companies/charter companies**: **QUARANTINE ENTIRELY.**
  No terra incognita colonizing loop; the wilds are settled via §10.4 rebuilding missions
  instead. Verify the engine tolerates zero-colonization gracefully.
- **artist_types/artist_work**: RESKIN (court bards, loremasters, smith-wrights — "works"
  become epics/heirlooms†) or QUARANTINE if hollow.
- **avatars/ethnicities/genes/persistent_dna**: portraits pipeline — see §15.5.
- **movements / rebel_demands**: RESKIN+REPLACE — orc uprisings in conquered dark lands,
  Dunlending unrest under ROH, restore-the-king movements in Gondor, Shire discontent
  (†Sackville-Baggins flavor); no Earth-ideology movement names survive.
- **societal_values**: RESKIN deliberately — the axes are permanently on-screen; rename/
  retune each in Tolkien register (e.g. toward "Lore ↔ Sword", "Hearth ↔ Road"†) and kill
  any anachronistic axis outright. ANTIQVITAS has no override to port; this is new work.
- **regencies / heir_selections / designated_heir_reason / child_educations**: RESKIN —
  they carry the Stewardship regency, Théoden's incapacity, Esgaroth's elected Master,
  and Durin's-line succession.
- **bureaucracies / cabinet_actions / country_interactions / character_interactions**:
  RESKIN all player-facing verbs and names (ANTIQVITAS precedent exists for the first
  three); cabinet flavor (Gríma!) hangs on these.
- **ai_***: retune weights for the alignment blocs (orcs never ally elves; Shadow AI
  aggression curves tied to §13 situations; FAN/LOR/RIV passivity until triggered).
- **defines**: `loading_screen/common/defines/me_dates.txt` `NGame = { START_DATE =
  "3018.1.1" END_DATE = "3200.1.1" }` (the ANTIQVITAS `antq_dates.txt` precedent, §4.4)
  plus whatever map/lighting defines the spike proves necessary.
- **music_player_tracks**: KEEP vanilla music wiring untouched (explicit user decision:
  no new audio, vanilla tracks + UI sounds remain).
- **tutorial_lessons**: QUARANTINE (point at ME hints via scriptable_hints instead)†.
- Everything else (`biases`, `insults` (write orcish insults! and elvish courtesies),
  `death_reason`, `country_ranks` ("Realm of Men"→ranks like Barony†… keep simple),
  `road_types`, `topography`, `vegetation`, `climates` …): sweep, verdict, log.

Acceptance for the sweep: `make validate` includes a `surface_area_check` that fails if any
vanilla `common/` subsystem lacks a verdict, and greps shipped text for the Appendix-A
banned-term list in player-visible strings.

---

# PART 13 — NARRATIVE: SITUATIONS, EVENTS, MISSIONS

Formats: ANTIQVITAS `events/` (namespaced country events, DHE date-window pattern),
`common/situations/`, `common/international_organizations/`, start-file IO seeding.
Target volume for v0.1.0: **the War of the Ring fully scripted + ~200 flavor events +
mission trees for 10 major realms**; grow from there.

## 13.1 The spine: "The War of the Ring" situation

A grand situation active from game start, with phase escalation partly on the canon clock,
partly reactive to world state (so player action matters but the default run rhymes with
canon): Phase I "The Gathering Storm" (3018.1: raids, spies, Gollum events) → Phase II
"The War Kindles" (≈3018.6: scripted MOR assault on Osgiliath; DOL strikes WOO; Black
Riders abroad) → Phase III "The Great Assaults" (≈3019.1–3019.3: ISE vs ROH culminating at
the Hornburg; RHU+GUN vs DAL+ERE; DOL vs LOR; MOR vs GON culminating at the Pelennor) →
Resolution (§13.2). Each front is its own sub-situation with scripted war declarations,
objective locations, and dramatic events (Théodred at the Fords, the Deeping Wall, the
siege beacons — "Gondor calls for aid!" as a ROH decision with real stakes).

## 13.2 The Ring questline (design carefully; this is the mod's soul)

The One Ring is world-state, not a unit you escort. Model: hidden `ring_bearer` scope
starting on Frodo/SHI; a **Council of Elrond** convergence event (~3018.10, requires
Gandalf-alive chain) spawns THE FELLOWSHIP as an abstract quest track with staged checkpoint
events (Caradhras/Moria choice → Durin's Bane fires the FAN/LOR chain-enablers → Amon Hen
breaking → the East-road stages: Emyn Muil, Ithilien, Cirith Ungol (**Shelob's Lair** —
also a standing attrition/terror hazard for any army daring that pass, quest or no quest)
→ Mount Doom window 3019.2–3019.6†). At each stage, a weighted outcome roll modified by *world state the player
actually influences*: Shadow patrol strength in the relevant regions, whether Saruman fell,
whether the great assaults were repelled, hope-vs-terror tallies from the fronts. Outcomes:
- **The Ring is destroyed** (canon-likely default): Sauron unmade — MOR collapses (ruler
  dies for real, government implodes, hosts rout, subjects/tributaries scatter or sue for
  peace), Age flips to Dominion of Men, rebuild content unlocks (§10.4), the Departure
  accelerates (§13.6).
- **The Ring is taken by Sauron** (if the West gets crushed early): permanent MOR ascendancy
  modifiers, darkness institution surges, the long defeat — playable horror mode; Free
  realms get last-stand content (Imladris under siege, the Havens exodus).
- **A great one claims it**† (rare: Saruman/Denethor/Boromir-flavored usurper chains): a
  third bloc — the New Ringlord — war of all against all. Bold but canon-plausible-adjacent;
  keep probability low, log the design.
The player never micro-controls Frodo; they tilt fates by winning wars, holding beacons,
clearing patrol strength — visible via a situation UI panel ("Hope"/"Shadow" meters†).

## 13.3 Saruman's treachery

ISE starts trusted (White Council IO member §13.4). Hidden corruption clock from 3000
backstory → event window 3018: public flip (leaves Council IO, uruk unlocks, DUN call-ups,
ROH destabilization events peak), unless a player-Rohan/Gandalf chain exposes him early
(harder war, earlier). If ISE loses the Hornburg arc: the Voice of Saruman events, Orthanc
siege, Scouring-of-the-Shire epilogue disaster for SHI if Saruman escapes†.

## 13.4 International organizations

- **The White Council** (RIV, LOR, LIN, ISE-until-flip, honorary Gandalf): coordination
  bonuses, council events, breaks on the flip.
- **The Shadow of the Eye** (MOR-led: DOL, UMB, HNE, HFA, KHA, RHU…): tribute flows, war
  call-ins, terror cohesion — *brittle if Sauron stumbles* (§8 Khand defection etc.).
- **The Free Alliance**† (formed by event at Phase II: GON, ROH, DAL, ERE, WOO, ESG…):
  the mechanical Last Alliance echo; leadership passes to Aragorn's Reunited Kingdom on
  formation (§13.5).
- Seed at start via `15_international_organizations.txt` (ANTIQVITAS
  `add_international_organization` format).

## 13.5 Set-piece scripted content

Paths of the Dead (RAN/GON chain: Aragorn + the palantír challenge → Dead army one-shot
stack → Pelargir → lifts the Pelennor siege); the Ents' awakening (ISE aggression + Fellowship
Moria stage → FAN war-spawn that wrecks Isengard); the Beacons of Gondor (GON⇄ROH call
mechanic with a lit-beacons event chain); the Eagles (§13.7); Éowyn & the Witch-king
(Pelennor resolution event — "no living man" clause honored); the death of Dáin and Brand
(northern front resolution); Denethor's despair (palantír-driven madness clock if sieges go
badly — succession crisis mid-war); formables: **The Reunited Kingdom** (RAN or GON —
requires the other's cores + war outcomes; Aragorn-alive path makes RAN the natural former),
restored **Arnor**, re-taken **Khazad-dûm** (ERE end-game), **Free Dunland**†.

## 13.6 The Fading (Elves) 

LIN/RIV/LOR live on a slow hourglass: yearly "Departure" pulses drain elven pops westward
(ship events at the Havens), sharply accelerating after the Ring resolves either way (the
Three fail). Elven realms are built to *matter enormously now and vanish beautifully later* —
end-game: Lórien fades to empty forest†, Rivendell to a museum-vale†, Círdan lingers last.
This is the anti-blob mechanic for elf players and it is pure canon.

## 13.7 Deus ex machinae (rare, dramatic, capped)

The Eagles of Manwë: 2–3 scripted interventions max (Five Armies precedent) at climax
events only — never a summonable army. Bombadil: one absurd rescue event if an army dies
in the Old Forest†. Dragon stirrings: a Withered Heath disaster tail-risk for the North
in the long peace†.

## 13.8 The palantíri & ring-lore (strategic espionage flavor)

Seven stones: **three in play** (Orthanc; the Anor-stone in Minas Tirith; the Ithil-stone
at Barad-dûr, taken with Minas Ithil in 2002), **three lost** (Osgiliath in the Anduin;
Amon Sûl and Annúminas drowned with Arvedui at Forochel, 1975), **one apart** (the
Elostirion stone in the Tower Hills, gazing only West — a Places-of-Power hook near the
Shire; departs with Círdan's ship in 3021): building-slot artifacts granting intel/diplo power at sanity/corruption
risk (Denethor/Saruman cautionary chains above). Ring-lore advances (§12) tempt Shadow-curious
players; the Three (Vilya/Nenya/Narya) are hidden realm modifiers that die with the One.

## 13.9 Flavor floor

For v0.1.0: the 10 majors (GON ROH MOR ISE ERE+DAL WOO LOR RIV UMB HNE) each ship a mission
tree **and ≥6 bespoke flavor events**; every other first-class realm ships **≥3** (raise
the floor to 6 for all in a later version). Hobbit events must be
funny (mathom disputes, the Old Took's record, mushroom trespass); orc events nasty-comic
(Shagrat-vs-Gorbag promotion brawls); Gondor events elegiac. Tone discipline per §14.

---

# PART 14 — LOCALIZATION & THE TERMINOLOGY BIBLE

## 14.1 Mechanics

`main_menu/localization/<lang>/*.yml` + `loading_screen/localization/` (ANTIQVITAS layout:
English authored; the other 10 client languages get mirrored English copies — same policy,
log as known limitation). BOM + `l_english:` format. Every new key localized at content-merge
time — `make validate` runs a missing-loc check; placeholder text ("TODO", "PLACEHOLDER",
lorem) is a lint failure.

## 14.2 Register: write like the book reads

Three text voices, applied consistently: **Westron-common** (events for Men/hobbits: warm,
concrete, proverb-ready), **High style** (Gondor/Elven formal content: slightly archaic
inversions, no contractions), **Shadow style** (Mordor/Isengard: cold administrative menace;
orc-dialogue events may use lowercase brutal vernacular). Absolute bans in player-visible
text: modern management jargon ("efficiency gains"), Earth demonyms/terms (French, Byzantine,
crusade, jihad, senate†-(Gondor's is a "Council")), anachronistic tech vocabulary. The
banned-word lint (Appendix A) enforces the floor; taste does the rest. UI chrome renames:
"Prestige"→"Renown"†, "Innovativeness"→"Lore"†, "Manpower"→"Muster", stability/legitimacy
reviewed case-by-case — only rename where vanilla's word breaks period voice (log each).

**Terminology rulings** (binding; Appendix A defers to these): "republic" → **free league**
(ESG) / **Brotherhood of Captains** (UMB); "parliament/senate" → **moot** (north/hobbits) /
**Council** (Gondor/elves) / **town-moot** (ESG); "khan/khagan/khaganate" → **wain-king /
wain-kingdoms** (Rhûn) and invented Variag titles† (KHA); "duke/count" gradients → Lord,
Marshal, Thain, Master, Prince (DAM), Steward; "emperor" → unused (the only high kingship
is the Reunited Kingdom's "High King"). Add new rulings here as collisions surface.

## 14.3 Name lexicons (`docs/world/lexicons/` + language name pools §6.2)

Per language: syllable/compound grammars + curated canon seed lists → generator emits
location names, character names, dynasty names, ship names†, army names. Sindarin
compounds from attested roots (amon/dol/minas/ost/nen/duin/ered/taur…: "Amon Thoron"†),
Rohirric from Old-English-shaped elements (Éo-, -burg, -seld, Folde…), Shire toponyms
(-bottom, -bury, -delving, Bywater pattern: cozy English), Dalish norse-tinged, Haradric
and Easterling invented phonologies documented from canon seeds (Umbar, Khand, Variag,
Balchoth as style anchors)†, Orkish harsh clusters for Mordor-interior names (Udûn, Gorgoroth
attested). Every generated name passes the lexicon's own validator (no accidental real-world
place names — lint against a gazetteer list; no comic collisions).

## 14.4 Dynamic country names

Vanilla/ANTIQVITAS `scripted_country_names` support: use for state transitions — GON under
a crowned king → "The Reunited Kingdom"; ISE post-flip → "Isengard Unleashed"†; MOR
post-ring-loss → "The Black Land, Masterless"†.

---

# PART 15 — 2D ASSET PIPELINE (style fidelity is a hard gate)

You generate images natively (GPT-Image). The single most important rule, stated by the
project owner in bold, is repeated here in bold: **EVERY image-generation request MUST
attach real vanilla EU5 assets as style references. No exceptions.** Un-referenced
generations drift generic — warm-yellow filter, plastic render, mobile-game gloss — and
are immersion poison. The pipeline below makes drift mechanically difficult.

## 15.1 Asset contracts (from the ANTIQVITAS/vanilla audit; re-verify via `asset_manifest.py`)

| Category | Size | Format | Batch mode |
|---|---|---|---|
| Goods/building/religion/institution/cabinet/misc icons | 128×128 | DDS BC7 +mips, alpha | **4-up sheet** |
| Advance icons | 256×256 | DDS BC7 +mips | **4-up sheet** |
| Estate-privilege icons | 64×90 | DDS BC7 | **4-up sheet** |
| COA emblems (White Tree, Red Eye, White Hand, Horse, Swan, Durin's crown…) | match vanilla `ce_*.dds` | DDS, alpha | 4-up or **SVG→raster** (clean silhouettes suit vectors) |
| Event/goods/unit/throne illustrations | 1080×440 | DDS BC7 +mips (non-pow2 mip chain via `dds.py`) | **one per request** |
| Loading screens | 3840×2160 | DDS (DXT1-class) | one per request |
| Frontend/menu background, logo | 3840×2160 / 1024×1024 | DDS | one per request |
| Mod thumbnail | 512×512, <1 MB | PNG (×2 copies) | one |
| Modifier/alert/map-mode icons | audit ANTIQVITAS `modifier_icons` + vanilla for exact sizes; add to manifest | DDS | **4-up sheet** |

## 15.2 Reference library first (M0/M11 groundwork)

Build `assets_queue/references/<category>/` by batch-converting curated vanilla DDS→PNG
(`extract_vanilla.py` + `dds.py identify`): ~12 vanilla goods icons, 8 advances, 8 building
icons, 6 event illustrations, 4 loading screens, emblem sheets, etc. For every category,
**look at the references** (you are multimodal) and write a one-paragraph *style codicil*
into `docs/art/STYLE.md` — palette temperature, brushwork, lighting direction, background
treatment, outline policy, alpha silhouette conventions — derived from observation, not
memory. Every generation prompt embeds the relevant codicil AND attaches 2–4 reference
images from that exact category.

## 15.3 Icon generation protocol (the 4-up loop)

1. Compose batch of 4 semantically-unrelated icons (reduces style bleed between neighbors).
2. Request one 2048×2048 image, strict 2×2 grid, **solid chroma background** (flat
   magenta/green per the ANTIQVITAS `*_chromakey.png` precedent), each quadrant centered
   with ≥12% margin, no text/numbers/borders/watermarks; attach category references;
   append the negative clause: *"no yellow-orange global wash, no lens flare, no cartoon
   outlines, no plastic 3D-render sheen, no photobash"*.
3. Split quadrants with PIL; chroma-key to alpha; auto-trim + re-center on the category's
   canvas; downscale to contract size; encode BC7 via `dds.py`.
4. **Automated QA gate per icon** (in `--check`): exact dimensions; alpha coverage within
   category band; **edge-occupancy ≤ threshold** (any silhouette pixels touching the crop
   border ⇒ CROPPED ⇒ regenerate); **palette-statistics guard**: mean hue/saturation/value
   deltas vs the category's vanilla reference distribution within tolerance (this is the
   anti-yellow-filter tripwire — tune thresholds on vanilla self-test first); SHA-dedup
   (no two keys share art).
5. `make art-review` contact sheets interleaving new icons WITH vanilla neighbors; you
   review the sheet visually each art batch; anything that reads "modded-in" gets one
   retry with sharpened prompt, then goes to `assets_queue/rejects/` with a note — never
   ship a known-weak icon silently (KNOWN_ISSUES it if stuck).
6. **Availability fallback**: if image generation is unavailable, rate-limited out, or
   refuses a key twice, ship a vanilla-derived recomposition (recolor/crop/composite of
   vanilla art via PIL) as an interim asset, KNOWN_ISSUES it, and move on — **M11's
   "zero placeholder" bar means zero *programmer-art*; a tracked vanilla-derived interim
   never deadlocks M12.** Retry generation in later sessions.

## 15.4 Illustrations & loading screens

One per request, full resolution, 2–4 vanilla illustration references attached, painterly
scene briefs written like Paradox art direction ("Minas Tirith at dawn from the Pelennor,
banners of the White Tree, mist on the Anduin, oil-painted, muted"). Same QA: dimension,
palette-stat guard vs vanilla illustration distribution, no-text check (OCR pass†),
edge-composition sanity. Event illustrations map to event categories via a manifest so
every §13 event has era-true art (no vanilla Renaissance interiors leaking through —
audit vanilla fallbacks referenced by kept events and override them).

## 15.5 What is NOT generated

3D: unit meshes, map objects, portraits' 3D heads — **reuse vanilla** via graphical-culture
mapping (elephants→mûmakil, medieval European sets→West, steppe sets→Rhûn, MENA-flavored
sets→Harad — pick tactfully, log). Orcs/elves in 3D: investigate `genes/ethnicities/avatars`
overrides for skin palettes & phenotype nudges (ashen orc skin†); if the engine resists,
accept human stand-ins for 3D and let 2D art carry the fantasy — decide in M11, log.
Audio: **zero new audio** — vanilla music and UI sounds stay (owner decision; do not
spend cycles here; `music_player_tracks` untouched).

## 15.6 Coats of arms

Procedural COA system (ANTIQVITAS `coat_of_arms` format): design each realm's arms from
canon (GON white tree+seven stars+crown on sable; ROH white horse on green; MOR the red
Eye on sable; ISE white hand; DAM silver swan-ship on blue; ERE/IRO Durin's emblems; SHI
†a leaf-and-hearth device — canon silent, invent modestly). New emblem textures via §15.3;
compose via patterns+colors in-script. Every tag gets bespoke arms — no two share, no
vanilla-Earth heraldry leakage (lint: no `ce_` texture reuse where the motif is Earth-
specific like crosses/crescents/fleur-de-lis; Appendix A list).

## 15.7 Map-adjacent art

Flatmap/paper-map (§5.3) in vanilla parchment voice; map-mode tints re-checked against
faction palette (Shadow = blacks/reds territory must read instantly); fonts: keep vanilla
(they're period-appropriate); terrain textures: reuse vanilla biome materials (ash-waste
can borrow volcanic/desert sets) — new terrain paint only if the spike shows it's cheap.

---

# PART 16 — TESTING PROTOCOL

## 16.1 Tier 1 — `make validate` (static; before every commit)

Everything ANTIQVITAS enforces (pdxlint brace/BOM/date/metadata; every generator `--check`)
plus ENDÓRË-specific: map bijectivity suite (§5.3), surface-area verdict coverage (§12),
banned-term grep (Appendix A), missing-loc check, asset contract suite (§15.3), lexicon
validators (§14.3), census sanity (no negative/absurd pops; realm totals within †-declared
envelopes).

## 16.2 Tier 2 — `make smoke` (game launch; before every content commit)

The ported ANTIQVITAS smoketest verbatim in design: launch vanilla control + mod via
`gamedriver.py` (`--user_dir=G:\endore_user_data`, windowed 1920×1080 min-graphics, muted),
wait for menu-ready, diff normalized `error.log` against `baselines/` + vanilla control,
**zero new lines or FAIL**. `--accept` only with a DECISIONS.md entry explaining every
newly-baselined line.

## 16.3 Tier 3 — milestone verification (observer runs + in-game tests)

- **In-game test scripts** (`in_game/common/tests/` — vanilla's own framework: named
  triggers with `year`/`success`/`fail_on_end_year`): write the ME assertion suite, e.g.
  `war_kindles_test` (Osgiliath assault flag by 3018.12), `treachery_test` (ISE flipped by
  3019.6), `ring_resolution_test` (one of the §13.2 outcome flags by 3021.12),
  `no_anachronism_test` (no country ever embraces a quarantined institution; no gunpowder
  unit exists), `fading_test` (elven pop total declines by 3040), `mordor_collapse_test`
  (conditional on destruction outcome). Run via observer mode (`gamedriver.py observer`,
  auto-resume on the known DX12 crash), parse results from logs.
- **Observer soaks**: N-year runs (M-scaled: 5y → 50y → full-to-3200 at M12) watching
  error.log growth, autosave integrity, year-throughput (performance budget: within ~2×
  vanilla tick speed at comparable date†), plus screenshot series over the map modes for
  visual regression review.
- **Canon-plausibility batch** (M12): ≥5 observer runs; target: War fires in all, West
  survives to resolution in ~majority, at least one run reaches Ring-destroyed ending
  organically. **Bounded tuning**: iterate on short mid-war bookmark runs with fixed seeds
  where the engine allows; cap at 6 tune-evaluate cycles — if targets are still missed,
  ship the closest tuning, record the honest matrix in `docs/playtests/` + KNOWN_ISSUES,
  and do not hold the release hostage to stochastic outcomes.

## 16.4 Evidence

Per-milestone `docs/m<N>/` evidence packs (logs, screenshots, test matrices) exactly like
ANTIQVITAS — they are the memory that survives context loss between sessions.

---

# PART 17 — GIT & GITHUB

- Repo `G:\endore`, branch `main`, remote `https://github.com/Rockydo/endore` (create via
  `gh repo create Rockydo/endore --public --source . --push`; general config mirrors
  `Rockydo/antiqvitas`: public, no LFS, plain main-branch flow).
- **Commit discipline**: on `main`, large coherent batches only (a milestone slice per
  commit; the bootstrap commit is the only small one). Conventional Commits: `feat(map):`,
  `feat(world):`, `feat(narrative):`, `feat(art):`, `feat(bootstrap):`, `fix(...)`,
  `docs(...)`. Terse subjects, no bodies, no co-author trailers (match ANTIQVITAS log
  style). Push after every commit.
- **Crash insurance**: long gaps between `main` batches are backed by WIP snapshots on a
  `wip/current` branch (commit+force-push freely there; never merge it — `main` batches are
  authored fresh). An interrupted session must never lose more than an hour of work.
- Committed: content roots, docs/, tools/, baselines/*.log, control layers, asset masters
  policy per ANTIQVITAS gitignore precedent (sources committed selectively — mirror its
  ignore list; keep the repo well under GitHub's soft limits; loading-screen DDS are ~5 MB
  each, fine).
- CI: optional thin lint workflow (py_compile + game-independent pdxlint subset behind a
  `--no-game` flag). The game cannot run on GitHub runners — all smoke/observer testing is
  local; do not pretend otherwise in CI.

---

# PART 18 — MILESTONES (each = a cluster of large commits + evidence pack + green gates)

| M | Deliverable | Gate (all prior gates stay green) |
|---|---|---|
| M0 | **Minimum** bootstrap (§2): repo, GitHub, toolchain port, skeleton mod, baselines — only what launching+testing requires | empty mod smokes clean; pushed |
| M1 | **PROOF OF ARDA** (§5.4, top priority, blocks all else): rough Middle-earth-shaped map + dates 3018/3200, wrap_x, immortals probe, dangling-reference signatures, in-game-test probe → ENGINE_FACTS | rough ME map loads; screenshot series shows the shape; one in-game test executes; smoke zero-new |
| M2 | **The Map v1** (§5): control layers, full generator chain, hierarchy, templates (terrain only), geography-reference quarantine sweep (§5.4) | in-game navigable Middle-earth, validate suite green, smoke zero-new incl. no dangling-reference errors |
| M3 | Realms painted: tags, COA v1 (script-only arms OK), ownership, named locations, ruins | every location owned/assigned or deliberately wild; smoke green |
| M4 | Peoples & faiths (§6–7): cultures, languages+name pools, religions, templates joined | map modes read correctly; loc complete for all keys |
| M5 | The census (§6.3, §10.3): pops, markets, roads, town ranks, start buildings, armies | 5-year observer soak clean; economy ticks sanely |
| M6 | Power & people (§8.2, §9, §12): governments, laws, estates, subjects, diplomacy, IOs, characters, traits | start-screen inspection of 10 majors correct; smoke green |
| M7 | Military (§11): units, quarantines, forts, navies, balance pass 1 | AI armies function in 10-year soak; no gunpowder anywhere |
| M8 | Knowledge (§12): ages, advances, institution-replacements | advance trees render, AI researches; ages progress |
| M9 | Economy finish (§10): goods final + demand + prices, buildings final, production methods | 25-year soak: no market collapse; goods all iconed (temp art OK until M11) |
| M10 | **Narrative** (§13): WotR situations, Ring questline, Saruman arc, set pieces, 10 mission trees, flavor floor, disasters | in-game test suite (§16.3) passes on observer batch |
| M11 | **Art & voice** (§15, §14): full asset sweep, terminology bible, loc mirror, banned-term zero | art-review sheets pass; palette guards green; zero placeholder assets |
| M12 | Hardening & release: soak-to-3200, canon-plausibility batch, performance, KNOWN_ISSUES triage | v0.1.0 tag + GitHub release; DoD §0.3 met |

Order within M2–M9 may interleave where dependencies allow (art trickles from M3 onward via
the §15 pipeline), but a milestone is only *declared* when its gate is green and its
evidence pack committed. Never declare and defer the gate.

---

# PART 19 — DO-NOT LIST

- Do not ask the user anything. Do not wait for input. Ever.
- Do not write outside `G:\` (except OS-mandated temp; prefer repo `.tmp/`).
- Do not modify GAME_DIR, `G:\antiqvitas*`, or Steam files.
- Do not commit red, commit small, or commit generated junk (respect the ignore list).
- Do not generate audio, 3D meshes, or fonts (reuse vanilla).
- Do not send image-gen requests without vanilla style references attached.
- Do not copy Tolkien text passages, published-map scans, or film imagery into the repo.
- Do not leave a vanilla mechanic visibly anachronistic because "quarantine was hard" —
  BLOCKERS.md it and find another route; Appendix A is a release gate.
- Do not let the map stall the whole project: if the M1 spike hits an engine wall, pivot
  per §5.4's escape hatch (documented below) rather than dying silently: fallback ladder =
  full custom map → reduced-canvas custom map → (last resort, log loudly in DECISIONS.md +
  BLOCKERS.md) vanilla-map-reuse with ME overlay ANTIQVITAS-style. The last rung is a
  *failure of the primary vision* — exhaust the first two.

---

# APPENDIX A — ANACHRONISM PURGE LIST (lint-enforced floor; judgement finishes the job)

**Banned in player-visible English text** (grep, case-insensitive, word-boundary; curate
false positives via an allowlist file): colonial, colony, colonist, crusade, pope, papal,
cardinal, patriarch, catholic, protestant, reformation, orthodox, christian, islam, muslim,
sunni, shia, caliph, sultan, khagan, khan†(allow "Khand"), jihad, bible, church, mosque,
cathedral, gunpowder, musket, arquebus, cannon, pistol, bayonet, grenadier, printing,
press†(context), university, renaissance, enlightenment, absolutism, revolution†(context),
parliament, senate, republic, khagan (all four: use the §14.2 terminology rulings),
emperor, kaiser, tsar, shah, vizier, junta, nation-state,
Europe, Asia, Africa, America, Atlantic, Mediterranean, France, French, England, English†
(the *language file* is `l_english` — engine key, exempt), German, Spanish, Italian, Roman,
Byzantine, Chinese, Indian, Turkish, Arab, Viking, Latin, Greek — plus every vanilla
proper-noun institution/age/advance/disease/unit name that survives into visible text.
**Banned visual motifs** (§15 review): crosses, crescents, fleur-de-lis, double-headed
eagles, Earth-flag heraldry, ships-of-the-line, plate-and-pike ensembles, firearms.
**Calendar**: check month-name localizability; if the engine hardcodes Gregorian month
names, record as accepted limitation in KNOWN_ISSUES (they're tolerable; Tolkien's own
narration uses them) — do not burn a milestone on it.

# APPENDIX B — LIVING DOCS (the project's memory; update as you go)

`docs/PROGRESS.md` (milestone truth), `docs/TODO.md` (next-task queue), `docs/DECISIONS.md`
(every judgement), `docs/ASSUMPTIONS.md` (every † with reasoning), `docs/ENGINE_FACTS.md`
(every empirically verified engine behavior), `BLOCKERS.md` (two-strike log),
`KNOWN_ISSUES.md`, `docs/SURFACE_AREA.md` (§12 verdicts), `docs/world/census_notes.md`,
`docs/world/lexicons/`, `docs/art/STYLE.md`, `docs/m<N>/` evidence packs. A session that
changed the world but not the docs is an unfinished session.

*Now go build the most beautiful fantasy grand-strategy conversion ever made by man or
machine. The Road goes ever on.*
