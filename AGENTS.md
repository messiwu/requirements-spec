# 仓库协作规则

- [KNOWN] 本仓库是 `requirements-spec` 单技能仓库，技能入口是根目录 `SKILL.md`。
- [INFERRED] 修改技能行为时保持入口简洁；只在相应任务分支中加载的细节放入 `references/`。
- [INFERRED] 新增规则必须对应可复现的需求失败，说明适用范围，避免由一个案例推导通用硬约束。
- [INFERRED] 修改方法、模板或示例后检查交叉引用和术语一致性。
- [KNOWN] 完成变更后运行 `python3 scripts/validate_skill.py`。
- [INFERRED] 文档使用简体中文；代码注释使用简体中文。

[RULES I BROKE]: 无。
