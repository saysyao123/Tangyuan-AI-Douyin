# DEPTH_MOTION_HARNESS v1.0

> 默认 DEPTH 方案。用于把公开舞蹈/动作参考视频转换为高细节 Depth Motion Reference，再供 Seedance 2.5 / 后续视频模型参考动作、重心、节奏与空间关系。

## 状态

- 2026-09-08：已实测通过。
- 基准素材：15.57s / 720×1280 / 30fps 抖音单人舞蹈。
- 云端执行：GitHub Actions 标准 Ubuntu runner（CPU）。
- 模型：Depth Anything V2 Small。
- 输出：Raw Depth / Temporal Depth / Original-vs-Depth 对比 / report.json。

## 锁定默认规则

1. 正式 DEPTH 默认采用：`GitHub Actions 云端 + Depth Anything V2 Small`。
2. 不再把轮廓分割、GrabCut、光流灰度代理等 Motion Proxy 作为正式 DEPTH 参考；它们仅允许用于极端情况下的快速预览。
3. 默认使用 Small 模型，不擅自升级 Base / Large / Giant。
4. 默认保持源视频 FPS、比例和时长；动作参考优先 15s–30s 连续段，不因方便擅自缩成 3–5s。
5. 默认同时产出：
   - `depth_v2_raw_h264.mp4`：高细节原始深度；
   - `depth_v2_temporal_h264.mp4`：光流辅助时序稳定版；
   - `original_vs_depth_h264.mp4`：人工 QA 对比版；
   - `report.json`：真实规格。
6. Seedance 动作参考优先使用 Temporal 版；Raw 版用于细节对照和必要时 A/B。
7. 输入视频优先选择：单人、主体清楚、遮挡少、镜头稳定、动作连续、关键肢体可见。
8. 如果目标包含“脚步不滑行 / 重心落脚”验证，素材必须完整看到脚部和地面接触；半身舞不允许代替脚步验证。

## 固定执行入口

仓库专用分支：`depth-worker`

核心文件：

- `.github/workflows/depth-cloud.yml`
- `06_TESTS/DEPTH_CLOUD/process_depth.py`
- `06_TESTS/DEPTH_CLOUD/job.json`

以后处理公开参考视频时，只更新 `depth-worker` 分支中的 `job.json`：

```json
{
  "source_url": "PUBLIC_VIDEO_URL",
  "fallback_url": "OPTIONAL_FALLBACK_URL",
  "artifact_name": "depth-job-name",
  "input_size": 518,
  "retention_days": 7
}
```

提交后自动触发云端 Depth Worker。

## 默认参数

- Model: Depth Anything V2 Small / ViT-S
- Input size: 518
- Device: GitHub Actions CPU
- Source FPS: preserve
- Source resolution/aspect: preserve output dimensions
- Depth normalization: EMA percentile normalization
- Temporal blend: current depth 0.82 + flow-warped previous depth 0.18
- Temporal cleanup: light bilateral filter
- Delivery codec: H.264 / yuv420p / faststart
- Artifact retention: 7 days
- Workflow timeout: 180 minutes

## QA Gate

正式使用前必须检查：

- 人体头、肩、躯干、手臂轮廓是否连续；
- 前后肢体遮挡关系是否合理；
- 手部主要动作是否仍可读；
- 躯干/骨盆重心变化是否可见；
- 快动作是否出现严重深度跳闪；
- Temporal 版是否减少闪烁但没有明显抹掉动作细节；
- 输出 FPS / 时长 / 分辨率是否与源素材一致；
- Seedance 只引用动作/重心/节奏，不复制原人物身份、服装、背景与妆容。

任一核心项不通过，不进入 Seedance Motion Reference 阶段。

## 费用与许可原则

- 当前仓库为 Public 时，使用 GitHub 标准 GitHub-hosted runner 的 Actions 计算按 GitHub 当前规则免费；禁止切换 Larger Runner，除非用户明确批准费用。
- Artifact 会占用 GitHub Actions / Packages 存储配额；默认只保留 7 天，并在结果已下载后优先清理，不把 Actions 当长期素材库。
- Depth Anything V2 Small 为 Apache-2.0；默认锁定 Small。Base / Large / Giant 的许可不同，不作为默认生产模型。
- 模型许可不等于输入素材版权许可。公开舞蹈视频用于动作研究/参考时，仍需独立考虑原视频、编舞、人物与发布用途的权利问题。

## 已知限制

1. GitHub 标准 runner 主要是 CPU，速度明显慢于 GPU；已验证 15.57s / 467 帧素材整套流程约为几十分钟级，而不是实时处理。
2. GitHub-hosted 单个 job 有最大执行时间；长视频应切段，而不是无限增加超时时间。
3. `depth-worker` 适合可由云端直接访问的公开 URL；私密/本地文件不能把敏感下载地址直接写进 Public 仓库。
4. 单目深度不是 3D 骨骼真值；快速手指、小物件、极端遮挡仍可能出现深度误判。
5. 时序稳定版是后处理增强，不等同于专门的视频深度时序模型；如未来出现同样免费、稳定且效果显著更好的云端方案，可做 A/B 后升级，但不得未经验证替换本默认路径。

## 变更规则

任何新 DEPTH 方案必须先与本方案做 A/B：

- 细节
- 时序稳定
- 动作/重心可读性
- 免费可用性
- 用户本机负担
- 处理速度
- 许可

只有整体明显优于当前方案，才允许替换默认 DEPTH Harness。
