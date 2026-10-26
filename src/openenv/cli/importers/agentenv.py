"""AgentEnv bundle source importer."""

from __future__ import annotations

import json
from pathlib import Path

from .base import (
    append_dependency_files,
    collect_source_dependencies,
    DetectedEnvironment,
    iter_directories,
    prepare_import_package,
    render_importer_template,
    write_text,
)


_AGENTENV_DEPENDENCY = "agentenv-framework>=0.9.1360"
_REQUIRES_PYTHON = ">=3.11.4"


def _is_task_file(path: Path) -> bool:
    try:
        steps = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return False
    return (
        isinstance(steps, list)
        and bool(steps)
        and all(
            isinstance(step, dict) and isinstance(step.get("type"), str)
            for step in steps
        )
    )


def detect_agentenv_bundles(source: Path) -> list[DetectedEnvironment]:
    """Detect AgentEnv bundles, folders whose tasks/ holds task files, without importing source."""
    source = source.resolve()
    matches: list[DetectedEnvironment] = []

    for tasks_dir in iter_directories(source, "tasks"):
        if not any(_is_task_file(path) for path in sorted(tasks_dir.glob("*.json"))):
            continue
        bundle = tasks_dir.parent
        matches.append(
            DetectedEnvironment(
                source_type="agentenv",
                class_name=bundle.name,
                module_path=""
                if bundle == source
                else bundle.relative_to(source).as_posix(),
                file_path=bundle,
            )
        )

    return matches


def _app_source(*, vendor_dir: str, bundle_path: str) -> str:
    return render_importer_template(
        "agentenv_app.py.tpl",
        bundle=f"{vendor_dir}/{bundle_path}" if bundle_path else vendor_dir,
    )


class AgentEnvImporter:
    """Importer for AgentEnv bundles, served by agentenv-framework's OpenEnv server."""

    source_type = "agentenv"

    def detect(self, source: Path) -> list[DetectedEnvironment]:
        return detect_agentenv_bundles(source)

    def generate(
        self,
        *,
        source: Path,
        destination: Path,
        env_name: str,
        detected: DetectedEnvironment,
    ) -> None:
        package = prepare_import_package(
            source, destination, env_name, vendor_dir=source.name
        )
        (destination / "server" / f"{env_name}_environment.py").unlink()
        write_text(
            destination / "server" / "__init__.py",
            f'"""{env_name} environment server: an AgentEnv bundle."""\n',
        )
        write_text(
            destination / "server" / "app.py",
            _app_source(
                vendor_dir=package.vendor_dir, bundle_path=detected.module_path
            ),
        )
        dependencies = collect_source_dependencies(source)
        if _AGENTENV_DEPENDENCY not in dependencies:
            dependencies.append(_AGENTENV_DEPENDENCY)
        append_dependency_files(
            destination, env_name, dependencies, requires_python=_REQUIRES_PYTHON
        )
