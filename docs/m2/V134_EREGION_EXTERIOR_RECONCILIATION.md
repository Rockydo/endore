# v134 Eregion exterior reconciliation

This M2 political and hierarchy batch resolves the remaining contradiction at Moria's
western side. It deliberately does not alter terrain, relief, forests, rivers, coasts,
location geometry, or the realm roster.

## Source ruling

*The Lord of the Rings*, Book II, places the Fellowship's route from the West-gate across
Eregion. Tolkien's map geography identifies Eregion west of the Misty Mountains, bounded
on the east by Moria's western cliff, with a northern low ridge south of Rivendell. The
Sirannon and the Elven-way run out from the Doors of Durin through Eregion to Ost-in-Edhil;
they describe an approach and an abandoned former Elven land, not an orc state border.

The direct project controls provide a compact, testable bracket: the Angle at
`0.475000, 0.270000` remains the Ranger refuge in North Arnor; Hollin Ridge at
`0.476614, 0.284861`, Warg Hill, and Ost-in-Edhil remain wild Eregion. Redhorn Gate stays
on the Anduin-side hierarchy as Moria's contrasting immediate mountain approach.

## Change and invariant

The Eregion northern UI join now falls between the Angle and Hollin rather than enclosing
both. Its eastern UI seam follows the cliff/crest between Warg Hill and the passable
Celebdil witness, so the named Moria peak remains on the Anduin side. Moria's reviewed
envelope includes that one passable crest representative, but is restricted to
`me_anduin_vale_region`; its former Eregion-side cells return to deliberate wilderness.
Validation now fails if the Angle leaves North Arnor or if any land Eregion cell gains a
non-wilderness owner.

## Complete named-theatre review

This correction is the only ownership change produced by the completed M2 named-theatre
sweep. The review does not convert sparse source geography into invented cadastral
borders. Instead it re-checks the complete generated control ledger against each bounded
theatre, retaining deliberate wilderness wherever neither canon nor the binding source
maps establish a controller.

| Theatre | Re-checked source relationship | Result |
| --- | --- | --- |
| Gap of Rohan | Dunland west of the Isen; Fords held from Rohan; compact Nan Curunir/Isengard | Retained: no source-proven mismatch. |
| Lothlorien and Moria | Golden Wood east of the Misty crest; Moria's west-gate exterior and Eregion | Corrected: this v134 Eregion/Moria reconciliation. |
| Dale and the Lonely Mountain | isolated Erebor, Dale/Long Lake, and Iron Hills east of Erebor | Retained: no invented eastern Dale frontier. |
| Mordor and Ithilien | mountain-enclosed Mordor; occupied gateworks versus emptied Ithilien | Retained: exact occupied cells only; Dead Marshes and Dagorlad remain wild. |
| East and South | Dorwinion at the north-western Sea of Rhûn, Khand, and the Harnen/Harad relation | Retained: only plan-sanctioned, explicitly marked extrapolated polities occupy the sparse map edge. |
| Far Harad fringe | the represented far-southern source edge | Retained: one documented fringe seat, not a fabricated mapped interior. |

The static ledger proof covers all 113 authored landmarks: every landmark has exactly one
owner-or-wilderness contract, and each theatre's required witnesses have an owner admitted
by that theatre's explicit allowlist. Realm seats and active settlement anchors are
separately checked by the generated ownership model; this is why some seat references do
not duplicate a landmark-control row.

## Verification

- `gmake validate`: PASS in 551.9 seconds, including the 448.4-second full M2 world gate,
  source-coordinate audit, controls, terrain cache, native rivers, hierarchy, ownership,
  people, census, templates, and lint.
- Named-theatre ledger audit: PASS. All 113 authored landmark references have an exact
  control contract; all six theatre ledgers have zero missing required witnesses and zero
  owner/allowlist mismatches.
- Runtime smoke is pending rather than failed: immediately after validation, the shared EU5
  lease was held by Antiquitas (`gamedriver session: mod`, PID 20948). The tool recorded
  the deferred gate; ENDÓRË did not wait, poll, or claim a smoke result. A paired smoke and
  exact fingerprint assertion remain mandatory before publication.
