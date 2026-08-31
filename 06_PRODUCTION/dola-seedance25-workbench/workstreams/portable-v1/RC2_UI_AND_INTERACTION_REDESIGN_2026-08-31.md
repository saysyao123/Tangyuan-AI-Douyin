# RC2 UI / Interaction Redesign — 2026-08-31

## Trigger

User-side Windows RC1 feedback:

- “添加 Dola 账号”点击后没有可见效果；
- “修改保险库密码”没有可见效果；
- 整体界面与早期 POC 相似，希望保留早期方案已经验证过的多账号工作台逻辑，并参考此前上传的 `小柴多开器3.4.8_Windows_x64` 的成熟产品结构重新梳理。

## Root cause found in RC1 renderer

RC1 renderer used browser-native JavaScript dialogs for important product actions:

- `window.prompt(...)` for account creation;
- `window.prompt(...)` repeatedly for vault password change;
- `window.confirm(...)` / `window.alert(...)` for destructive and success/error flows.

These dialogs are not a reliable packaged-Electron interaction contract. In the user build this manifested as buttons appearing clickable but producing no useful visible workflow. This is an RC1 product bug, not user misuse.

## Reference principles retained

From the earlier Dola workbench and clean-room reference-app analysis, RC2 keeps the architecture that was already directionally correct:

1. one durable account record per Dola account;
2. one independent `persist:dola_<accountId>` Chromium session per account;
3. left account pool / center current Dola browser / right generation task panel;
4. only one visible manual-login/debug WebView at a time;
5. hidden account workers remain separate from the visible debug surface;
6. account identity, task identity and output identity stay explicitly bound;
7. no passwords, Google TOTP, raw Cookie or session tokens are exposed to Codex.

The uploaded reference installer was re-located from the user's Library and re-checked as the same 3.4.8 Windows x64 reference package used in the earlier clean-room analysis. RC2 does not copy proprietary code or assets from it; it uses only high-level product/interaction lessons.

## RC2 product changes

### Account manager

- Replace prompt-based account creation with a real in-app modal.
- “创建并打开登录页” becomes one explicit action.
- Account list shows count and per-account login state.
- Selecting an account prepares its encrypted profile, then opens only that account's visible Dola WebView.
- Add explicit “检查登录” control and session-state badge.

### Vault settings

- Replace prompt-based password flow with a real password form.
- First preset password state is visible in UI.
- If preset password is still active, user only enters the new password twice.
- Success and errors render as visible in-app status/toast messages.
- Custom in-app confirmation dialog replaces browser confirm/alert usage.

### Seedance studio

- Remove confusing provider choice from the primary V1 UI; Dola Web is the V1 provider path.
- Add clear T2V / I2V mode selector.
- Add native Windows image picker for I2V.
- Keep 5s / 10s normal targets and 30s experimental.
- Default action becomes “创建并开始”.
- “仅加入队列” remains available for batch/Codex workflows.
- Keep explicit recover-without-resubmit action.

## Regression tests added

`test/renderer-contract.test.js` verifies at least:

- renderer no longer calls `window.prompt`, `window.alert` or `window.confirm`;
- account creation modal exists and invokes `bridge.addAccount(name)`;
- password modal exists and invokes `bridge.changeVaultPassword(current, next)`;
- I2V image picker is wired through preload + portable main;
- Dola Web / Seedance 2.5 remains the primary task path.

## Evidence boundary

RC2 automated checks can prove renderer wiring, syntax and Windows packaging. They cannot prove the real Dola G1 gate. G1 still requires the user's Windows machine to show:

`add account -> Dola page opens -> manual login -> 5s generation submit -> result observation -> highest-quality accessible MP4 download`.
