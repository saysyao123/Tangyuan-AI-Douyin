# R1S01 Data Source Proof｜BGM 数据源最小验证

> 目的：只验证 `抖音账号热门音乐面板 → 具体音乐实体 → 音频 → 试听片段`，不进入 MV 后续阶段。

## PASS 条件

至少用 1 首真实 BGM 完成：

1. 从当前抖音创作者中心账号的「选择音乐 / 热门榜」读取候选；
2. 证明候选当前存在「使用」入口；
3. 尽可能锁定具体音乐实体（music_id / 版本 / 作者 / 链接）；
4. 获取对应音频文件；
5. 裁出一段 15–30 秒试听片段；
6. 用户能直接试听并判断是否与自己在抖音听到的热门版本一致。

本轮不要求一次解决 7 日历史排名；先证明“今天的真实音乐实体和试听链路”可以稳定跑通。

---

## 当前执行分流

### Path A｜Codex 电脑完整验证（推荐）

如果当前电脑具备 Git / Python / pip / Playwright / ffmpeg，则按下文 Step A–E 执行。

如果当前电脑环境不具备这些依赖，不要求用户现场安装修复；将完整验证交给 Codex-capable computer。Codex 的正式要求见：

`CODEX_TEST_REQUIREMENT.md`

### Path B｜无本地运行环境的临时验证（当前可做）

用户只需要从抖音 App 提供：

- 一个具体音乐的分享链接；或
- 一个正在使用目标热门 BGM 的代表视频分享链接；
- 如方便，可附音乐页/视频页里显示音乐名称的截图。

系统负责在公开可访问范围内尝试：

1. 锁定具体歌曲/版本/作者及可识别的音乐实体信息；
2. 对照同名不同 Remix / 翻唱 / 原版，避免只按歌名匹配；
3. 查找当前公开样本和相关热度信号；
4. 如果存在无需绕过登录/DRM即可访问的公开播放源，只使用短试听片段/公开预览做版本识别；
5. 输出 `ENTITY_CONFIDENCE` 与仍缺失的账号侧验证项。

Path B 可以验证“实体识别 + 试听判断”是否可行，但不能替代账号侧 `AVAILABLE_AT_BUILD`。完整 Gate 仍需后续 Codex 电脑完成。

---

## Step A｜读取你账号当前「热门榜」

### Windows PowerShell

先切到测试分支并进入 Probe 目录：

```powershell
git fetch origin
git checkout test/mv-round-01
cd .\06_TESTS\MV\ROUND_01\R1S01_DATASOURCE
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
python .\probe_creator_music.py --topn 30
```

脚本会打开一个 Chromium 窗口。

### 你只需要做什么

第一次运行时，如果抖音要求登录：

1. 在浏览器中正常完成登录 / 验证码；
2. 不需要手动选歌、不需要发布；
3. 登录完成后保持浏览器打开，脚本会继续尝试打开「选择音乐 / 热门榜」。

脚本完成后会生成：

```text
r1s01_probe_output/
├─ summary.json
├─ creator_music_panel.json
├─ creator_music_network.json
└─ creator_music_panel.png
```

这些是**本地私有测试证据**，目录已被 `.gitignore` 排除。不要把浏览器 Profile、Cookie 或 Probe 原始输出提交到公开 GitHub。

### 最低验证标准

`summary.json` 中应满足：

```text
success = true
captured_rows > 0
use_button_count > 0
```

截图里应能看到当前账号真实的「热门榜」音乐面板。

> 如果 `network_music_responses > 0`，说明我们还抓到了音乐面板背后的网络数据，后续有机会直接提取 music_id、播放地址、使用量等字段。Probe 不持久化网络 URL 的 query 参数，以避免把临时 token 当测试证据保存。

---

## Step B｜从网络响应提取具体音乐实体

```powershell
python .\extract_music_entities.py .\r1s01_probe_output\creator_music_network.json --out .\r1s01_probe_output\music_entities.json
```

验证目标：输出至少一个可识别的 `music_id + title`，最好同时包含作者、use_count、share_url 或 play_url。

如果这一步暂时提取不到 music_id，不代表 Step A 失败；需要检查网络响应真实字段，再调整提取器。

---

## Step C｜取得具体音乐音频

R1 暂时不复制第三方下载器源码到主仓库。先使用已验证活跃的开源项目：

- `jiji262/douyin-downloader`

它支持 `/music/{music_id}`，优先获取音乐直接音频，拿不到时回退到该音乐下的关联作品。

建议先回到本仓库根目录，再把外部参考项目放进已忽略/独立的 `_external` 目录：

```powershell
cd ..\..\..\..
mkdir _external -ErrorAction SilentlyContinue
git clone https://github.com/jiji262/douyin-downloader.git _external\douyin-downloader
cd .\_external\douyin-downloader
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy config.example.yml config.yml
python -m tools.cookie_fetcher --config config.yml
```

浏览器中完成一次抖音登录后回到终端按 Enter，让项目保存当前登录 Cookie。

得到 `music_id` 后，以真实 ID 替换：

```powershell
python run.py -c config.yml -u "https://www.douyin.com/music/MUSIC_ID" -p .\Downloaded
```

### 这一层的验证标准

输出目录里必须出现可播放的音频文件，并且 metadata 能对应同一个 music_id / 歌名 / 作者。

---

## Step D｜剪出试听片段

回到 `R1S01_DATASOURCE`：

```powershell
python .\build_preview.py "D:\path\to\downloaded_audio.mp3" --start 0 --duration 24 --out .\r1s01_probe_output\preview_24s.m4a
```

第一轮如果还没锁定热门截取起点，可以先 `--start 0` 验证裁剪链路。

后续拿到同音频样本 / 热门截取模板后，再把 `--start` 换成真实热门起点。

### 试听验证

用户只需要试听 `preview_24s.m4a`，确认：

- 是不是自己在抖音近期听到的那个版本；
- 这个片段是否有做 MV 的欲望；
- 是否需要换版本 / 换截取模板。

---

## Step E｜账号可用性双 Gate（后续固定）

制作开始前：

`AVAILABLE_AT_BUILD = TRUE`

发布前再次确认：

`AVAILABLE_AT_PUBLISH = TRUE`

两次都必须基于当前账号的抖音音乐面板，而不是只凭本地音频文件。

---

## 本次需要回传的文件

完整 Path A 第一次先只跑 Step A + Step B，然后把以下内容**发到当前 ChatGPT 对话，不要提交到公开 GitHub**：

```text
summary.json
creator_music_panel.json
creator_music_network.json
music_entities.json（如果生成成功）
creator_music_panel.png
```

不要手工修这些 JSON；失败结果同样是 R1 的正式测试证据。

Path B 不需要这些本地文件，只需要一个真实抖音音乐/视频分享链接作为实体识别入口。

---

## 当前第三方参考项目

- `zJay26/douyin-skills`：参考真实 Creator Center 音乐面板、热门榜与“使用”按钮的浏览器交互方式。
- `jiji262/douyin-downloader`：参考 music_id 音乐详情、同音乐作品列表、直接音频下载与 Cookie / 风控处理。
- `zhangshuai/douyin-go`：参考抖音开放平台音乐榜单结构（rank / use_count / share_url 等）；官方榜单权限作为后续长期数据源候选。

R1 不把第三方项目直接复制进 Runtime；先用 PoC 证明链路，再决定需要抽取哪一小部分能力进入正式系统。
