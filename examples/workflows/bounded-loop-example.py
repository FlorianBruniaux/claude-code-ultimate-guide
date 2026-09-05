#!/usr/bin/env python3
"""Runnable bounded-loop example with no model or network dependency."""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Evidence:
    attempt: int
    artifact: str
    accepted: bool
    reason: str


@dataclass(frozen=True)
class RunResult:
    status: str
    evidence: tuple[Evidence, ...]


Action = Callable[[str, int], str]
Verifier = Callable[[str], tuple[bool, str]]


def run_bounded_loop(
    goal: str,
    action: Action,
    verify: Verifier,
    *,
    max_attempts: int,
) -> RunResult:
    """Repeat action and a separate verifier call until accepted or exhausted."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    history: list[Evidence] = []
    for attempt in range(1, max_attempts + 1):
        artifact = action(goal, attempt)
        accepted, reason = verify(artifact)
        history.append(Evidence(attempt, artifact, accepted, reason))
        if accepted:
            return RunResult("accepted", tuple(history))

    return RunResult("escalated", tuple(history))


def _example_action(goal: str, attempt: int) -> str:
    return f"{goal}:candidate-{attempt}"


def _example_verifier(artifact: str) -> tuple[bool, str]:
    accepted = artifact.endswith("candidate-2")
    reason = "required check passed" if accepted else "required check failed"
    return accepted, reason


def _self_check() -> None:
    result = run_bounded_loop(
        "repair-build",
        _example_action,
        _example_verifier,
        max_attempts=3,
    )
    assert result.status == "accepted"
    assert len(result.evidence) == 2
    assert result.evidence[0].accepted is False
    assert result.evidence[1].accepted is True

    exhausted = run_bounded_loop(
        "impossible",
        _example_action,
        lambda _: (False, "still failing"),
        max_attempts=2,
    )
    assert exhausted.status == "escalated"
    assert len(exhausted.evidence) == 2


if __name__ == "__main__":
    _self_check()
    result = run_bounded_loop(
        "repair-build",
        _example_action,
        _example_verifier,
        max_attempts=3,
    )
    print(f"{result.status} after {len(result.evidence)} attempts")
