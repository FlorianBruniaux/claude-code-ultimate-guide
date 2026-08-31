#!/usr/bin/env python3
"""Dependency-free state engine for the Claude Code learning-path example."""

from __future__ import annotations

import argparse
from datetime import date, timedelta
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Dict, List, Optional


STATE_RELATIVE_PATH = Path(".claude/learning/claude-code-guide-progress.json")
STATE_VERSION = 1


class ProgressError(ValueError):
    """Raised when local progress data is invalid or an action is unsafe."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ProgressError(message)


def load_path(path_file: Path) -> Dict[str, Any]:
    """Load the JSON subset of YAML used for this dependency-free example."""
    try:
        data = json.loads(path_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ProgressError("Learning-path definition is invalid") from error
    _require(isinstance(data, dict), "Learning-path definition is invalid")
    _require(data.get("schema_version") == 1, "Learning-path definition is unsupported")
    _require(data.get("review_intervals_days") == [1, 3, 7, 14, 30, 60, 90], "Review intervals are invalid")
    _require(isinstance(data.get("tracks"), dict), "Learning-path tracks are invalid")
    _require(isinstance(data.get("modules"), list), "Learning-path modules are invalid")
    _require(len(data["modules"]) == 7, "Learning path must contain seven modules")
    ids = [module.get("id") for module in data["modules"] if isinstance(module, dict)]
    _require(len(ids) == len(data["modules"]) and len(set(ids)) == len(ids), "Learning-path module ids are invalid")
    for module in data["modules"]:
        _require(all(isinstance(module.get(field), str) and module[field] for field in ("id", "title", "guide", "exercise")), "Learning-path module is invalid")
        _require(isinstance(module.get("prerequisites"), list), "Learning-path prerequisites are invalid")
    for track_name, track in data["tracks"].items():
        _require(isinstance(track_name, str) and isinstance(track, dict), "Learning-path track is invalid")
        _require(isinstance(track.get("modules"), list) and track["modules"], "Learning-path track modules are invalid")
        _require(all(module_id in ids for module_id in track["modules"]), "Learning-path track references an unknown module")
    return data


def state_path(root: Path) -> Path:
    return root / STATE_RELATIVE_PATH


def new_state(track: str) -> Dict[str, Any]:
    return {"version": STATE_VERSION, "track": track, "modules": {}}


def _validate_state(state: Any, path_data: Dict[str, Any]) -> Dict[str, Any]:
    """Reject state that is incompatible with the trusted path definition."""
    _require(isinstance(state, dict), "Progress state is corrupt")
    _require(type(state.get("version")) is int and state["version"] == STATE_VERSION, "Progress state is corrupt")
    _require(isinstance(state.get("track"), str) and state["track"] in path_data["tracks"], "Progress state is corrupt")
    modules = state.get("modules")
    _require(isinstance(modules, dict), "Progress state is corrupt")
    known_modules = _module_index(path_data)
    track_modules = set(path_data["tracks"][state["track"]]["modules"])
    for module_id, record in modules.items():
        _require(isinstance(module_id, str) and module_id in known_modules and module_id in track_modules, "Progress state is corrupt")
        _require(isinstance(record, dict), "Progress state is corrupt")
        _require(isinstance(record.get("completed_on"), str), "Progress state is corrupt")
        _require(isinstance(record.get("evidence"), str) and record["evidence"].strip(), "Progress state is corrupt")
        try:
            date.fromisoformat(record["completed_on"])
        except ValueError as error:
            raise ProgressError("Progress state is corrupt") from error
        _require(all(item in modules for item in known_modules[module_id]["prerequisites"]), "Progress state is corrupt")
    return state


def load_state(root: Path, path_data: Dict[str, Any]) -> Dict[str, Any]:
    """Read and validate state, leaving corrupt files untouched and unusable."""
    target = state_path(root)
    try:
        raw = target.read_text(encoding="utf-8")
        state = json.loads(raw)
    except FileNotFoundError as error:
        raise ProgressError("Progress state does not exist; run init first") from error
    except (OSError, json.JSONDecodeError) as error:
        raise ProgressError("Progress state is corrupt") from error
    return _validate_state(state, path_data)


def save_state(root: Path, state: Dict[str, Any], path_data: Dict[str, Any]) -> None:
    """Atomically replace the state file after validating the complete payload."""
    _validate_state(state, path_data)
    target = state_path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".progress-", suffix=".tmp", dir=str(target.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    except OSError as error:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise ProgressError("Could not save progress state") from error


def create_profile(root: Path, path_data: Dict[str, Any], track: str) -> Dict[str, Any]:
    _require(track in path_data["tracks"], "Unknown learning track")
    state = new_state(track)
    _validate_state(state, path_data)
    target = state_path(root)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=".progress-", suffix=".tmp", dir=str(target.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError as error:
            raise ProgressError("Progress state already exists; refuse to overwrite it") from error
    except OSError as error:
        raise ProgressError("Could not create progress state") from error
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
    return state


def _module_index(path_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {module["id"]: module for module in path_data["modules"]}


def _track_module_ids(state: Dict[str, Any], path_data: Dict[str, Any]) -> List[str]:
    try:
        return path_data["tracks"][state["track"]]["modules"]
    except KeyError as error:
        raise ProgressError("Progress state names an unknown track") from error


def complete_module(
    state: Dict[str, Any],
    path_data: Dict[str, Any],
    module_id: str,
    evidence: str,
    completed_on: Optional[date] = None,
) -> Dict[str, Any]:
    """Record a completion only when all prerequisites and evidence are present."""
    _validate_state(state, path_data)
    modules = _module_index(path_data)
    _require(module_id in modules, "Unknown module")
    _require(module_id in _track_module_ids(state, path_data), "Module is not in the selected track")
    _require(isinstance(evidence, str) and evidence.strip(), "Completion requires a non-empty evidence note")
    _require(module_id not in state["modules"], "Module is already complete")
    for prerequisite in modules[module_id]["prerequisites"]:
        _require(prerequisite in state["modules"], "Module %s requires %s" % (module_id, prerequisite))
    state["modules"][module_id] = {
        "completed_on": (completed_on or date.today()).isoformat(),
        "evidence": evidence.strip(),
    }
    return state


def next_module(state: Dict[str, Any], path_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the first incomplete module whose prerequisites are satisfied."""
    _validate_state(state, path_data)
    modules = _module_index(path_data)
    for module_id in _track_module_ids(state, path_data):
        module = modules[module_id]
        if module_id not in state["modules"] and all(item in state["modules"] for item in module["prerequisites"]):
            return module
    return None


