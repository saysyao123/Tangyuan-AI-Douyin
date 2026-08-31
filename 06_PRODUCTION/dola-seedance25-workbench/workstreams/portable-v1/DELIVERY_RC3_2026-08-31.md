# Dola Seedance Portable V1 — RC3 Delivery Receipt

Date: 2026-08-31
Workstream: `portable-v1`
Branch: `work/dola-portable-v1`

## RC2 user-side evidence that triggered RC3

The Windows RC2 test produced two important observations:

1. The center embedded Dola WebView could generate successfully when the user operated Dola directly in that page.
2. The right-hand Seedance Studio `创建并开始` path created a task but the automated task failed.
3. When I2V was selected, the extra image-input controls pushed the lower task area below the fixed-height right panel, making the task list difficult or impossible to inspect without a proper vertical scroll path.

This changes the G1 diagnosis: the user-visible account/session/Dola page is demonstrably usable for generation, while the workbench dispatch surface remains the failing layer. The project therefore must not classify the failure as a generic Dola/provider failure.

## RC3 dispatch change

For desktop UI submission, RC3 now prefers the exact currently visible Dola WebView for the selected account.

Flow:

```text
right Seedance Studio
  -> create durable task
  -> desktop IPC identifies the visible WebView using the account's Electron partition
  -> confirm visible Dola login state
  -> acquire the existing WorkerScheduler lease
  -> bind the Portable Dola runner temporarily to that visible WebContents
  -> prepare model/duration/ratio/image/prompt on the same center page
  -> arm capture before submit
  -> submit on that page
  -> observe/resolve/download through the existing lifecycle
```

The visible WebView is not a second login path and no credentials are read. It is the same account partition the user already opened manually.

Codex / loopback API dispatch remains a background-worker path. If desktop IPC cannot find a matching visible WebView, the existing local Control Plane background dispatch remains available as the fallback. This keeps interactive G1 debugging aligned with the visible page without removing the background architecture required for later G2/G5/G20 testing.

## RC3 right-panel change

The complete Seedance Studio column now has an explicit vertical scrollbar. The task form no longer permanently hides the lower task list when I2V adds the image row.

Task cards are also decorated with:

- `执行位置：中间可见 Dola 网页` when the visible-WebView path is used;
- the actual persisted task error when a task fails;
- blocked-state detail when relevant.

This is intended to make the next Windows failure actionable instead of displaying only a generic `failed` badge.

## Automated evidence

Foundation workflow:

- Workflow: `Dola Portable V1`
- Run: `#122`
- Run id: `33370534500`
- Head: `053d6756cb1ee58a77bf9fefe97cffe73d4ec1a9`
- Result: PASS

Release workflow:

- Workflow: `Dola Portable Release ZIP`
- Run: `#16`
- Run id: `33370534517`
- Head: `053d6756cb1ee58a77bf9fefe97cffe73d4ec1a9`
- Result: PASS
- Artifact id: `9749952407`
- GitHub artifact digest: `sha256:6e160efaefca8bf025619d5e03a55412539f44e9d5f9f04bd43e2af3add35544`

End-user ZIP:

`Dola-Seedance-Workbench-Portable-v1-RC3.zip`

Verified SHA-256:

`e59d4fca2817e68bd5fc1e730804870b624b193712a17632effe769ddc9330a1`

Executable:

`Dola-Seedance-Workbench-Portable-0.3.2-portable-v1-rc3-x64.exe`

Archive integrity test: PASS.

## Real-world Gate status after packaging

- Center visible Dola page manual generation on the user's authorized account: OBSERVED SUCCESS on RC2.
- RC2 right-panel automatic submit: OBSERVED FAIL.
- RC3 right-panel visible-WebView automatic submit: READY_FOR_USER_RETEST / NOT_PASSED_YET.
- RC3 result observation + highest-quality accessible MP4 download: NOT_PASSED_YET.
- clean shutdown/restart session persistence: still requires explicit user evidence.
- G2/G5/G20 remain blocked by G1.
- 30s remains entitlement-gated and experimental; no bypass behavior is added.

No CAPTCHA/MFA bypass, login bypass, quota/entitlement bypass, rate-limit evasion, 403 bypass or provider restriction circumvention is part of RC3.
