# GNM Avatar · 单目视频 3D Talking Head 重建

基于 Google **GNM Head**（Generative aNthropometric Model）的单目说话视频 3D 头像重建：
身份 / 逐帧表情 / 头部姿态联合优化 + 从视频烘焙 UDIM 纹理，在 RAVDESS 与 HDTF 上的演示。

**在线页面（GitHub Pages）：** https://caesarrwang.github.io/avatar_gnome/
本地查看：`git clone` 后直接双击 `index.html` 即可（图片、视频和 3D 模型都通过普通 `<script>`/相对路径加载，不需要起静态服务）。

## 内容

- **GNM 模型内部细节** — 前向模型公式、253 维身份 / 383 维表情基、4 关节 LBS 与姿态修正、46 个顶点组、UDIM UV、68 关键点定义、语义采样器。
- **重建方法** — FAN 68 点关键点 → 两阶段 Adam 联合优化（共享身份与焦距，逐帧表情/姿态，采样器先验 + 时域平滑）→ 全网格导出 → 纹理烘焙（深度可见性 + cos⁴ 加权 + push-pull 补洞）。
- **结果演示** — RAVDESS Actor_24 11 段（5,276 帧，4.96 px）与 HDTF 6 段（4,475 帧，4.31 px）的六列对比视频（含音轨）、可交互的贴图 3D 模型、纹理 tile 与定量表格。

## 进展记录（独立页面）

`texture.html` 记录主报告之后的工作，内容不与主报告混排：四条全头纹理路线的对比（Hunyuan3D-2 Paint、生成环绕视频反投影、真实像素混合、生成式重绘 UV）、把生成视频对齐到网格（逐帧位姿、关键点扭正、光流精修）、眼球贴图规范与逐帧眼球转动、渲染时计算的眼部高光、牙齿调色，以及遗留问题。
在线地址：https://caesarrwang.github.io/avatar_gnome/texture.html
它的素材单独放在 `assets/tex/`，由工作目录的 `scripts/make_texture_page_assets.py` 与 `scripts/make_texture_page_videos.sh` 生成。

## 目录

```
index.html            主报告页面
texture.html          进展记录页面（纹理 / 眼球 / 高光），素材在 assets/tex/
assets/img/           图表（GNM 可视化、流程分解、纹理）
assets/models/        可交互 3D 模型（GLB + 同名 .glb.js base64 数据脚本，three.js 加载）
assets/js/            自托管 three.js r160 打包（three-bundle.js）
assets/video/         演示视频（H.264 + AAC，六列：源 | 关键点 | 网格叠加 | 网格灰底 | 贴图叠加 | 贴图灰底）
```

## 更新页面

修改后先运行 `python tools/stamp_version.py`（给所有资源链接加版本号并写入页脚 build 标记，避免浏览器 / GitHub Pages 缓存旧资源），再提交推送。

## 复现

代码位于工作目录 `test_gnm_recons/scripts/`（`detect_landmarks.py`、`fit_gnm.py`、`bake_texture.py`、`render_results.py`、`make_report_assets.py`），
一键脚本 `run_actor24.sh`（RAVDESS）与 `run_hdtf.sh <clip> ...`（HDTF）。
环境：Python 3.12、PyTorch 2.11 (cu128)、GNM (commit abbad03)、face-alignment、pyrender 0.1.45 + EGL。

## 引用

- Ploumpis et al., *GNM Head: A Generative aNthropometric Model of the human head*, 2026. arXiv:2607.23687. https://github.com/google/GNM
- Bulat & Tzimiropoulos, *How far are we from solving the 2D & 3D Face Alignment problem?*, ICCV 2017.
