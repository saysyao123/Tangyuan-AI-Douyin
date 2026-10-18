> 最新续作状态：请先读 [T33_PROGRESS.md](T33_PROGRESS.md) 与 [T33 RELEASE](../evidence/T33_20261018/RELEASE.json)。以下 T32 记录保留为历史。

# T32 唯一续作状态｜R2 第一幕美术验收版已发布

更新时间：2026-10-18。**最终用户审美尚待确认，项目完成仍为 FALSE；不能把技术通过替代最终美术认可。**

试玩：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/chapter/

四图、实际对白与动作、QA：https://lantern-inn-act1-t32.ardentfern6.chatgpt.site/review/

## 目标和锁定规则

继续 Type PAL 固定上游 f98d0ddd89ebdee7b04502ee35de26ee82c6d246 与 T22 完整网页，第一幕 fair→backstage→street→courtyard。对照 T19 V2，完成统一的高细节像素场景、角色/NPC、步态、演出及头像。保留剧情、地图、碰撞、脚点、键盘、点击寻路、SAVE12 和自愿提示；不扩写后续剧情，不新增第一幕战斗，不覆盖 main 或原正式 Site。

## 当前实际成果

上一版已整合四场景高清房屋、戏台、摊车、树、院墙、药炉、地面，双主角与六类 NPC 方向图、步态、倒地、抬走、蹲下。

R2 补齐八张同身份头像，原图 256×288、实际固定 64×72 逻辑尺寸；正文、姓名、分页不变，第一幕之外保持旧资源。实际第一幕六种说话身份用原生交互验收；访客/演员资源只解码，不发明对白。后台右墙换为完整门窗/顶梁/柱/茶具与毛巾，左墙保留戏服/面具/镜子；按原墙平面投影，箱子去掉室内积雪。

本轮还修正旧示例残留：help.html 改为当前第一幕路线，新增 109 个原生工程文件的 first-act-project.zip；旧示例作为历史保留。高清渲染代码与素材另在对应源码包，编辑器默认预览仍是原生小图。最新整站 ZIP 已替换原交付文件，包含当前下载和审查页。

## 已证明及复用

- 完整空存档第一幕购买分享→演出→后台→旧街→小院→归家、保存重开、旧工程隔离与网页，Run39088306145 九项 PASS；不重复未受影响流程。
- R2 Run39093310372 Chromium/Firefox 各五项真实对白与头像检查 PASS，零 pageerror。WebKit 临时隐私会话在缩略图 Blob 入库处失败，该运行没有发布。
- R2 Run39093766720 使用正常持久会话完成 WebKit 五项 PASS；原生后台倒地、抬走和存档重开两项 PASS。没有改存档格式或模拟存储。
- 新构建 238 个 chapter 文件与先前 Chromium/Firefox 通过版本逐字节一致，109 个原生项目文件与固定 T30 基线一致；本次部署同样复用这 238 个实测文件，806 项运行清单及帮助/审查页链接、本地下载校验通过。
- 三种引擎为 Linux CI 实机；没有冒称真实手机、Safari 应用或发布域重跑全程。WebKit 隐私会话限制保留。

## 发布与固定版本

- 开发分支：feature/t32-act1-art-integration-20261018
- R2 来源：7826619a61d978c73c7a26d0288d9c335c371953
- 实际运行固定 SHA：7e6eba44758bae5d758b6443dc672fcf60f54891
- 同一隔离 Site：appgprj_6ad427757a608191a95a42cc68b1f19b
- Site 源提交：2154eae99251a6ce826a9ce69b30bbf090bcf904
- 发布版本：appgprj_6ad427757a608191a95a42cc68b1f19b~appgver_f6adab4d4500819197a1ff554f016abf
- 部署：appgdep_6ad48785980881919d6d111695a4827b，状态 succeeded
- 原正式 Site appgprj_6ad1b7b5f0bc81919dcf871ecce85086 与 GitHub main 未修改。回滚运行基线：146298ede54a65025ab7a794b49ab53c4bf3ae92。

## 下一次唯一入口

先读本页、docs/T32_R2_REVIEW.md 和 evidence/T32_20261018/RELEASE.json，再核对用户对当前实机画面的反馈，只修未通过对象。不要重启引擎、重做网页、重跑未变旧测试，也不要将后续“继续”理解为扩写第二幕。素材清单中的早期 pending 字样属于构建时状态；实际 QA 与发布真值以本页和 RELEASE.json 为准。

尚未完成：最终用户审美认可、真实手机/Safari 应用验证。合成对白仍与原书私有文本分开，不自动跨域迁移存档。
