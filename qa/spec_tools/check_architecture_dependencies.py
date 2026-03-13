from __future__ import annotations

import argparse
import ast
import fnmatch
import json
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULES = PROJECT_ROOT / "spec" / "architecture" / "dependency-rules.json"


@dataclass(frozen=True)
class DependencyRule:
    id: str
    description: str
    source_glob: str
    deny_module_prefixes: tuple[str, ...]
    exclude_files: tuple[str, ...]


def _load_rules(path: Path) -> tuple[Path, list[DependencyRule]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    python_root = PROJECT_ROOT / payload.get("python_root", "backend/app")
    rules: list[DependencyRule] = []
    for item in payload.get("rules", []):
        rules.append(
            DependencyRule(
                id=item["id"],
                description=item["description"],
                source_glob=item["source_glob"],
                deny_module_prefixes=tuple(item.get("deny_module_prefixes", [])),
                exclude_files=tuple(item.get("exclude_files", [])),
            )
        )
    return python_root, rules


def _module_from_path(python_root: Path, file_path: Path) -> str:
    rel = file_path.relative_to(python_root).as_posix()
    stem = rel[:-3] if rel.endswith(".py") else rel
    parts = [part for part in stem.split("/") if part]
    return ".".join(["app", *parts])


def _resolve_from_import(current_module: str, node: ast.ImportFrom) -> set[str]:
    package_parts = current_module.split(".")[:-1]
    targets: set[str] = set()

    if node.level == 0:
        if node.module:
            targets.add(node.module)
        return targets

    up = max(node.level - 1, 0)
    base_parts = package_parts[: max(0, len(package_parts) - up)]
    if node.module:
        module_parts = [part for part in node.module.split(".") if part]
        targets.add(".".join([*base_parts, *module_parts]))
        return targets

    for alias in node.names:
        if alias.name == "*":
            targets.add(".".join(base_parts))
        else:
            targets.add(".".join([*base_parts, alias.name]))
    return targets


def _collect_imports(python_root: Path, file_path: Path) -> set[str]:
    module_name = _module_from_path(python_root, file_path)
    tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.update(_resolve_from_import(module_name, node))
    return {item for item in imports if item}


def run_check(rules_path: Path) -> int:
    python_root, rules = _load_rules(rules_path)
    python_files = sorted(path for path in python_root.rglob("*.py") if path.is_file())

    violations: list[str] = []
    checked = 0
    for file_path in python_files:
        rel_file = file_path.relative_to(PROJECT_ROOT).as_posix()
        imports = _collect_imports(python_root, file_path)
        for rule in rules:
            if not fnmatch.fnmatch(rel_file, rule.source_glob):
                continue
            if any(fnmatch.fnmatch(rel_file, pattern) for pattern in rule.exclude_files):
                continue
            checked += 1
            for imported_module in imports:
                if not imported_module.startswith("app."):
                    continue
                if any(imported_module.startswith(prefix) for prefix in rule.deny_module_prefixes):
                    violations.append(
                        f"{rule.id}: {rel_file} imports forbidden module `{imported_module}` "
                        f"({rule.description})"
                    )

    if violations:
        print("Architecture dependency check FAILED")
        for item in violations:
            print(f"- ERROR: {item}")
        print(f"- Rules applied: {len(rules)}; file-rule checks: {checked}")
        return 1

    print("Architecture dependency check PASSED")
    print(f"- Rules applied: {len(rules)}; file-rule checks: {checked}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check architecture dependency rules for backend modules.")
    parser.add_argument(
        "--rules",
        type=Path,
        default=DEFAULT_RULES,
        help="Path to architecture dependency rules JSON (default: spec/architecture/dependency-rules.json).",
    )
    args = parser.parse_args()
    return run_check(args.rules)


if __name__ == "__main__":
    raise SystemExit(main())
