# Test Log

所有真实测试按时间追加，不覆盖历史结果。

## 2026-08-29 — Repository bootstrap

- Gate: G0
- Status: PASS
- Result:
  - Public test repository confirmed.
  - Safety rules established.
  - Raw credentials/captures/browser profiles excluded from Git.
  - POC acceptance gates defined.
- Evidence: repository files and commit history.

## 2026-08-29 — CI static validation

- Gate: pre-G1 static validation
- Status: PASS
- Environment: GitHub Actions / Ubuntu / Node.js 20
- Result:
  - `npm install` passed.
  - `npm run typecheck` passed.
  - `npm test` passed.
  - Redaction unit tests passed.
- Scope note:
  - This validates code compilation and sanitizer behavior only.
  - It does **not** prove Dola browser connectivity, request capture, Seedance 2.5 lifecycle mapping, or 30-second generation.

## 2026-08-29 — Default architecture switched to current Chrome Extension

- Gate: pre-G1 architecture validation
- Status: IMPLEMENTED / awaiting user browser test
- Result:
  - Default Playwright/new-profile path removed from normal user flow.
  - `START_WEB.bat` removed.
  - Debug localhost launcher renamed to `DEBUG_START_WEB.bat`.
  - `extension/manifest.json` switched to Manifest V3 MAIN-world `page-hook.js` at `document_start`.
  - `content.js` remains isolated-world UI/storage layer.
  - Inspector defaults to capture ON for first use.
  - Existing Google/Dola login state in the user's current Chrome is preserved by design.
  - fetch/XHR request and text/json response observation is sanitized before being stored by the extension UI.
- Scope note:
  - Static architecture is implemented.
  - G1 is not PASS until the extension is manually loaded in the user's current Chrome and the Inspector is visibly present on Dola.

## 下一测试：G1 Current Chrome Extension

目标：

1. 在用户平时正在使用、已经登录 Google 的 Chrome 打开 `chrome://extensions/`。
2. 开启开发者模式并“加载已解压的扩展程序”。
3. 选择仓库中的 `extension` 文件夹。
4. 在同一个 Chrome 打开 `https://www.dola.com/`。
5. 确认右侧出现 `Seedance Inspector`。
6. 确认页面显示 `当前 Chrome 会话 · 无需重新登录` 和 `自动记录已开启`。
7. 正常进行 Google/Dola 登录或直接复用已有登录态。

G1 通过后进入 G2：正常生成一次 Seedance 2.5 / 10s / T2V，并验证请求/响应捕获。

## 2026-08-30 — Windows D0/D1 Electron persistent-session test

- Gate: D0 / D1
- Status: PASS
- Environment: Windows desktop, `LOCAL_CONTROL_PLANE_ROOT`, branch `feat/codex-control-plane`
- Action:
  - Installed `apps/desktop` dependencies and ran `npm run check`.
  - Started Electron and verified `studio health`.
  - Verified `accounts list`, created `Dola A`, and opened its real visible WebView.
  - User manually completed Google/Dola login in Dola A.
  - Closed and restarted Electron.
  - Created and opened `Dola B`.
- Expected:
  - Dola A keeps its login after restart.
  - Dola B uses a separate Chromium persistent session and does not inherit Dola A's login.
- Observed:
  - After manual login, Dola A visibly showed the logged-in account label `DOLA_ACCOUNT_A` and no login dialog.
  - After Electron restart, Dola A still visibly showed `DOLA_ACCOUNT_A` and no login dialog.
  - Dola B visibly showed the Dola `登录` entry point and did not show Dola A's account label.
  - The desktop UI showed both account cards and switched to Dola B through the control-plane `accounts open` command.
  - After this initial isolation check, the user manually logged in Dola B; Dola B then visibly showed the account label `DOLA_ACCOUNT_B` while Dola A remained `DOLA_ACCOUNT_A`.
- PASS/FAIL: PASS
- Evidence:
  - `npm install` completed successfully.
  - `npm run check` completed successfully.
  - `npm run studio -- health` returned `ok: true`.
  - `npm run studio -- accounts list/add/open` completed successfully.
  - Visible Electron WebView observations before and after restart.
- Known limitations:
  - Dola B was initially left logged out to prove it did not inherit Dola A; it was subsequently logged in manually for the two-account test.
  - `dola-web` automatic dispatch remains blocked by `D2_GATE_NOT_PASSED`.
  - D2 request lifecycle and Dola native 30-second capability are not yet verified.
- Next action: In Dola A, the user must manually initiate one normal Seedance 2.5 10-second T2V request for D2 observation; do not mark D2 or D3 passed from configuration alone.

## 2026-08-30 — 30s backend dispatch probe

- Gate: D3 preflight
- Status: BLOCKED BY D2 GATE (expected)
- Environment: Windows desktop, branch `feat/codex-control-plane`; Dola A and Dola B had both been visibly logged in.
- Action:
  - Queried `providers list`.
  - Created a local `dola-web` T2V task with `duration=30` and `ratio=9:16`.
  - Called `tasks dispatch` once, then cancelled the local probe task.
- Observed:
  - `dola-web` reports `dispatchReady: false`, `gate: D2`, and `i2v: unknown`.
  - `duration=30` passes local task validation and is stored in task metadata.
  - Dispatch returned HTTP `409` with `D2_GATE_NOT_PASSED`.
  - No provider request, video generation, quota consumption, or media result occurred.
- Conclusion:
  - The current backend can represent a 30s task, but cannot yet send it to Dola.
  - The first-frame-plus-action-prompt idea is an input strategy, not a Provider implementation; the current CLI task contract does not yet carry a first-frame asset.
  - A real D2 10s lifecycle observation is still required before implementing the experimental Dola adapter and attempting a native 30s request.
- Evidence: `providers list`, `tasks create --duration 30`, `tasks dispatch` response `409 D2_GATE_NOT_PASSED`, and local cancellation response.
- Next action: Complete one normal user-initiated Seedance 2.5 10s T2V observation in Dola A, then standardize submit/SSE/conversation-chain/result evidence.

### 测试记录模板

```text
Date:
Gate:
Environment:
Action:
Expected:
Observed:
PASS/FAIL:
Evidence:
Known limitations:
Next action:
```
