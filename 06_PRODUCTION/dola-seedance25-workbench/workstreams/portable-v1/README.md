# Dola Workbench Portable V1

> 独立工作流记录目录。本文档与本目录下所有记录仅服务于 `work/dola-portable-v1` 分支的新一轮 Windows 便携工作台开发，不与此前 D0-D6 POC、30s 实验或历史 evidence 混写。

## Workstream identity

- Branch: `work/dola-portable-v1`
- Parent project: `06_PRODUCTION/dola-seedance25-workbench`
- Workstream path: `06_PRODUCTION/dola-seedance25-workbench/workstreams/portable-v1/`
- Started: 2026-08-31
- Status: `AUDIT_AND_FOUNDATION`

## V1 outcome

把现有 Dola Seedance 2.5 POC 升级为 Windows x64 绿色便携工作台：

1. Electron 桌面 Session Manager + localhost Web Workbench；
2. 约 20 个、可继续扩展的 Dola 账号槽位；
3. 每账号独立 persistent Chromium partition / WebContents / task binding；
4. 首次登录和失效后的重新登录由用户人工完成；
5. Codex 在保险库解锁后通过 HTTP API + CLI + machine-readable state 全自动管理；
6. T2V + I2V，Seedance 2.5，5s/10s 为稳定目标，30s 为独立实验 Gate；
7. 真实 Dola 网页 UI 驱动提交，Observer 只做生命周期观察；
8. 单账号同时最多一个 generation，不同账号可并行；默认 active worker pool=3，可配置；
9. 任务支持单条和 project batch；project/shot/revision 强幂等；
10. 自动恢复原任务，不因 Observer/下载失败而重复生成；
11. 下载当前正常会话可访问的最高质量媒体版本；
12. 按 project/shot 自动归档，并输出 task JSON 与 `PROJECT_COMPLETE`；
13. Portable app/runtime 与长期 data 完全分离；
14. profiles/session 区域使用主密码保险库，每次启动人工解锁一次；
15. Codex 可启动/停止 Workbench，但不能读取主密码、Cookie、Token 或浏览器原始凭据。

## V1 Production PASS

用户启动并解锁一次 Workbench 后，Codex 可一次提交一个多镜头项目，并在无需用户触碰 Dola 页面情况下完成：

```text
read account pool
→ schedule healthy account(s)
→ wake isolated session
→ upload local input
→ fill prompt / model / duration / ratio
→ submit through real Dola UI
→ observe lifecycle
→ recover across restarts if needed
→ resolve authorized media candidates
→ download highest-quality accessible file
→ archive by project/shot/revision
→ emit PROJECT_COMPLETE
```

仅在 `LOGIN_REQUIRED`、MFA/CAPTCHA、或 Dola 页面发生无法自动判断的重大变化时要求人工介入。

## Safety / scope lock

- 不自动注册账号；
- 不托管 Google 密码/TOTP；
- 不绕过 CAPTCHA/MFA；
- 不伪造 entitlement、设备身份或反滥用字段；
- 不把自动换账号设计为规避单账号 quota/rate-limit/付费限制的手段；
- quota/permission/entitlement 明确拒绝时暂停该账号并记录；
- 只获取当前正常登录会话实际可访问/授权返回的媒体；
- 不把真实 Cookie、Token、Profile、原始未脱敏 HAR/响应写入 Git。

## Records in this workstream

- `PRODUCT_CONTRACT.md` — 本轮已锁定产品合同；
- `CODE_AUDIT_2026-08-31.md` — 现有代码审计与复用/重构判断；
- `IMPLEMENTATION_PLAN.md` — 分 Gate 实施计划；
- `DECISION_LOG.md` — 本轮关键架构决策；
- `TEST_LOG.md` — 仅记录本 workstream 的测试证据；
- `STATUS.md` — 当前状态和下一动作。

历史 POC 的 `docs/TEST_LOG.md`、`evidence/` 等保持原状，不把本轮测试记录追加到旧记录里。