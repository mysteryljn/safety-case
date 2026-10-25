# safety-case

把安全论证的 claim、argument 和 evidence 建成一个可检查的 JSON 图。工具检测孤立 claim、缺失证据、悬空引用和循环依赖，帮助 ISO 26262 工作产品在评审前形成可追踪的最小闭环。

## 痛点

功能安全项目的证据常散落在测试报告、表格和邮件中，变更后很难知道哪个安全主张失去支撑。本工具不替代认证工具链，但提供可版本化、可审查的安全论证骨架。

## 使用

    python safetycase.py examples/case.json

## 许可证

MIT
