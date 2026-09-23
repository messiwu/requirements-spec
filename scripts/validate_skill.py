from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "LICENSE",
    "README.md",
    "agents/openai.yaml",
    "assets/AGENTS-项目片段.md",
    "scripts/configure_project.py",
    "references/01-设计依据与边界.md",
    "references/02-agent工作规程.md",
    "references/03-质量审查与交接.md",
    "references/04-场景扩展与配图.md",
    "references/模板/00-交接索引.md",
    "references/模板/01-需求规格.md",
    "references/模板/02-依据与决策.md",
    "references/模板/03-验收与追溯.md",
]


def check_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"缺少必需文件：{relative}")


def check_frontmatter(errors: list[str]) -> None:
    content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        errors.append("SKILL.md 缺少有效 YAML frontmatter")
        return
    frontmatter = match.group(1)
    if not re.search(r"^name:\s*requirements-spec\s*$", frontmatter, re.MULTILINE):
        errors.append("SKILL.md 的 name 必须是 requirements-spec")
    if not re.search(r"^description:\s*\S.+$", frontmatter, re.MULTILINE):
        errors.append("SKILL.md 缺少非空 description")


def check_links(errors: list[str]) -> int:
    count = 0
    for markdown in ROOT.rglob("*.md"):
        content = markdown.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            count += 1
            relative = target.split("#", 1)[0].strip("<>")
            if relative and not (markdown.parent / relative).resolve().exists():
                errors.append(f"失效链接：{markdown.relative_to(ROOT)} -> {target}")
    return count


def check_project_setup(errors: list[str]) -> None:
    script = ROOT / "scripts" / "configure_project.py"
    with tempfile.TemporaryDirectory() as temporary:
        project = Path(temporary) / "project"
        project.mkdir()
        agents = project / "AGENTS.md"
        agents.write_text("# 原有规则\n\n保留。\n", encoding="utf-8")
        first = subprocess.run(
            [sys.executable, str(script), str(project)],
            text=True,
            capture_output=True,
        )
        if first.returncode != 0:
            errors.append(f"项目接入脚本首次执行失败：{first.stderr or first.stdout}")
            return
        initial = agents.read_text(encoding="utf-8")
        second = subprocess.run(
            [sys.executable, str(script), str(project)],
            text=True,
            capture_output=True,
        )
        repeated = agents.read_text(encoding="utf-8")
        if second.returncode != 0:
            errors.append(f"项目接入脚本重复执行失败：{second.stderr or second.stdout}")
        if initial != repeated:
            errors.append("项目接入脚本重复执行后改变了文件")
        if "保留。" not in repeated:
            errors.append("项目接入脚本覆盖了原有规则")
        if repeated.count("<!-- requirements-spec:start -->") != 1:
            errors.append("项目需求入口出现次数不等于 1")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_frontmatter(errors)
    links = check_links(errors)
    check_project_setup(errors)

    if errors:
        for error in errors:
            print(f"错误：{error}")
        return 1

    markdown_count = len(list(ROOT.rglob("*.md")))
    print(f"检查通过：{markdown_count} 份 Markdown，{links} 个内部链接，项目接入脚本幂等。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
