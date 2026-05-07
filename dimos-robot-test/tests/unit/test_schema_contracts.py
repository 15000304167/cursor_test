from __future__ import annotations

import pytest
from pydantic import ValidationError

from dimos_testkit.skills.contracts import MoveSkillArgs


@pytest.mark.unit
def test_move_skill_args_valid() -> None:
    m = MoveSkillArgs.model_validate({"x": 0.1, "duration": 1.0})
    assert m.x == 0.1
    assert m.duration == 1.0


@pytest.mark.unit
def test_move_skill_args_rejects_bad_types() -> None:
    with pytest.raises(ValidationError):
        MoveSkillArgs.model_validate({"x": "nope"})