def review_schedule(state: Dict[str, Any], path_data: Dict[str, Any], module_id: str) -> List[Dict[str, Any]]:
    _validate_state(state, path_data)
    _require(module_id in state["modules"], "Module is not complete")
    completed_on = date.fromisoformat(state["modules"][module_id]["completed_on"])
    return [
        {"module_id": module_id, "interval_days": interval, "due_on": (completed_on + timedelta(days=interval)).isoformat()}
        for interval in (1, 3, 7, 14, 30, 60, 90)
    ]


def due_reviews(state: Dict[str, Any], path_data: Dict[str, Any], on_date: Optional[date] = None) -> List[Dict[str, Any]]:
    _validate_state(state, path_data)
    today = on_date or date.today()
    return [
        review
        for module_id in sorted(state["modules"])
        for review in review_schedule(state, path_data, module_id)
        if date.fromisoformat(review["due_on"]) <= today
    ]


def status(state: Dict[str, Any], path_data: Dict[str, Any], on_date: Optional[date] = None) -> Dict[str, Any]:
    _validate_state(state, path_data)
    module_ids = _track_module_ids(state, path_data)
    completed = [module_id for module_id in module_ids if module_id in state["modules"]]
    return {
        "track": state["track"],
        "completed_modules": completed,
        "total_modules": len(module_ids),
        "next_module": next_module(state, path_data),
        "due_reviews": due_reviews(state, path_data, on_date),
    }


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("Expected YYYY-MM-DD") from error


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root that stores .claude/learning state")
    parser.add_argument("--path", type=Path, default=Path(__file__).resolve().parents[1] / "assets" / "path.yaml", help="Path definition file")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a new profile without overwriting existing state")
    init.add_argument("--track", required=True, choices=("Beginner", "Practitioner", "Production", "Maintainer"))
    commands.add_parser("status", help="Show deterministic progress and due reviews")
    commands.add_parser("next", help="Show the next available module")
    complete = commands.add_parser("complete", help="Record a module with evidence")
    complete.add_argument("module_id")
    complete.add_argument("--evidence", required=True)
    complete.add_argument("--date", type=_parse_date, dest="completed_on")
    due = commands.add_parser("due", help="List due spaced reviews")
    due.add_argument("--date", type=_parse_date, dest="on_date")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = _parser().parse_args(argv)
    try:
        path_data = load_path(args.path)
        if args.command == "init":
            print(json.dumps(create_profile(args.root, path_data, args.track), indent=2, sort_keys=True))
            return 0
        state = load_state(args.root, path_data)
        if args.command == "complete":
            complete_module(state, path_data, args.module_id, args.evidence, args.completed_on)
            save_state(args.root, state, path_data)
            print(json.dumps(state["modules"][args.module_id], indent=2, sort_keys=True))
            return 0
        if args.command == "next":
            print(json.dumps(next_module(state, path_data), indent=2, sort_keys=True))
            return 0
        if args.command == "due":
            print(json.dumps(due_reviews(state, path_data, args.on_date), indent=2, sort_keys=True))
            return 0
        print(json.dumps(status(state, path_data), indent=2, sort_keys=True))
        return 0
    except ProgressError as error:
        print("error: %s" % error, file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
