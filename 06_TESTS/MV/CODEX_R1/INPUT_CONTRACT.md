# CODEX R1｜INPUT CONTRACT

## Principle

Codex must know exactly what it can expect from the user and what it must obtain automatically.

Do not ask the user to manually perform steps Codex can execute itself.

---

## Required repo context

Codex must be inside this repository and read:
- `06_TESTS/MV/CODEX_R1/CURRENT_STATE.md`
- `06_TESTS/MV/CODEX_R1/CODEX_R1_MASTER_PLAN.md`
- `06_TESTS/MV/CODEX_R1/GOLDEN_TARGET.md`

---

## Local input directory

Codex creates if absent:

```text
06_TESTS/MV/CODEX_R1/local/
  inputs/
    audio/
    videos/
    links/
  outputs/
    audio/
    sources/
    subtitles/
    video/
    final/
    manifests/
    reports/
    logs/
```

`local/` is machine-local runtime data and should not be committed if it contains large media, cookies, account data, or temporary credentials.

---

## Minimum user-provided input for MODE A

### Audio
Preferred:
`local/inputs/audio/你有没有真的爱过我-阿图表妹.mp3`

If absent, Codex should first attempt to obtain the exact version automatically.

Only after automatic retrieval fails should Codex ask the user to provide the file.

### Video sources
Preferred automatic path:
- Codex retrieves watermark-free HD versions using provided source / share links.

Fallback user input:
```text
local/inputs/videos/S1.mp4
local/inputs/videos/S2.mp4
...
local/inputs/videos/S8.mp4
```

### Source links
Optional:
`local/inputs/links/source_urls.json`

Suggested shape:
```json
{
  "S1": "...",
  "S2": "...",
  "S3": "...",
  "S4": "...",
  "S5": "...",
  "S6": "...",
  "S7": "...",
  "S8": "...",
  "reference_mv": "...",
  "music_page": "..."
}
```

---

## Account / login inputs

Never request passwords, cookies, session tokens, or secret keys in chat or commit them to GitHub.

If Douyin Creator Center requires login:
- Codex launches persistent browser profile;
- user may manually log in / solve CAPTCHA;
- browser state stays local;
- Codex resumes automatically afterwards.

Local browser profile must be gitignored.

---

## External generation boundary for MODE B

If Codex cannot directly generate GPT first frames or Seedance videos:

Codex must output deterministic filenames:

```text
local/inputs/generated/first_frames/S01.png ...
local/inputs/generated/videos/S01.mp4 ...
```

and a manifest:
`local/outputs/manifests/external_generation_request.json`

State must become:
`EXTERNAL_GENERATION_REQUIRED`

After files appear, Codex validates them and resumes. It must not ask the user to re-explain project context.

---

## Forbidden input handling

Do not:
- commit cookies;
- commit login profiles;
- commit private account exports unless explicitly approved;
- commit large media by default;
- infer missing source files from filenames alone;
- silently substitute another song version.
