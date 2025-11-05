# ManimGL 物理动画迁移指南

## 1. 核心模块树速览
- **Scene**：负责动画生命周期、时间推进与窗口交互，构造时创建 `Camera`、`SceneFileWriter` 并维护渲染分组，是所有场景的宿主。【F:manimlib/scene/scene.py†L1-L357】
- **Animation**：封装插值与节奏控制，`begin → update_mobjects → interpolate → finish` 流程统一管理动画目标与时间跨度。【F:manimlib/animation/animation.py†L1-L199】
- **Mobject**：提供层级树、数据缓冲与更新器（updater），`add_updater`/`update` 用于把外部状态映射到画面。【F:manimlib/mobject/mobject.py†L820-L903】
- **Renderer**：由 `Camera` 负责 moderngl 上下文、FBO 与像素导出，`SceneFileWriter` 负责帧写出、音频合成与 FFmpeg 调用。【F:manimlib/camera/camera.py†L1-L177】【F:manimlib/scene/scene_file_writer.py†L1-L200】

## 2. 运行环境搭建与验证
1. 安装系统依赖（FFmpeg、OpenGL、可选 LaTeX/Pango），然后执行 `pip install -e .` 或 `pip install manimgl`，最后用 `manimgl example_scenes.py OpeningManimExample` 做冒烟测试。【F:README.md†L19-L104】
2. 离线/受限环境中安装 `requirements.txt` 可能因缺失包而失败（本环境无法通过代理获取 addict）。遇到类似错误时可改为使用离线轮子或跳过可选依赖后再逐项补齐。【3de791†L1-L4】【ffacc9†L1-L7】
3. 验证 Python 端语法可以运行 `python -m compileall example_scenes.py`，保证示例和新场景在无渲染依赖时也能通过静态检查。

## 3. 渲染主循环与调试插桩
- 主流程：`Scene.run()` 初始化文件写入器并顺序调用 `setup → construct → interact → tear_down`；适合在 `construct` 前后打断点观察场景初始化。【F:manimlib/scene/scene.py†L157-L195】
- 时间推进：`update_frame` 负责增加逻辑时间、执行所有 updater、捕获相机帧并在需要时限速；在此加入日志可追踪每帧耗时或窗口事件。【F:manimlib/scene/scene.py†L247-L272】
- 帧写出：`emit_frame` 调用 `SceneFileWriter.write_frame` 写入像素；在 `SceneFileWriter` 中可以通过覆写 `open_movie_pipe` 或添加日志监控 FFmpeg 状态。【F:manimlib/scene/scene.py†L274-L279】【F:manimlib/scene/scene_file_writer.py†L33-L200】
- 调试时间轴：`progress_through_animations` 按 dt 推进所有动画，若需要断点分析 easing，可在循环内部插入调试输出。【F:manimlib/scene/scene.py†L559-L620】

## 4. 动画插值与 easing
- `Animation` 在 `begin` 阶段复制起始对象、应用 `lag_ratio`，并在 `interpolate_mobject` 中遍历所有家族成员，支持子对象错峰动画。【F:manimlib/animation/animation.py†L63-L182】
- `rate_functions` 提供平滑、过冲、往返等缓动函数，可通过 `Animation.set_rate_func` 或 `Scene.play(..., rate_func=...)` 切换曲线。【F:manimlib/utils/rate_functions.py†L1-L107】
- 复合动画时，场景统一调用 `update_mobjects(dt)` 推动带 updater 的对象，与 `Animation.update_mobjects(dt)` 协同，保证外部状态与插值一致。【F:manimlib/scene/scene.py†L283-L289】【F:manimlib/animation/animation.py†L105-L122】

## 5. 物理状态映射到 Mobject
- `Mobject.add_updater` 支持把闭包绑定到对象，Manim 会在每帧自动调用并传入 dt；可通过 `suspend_updating` 控制嵌套更新，避免递归状态错乱。【F:manimlib/mobject/mobject.py†L820-L888】
- 渲染批次通过 `Scene.assemble_render_groups` 按类型、着色器与 z-index 分类，设计新物体时保持统一 Shader/Wrapper 可减少状态切换。【F:manimlib/scene/scene.py†L319-L333】
- 外部物理数据应在 updater 内部执行有限步长积分、再更新 Mobject 几何，避免在 `construct` 阶段直接写死关键帧。

