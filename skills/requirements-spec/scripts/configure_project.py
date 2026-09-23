from pathlib import Path
import sys


START = "<!-- requirements-spec:start -->"
END = "<!-- requirements-spec:end -->"


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：python3 configure_project.py <项目根目录>")
        return 2

    project = Path(sys.argv[1]).expanduser().resolve()
    if not project.is_dir():
        print(f"项目目录不存在：{project}")
        return 2

    target = project / "AGENTS.md"
    if target.is_symlink():
        print(f"项目规则文件是符号链接，请检查实际目标：{target}")
        return 2

    snippet = (Path(__file__).resolve().parents[1] / "assets" / "AGENTS-项目片段.md").read_text(encoding="utf-8").strip()
    existing = target.read_text(encoding="utf-8") if target.exists() else ""

    if (START in existing) != (END in existing):
        print(f"项目规则片段标记不完整，未修改：{target}")
        return 2

    if START in existing:
        before, remainder = existing.split(START, 1)
        _, after = remainder.split(END, 1)
        updated = before + snippet + after
        action = "已更新需求入口"
    elif "使用已安装的 `requirements-spec` skill" in existing:
        print(f"已存在需求技能入口，未重复添加：{target}")
        return 0
    else:
        updated = existing.rstrip() + ("\n\n" if existing.strip() else "") + snippet + "\n"
        action = "已添加需求入口"

    if updated != existing:
        target.write_text(updated, encoding="utf-8")
    else:
        action = "入口已是最新"

    print(f"{action}：{target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
