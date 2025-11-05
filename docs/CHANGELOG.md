# Changelog

## Unreleased

### Added
- 新增《ManimGL 物理动画迁移指南》，梳理核心模块、调试流程与性能建议，便于团队快速熟悉引擎契约。【F:docs/physics_engine_migration.md†L1-L54】
- 增补 `PhysicsDrivenSpring` 示例，演示外部物理状态通过 updater 驱动场景的最小骨架。【F:example_scenes.py†L725-L857】

### Changed
- 无。

### Fixed
- 无。

### Perf
- 无。

### Safety
- 文档内强调数值积分步长与裁剪策略，降低长时间仿真发散风险。【F:docs/physics_engine_migration.md†L37-L49】