## 6. 引擎契约与渲染步骤
1. **初始化**：`Scene.__init__` 合并全局/局部配置，创建 `Camera`/`SceneFileWriter` 并把 `frame` 作为首个 Mobject。【F:manimlib/scene/scene.py†L72-L133】
2. **构建场景**：`construct` 中通过 `add`/`remove` 维护 `mobjects`，内部自动重排 z-index 并更新渲染批。【F:manimlib/scene/scene.py†L319-L359】
3. **播放动画**：`Scene.play` 链式执行 `pre_play → begin_animations → progress_through_animations → finish_animations → post_play`，期间自动写帧与播放音频。【F:manimlib/scene/scene.py†L536-L620】
4. **渲染输出**：`SceneFileWriter` 根据配置决定是否拆分片段、是否写入音频，并在 `finish` 时关闭所有流。【F:manimlib/scene/scene_file_writer.py†L187-L200】
5. **写出视频**：默认配置中使用 `ffmpeg`+`libx264`，可在 `manimlib/default_config.yml` 里调整分辨率、帧率与编码格式。【F:manimlib/default_config.yml†L49-L108】

## 7. 自定义物理动画骨架
- 新增的 `PhysicsDrivenSpring` 示例展示了“物理状态 → updater → 渲染”链路：`SpringState.integrate` 使用半显式欧拉法推进弹簧状态，`SpringMass.update_from_state` 将位置/速度映射成点与速度箭头，`spring` 线条在 updater 中同步长度，并驱动面板读数更新。【F:example_scenes.py†L725-L857】
- 在 `advance_state` 中对大 dt 进行细分，确保数值稳定；示例同时设置了位置/速度裁剪，避免越界导致画面闪烁。【F:example_scenes.py†L832-L857】
- 运行命令：`manimgl example_scenes.py PhysicsDrivenSpring -p -w`，建议在安装完依赖后执行以验证整条渲染链路（可结合 `-s` 仅输出末帧）。

## 8. 性能与扩展建议
- 默认相机为 1920×1080@30fps，可通过 CLI（`-l/-m/--hd/--uhd`）或配置文件调节分辨率；同时支持多重采样（`Camera(samples)`）控制抗锯齿。【F:manimlib/default_config.yml†L49-L108】【F:manimlib/camera/camera.py†L34-L104】
- 渲染同步逻辑通过虚拟时间与真实时间对比做限速，可在 `Scene.update_frame` 中监测 `time.sleep` 触发频率来评估 CPU/GPU 负载。【F:manimlib/scene/scene.py†L247-L272】
- 对实时交互或批量更新场景，优先减少 Shader 切换、复用共享纹理，并在 updater 中避免大量 Python 分配（示例中复用 `SpringState` 实例与数值对象）。

## 9. 迁移经验与常见陷阱
- **依赖分辨**：确认使用的是 ManimGL（`manimgl` 包），否则 API 与社区版不兼容。【F:README.md†L19-L52】
- **数值稳定**：长时间物理仿真需限制 dt，并准备 `position_limit`/`velocity_clip` 防止对象移出视野（示例已实现裁剪逻辑）。【F:example_scenes.py†L725-L857】
- **资源输出**：渲染音频时确保 `sounds` 目录可访问，`SceneFileWriter` 会在缺失文件时抛异常，可提前检查路径或覆写 `get_full_sound_file_path`。【F:manimlib/scene/scene_file_writer.py†L137-L183】
- **调试策略**：利用 `Scene.interact()` 进入交互循环，并结合 `Scene.temp_record()`/`temp_skip()` 快速定位耗时段，避免全量渲染来回切换。【F:manimlib/scene/scene.py†L197-L420】
- **配置同步**：在多项目共用 Manim 时，把 `custom_config.yml` 放在项目根目录，确保输出目录、字体与缓存一致，避免跨平台字体差异导致布局错位。【F:manimlib/default_config.yml†L11-L108】

> 建议把本文档连同示例场景作为团队新成员的入门材料，并在私有仓库中补充针对业务模型的 updater 模板，形成可重复使用的物理动画基线。
