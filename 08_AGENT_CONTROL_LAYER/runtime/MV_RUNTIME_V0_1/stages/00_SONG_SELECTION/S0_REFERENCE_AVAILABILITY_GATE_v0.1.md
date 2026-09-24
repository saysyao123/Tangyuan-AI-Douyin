# S0 Reference Availability Gate v0.1

## Why this gate exists

A good song candidate can still fail operationally because the originally recommended concrete reference:
- is removed;
- no longer opens;
- cannot be saved/exported through normal user-facing means;
- is region/login restricted;
- is available only as an indexed stale URL.

This must not silently force the system to abandon the song.

## State model

After Human Song-Family preference:

1. `SONG_FAMILY_SELECTED`
2. check concrete reference availability

Possible outcomes:

### AVAILABLE
Concrete reference can be opened and practically used as evidence.
-> proceed to Human Reference Lock.

### DEGRADED
Reference opens but is poor for downstream visual/motion analysis.
-> keep song family selected; search alternate reference.

### UNAVAILABLE
Reference cannot be practically used.
-> enter `REFERENCE_RECOVERY`.

### AUDIO_ONLY
A source can confirm song/audio/lyrics but is not a valid visual/motion reference.
-> may support S1 song verification later, but does not satisfy S0 visual reference requirement by itself.

## Recovery order

1. same Song Family + same trusted core ecosystem;
2. same Song Family + another concrete Douyin work;
3. same Song Family + accessible public video for song/lyrics confirmation;
4. if no suitable visual reference exists, allow an explicit split:
   - SONG_REFERENCE = chosen song/audio evidence
   - VISUAL_STRUCTURE_REFERENCE = separate work chosen later for Director structure

The split must be explicit. Never pretend an audio/lyrics video is a motion/camera reference.

## Download/access rule

S0 does not depend on unofficial downloader tools or bypass methods.

Preferred:
- normal platform access/save/share/export where available;
- user-provided media;
- another accessible concrete reference;
- public evidence links.

If a platform blocks normal download, mark it operationally unavailable instead of building the workflow around circumvention.

## Seal rule

S0 may seal in either of two modes:

### MODE A — SINGLE_REFERENCE
One concrete work is both:
- selected song reference;
- usable downstream structural reference.

### MODE B — SPLIT_REFERENCE
The selected song family is locked, but:
- song/audio evidence and
- visual/motion structure evidence
come from different explicit references.

MODE B requires the distinction to be preserved in the handoff.
