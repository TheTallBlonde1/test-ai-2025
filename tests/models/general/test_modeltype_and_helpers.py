import json
from pathlib import Path

import pytest

from aiss.models.games import (
    ActionAdventureGameInfo,
    HorrorSurvivalGameInfo,
    MmoOnlineGameInfo,
    PuzzleStrategyGameInfo,
    RolePlayingGameInfo,
    ShooterGameInfo,
    SimulationSandboxGameInfo,
    SportsRacingGameInfo,
)
from aiss.models.games._base import StudioProfile
from aiss.models.shared import ModelType, compose_instructions


@pytest.mark.parametrize(
    "model_type, expected_cls",
    [
        (ModelType.ACTION_ADVENTURE_GAME, ActionAdventureGameInfo),
        (ModelType.SHOOTER_GAME, ShooterGameInfo),
        (ModelType.PUZZLE_STRATEGY_GAME, PuzzleStrategyGameInfo),
        (ModelType.ROLE_PLAYING_GAME, RolePlayingGameInfo),
        (ModelType.SIMULATION_SANDBOX_GAME, SimulationSandboxGameInfo),
        (ModelType.SPORTS_RACING_GAME, SportsRacingGameInfo),
        (ModelType.HORROR_SURVIVAL_GAME, HorrorSurvivalGameInfo),
        (ModelType.MMO_ONLINE_GAME, MmoOnlineGameInfo),
    ],
)
def test_modeltype_registry_maps_to_games(model_type, expected_cls):
    assert model_type.get_model_from_name() is expected_cls
    registry = ModelType.registry()
    assert registry[model_type.value] is expected_cls


def test_compose_instructions_appends_additional_context():
    base = "Do the base task."
    combined = compose_instructions(base, ["Add more data", "Highlight retention"])
    assert "Additional context" in combined
    assert "- Add more data" in combined
    assert combined.strip().endswith("- Highlight retention")


def test_game_json_model_roundtrip(tmp_path: Path):
    profile = StudioProfile(
        name="Fixture Forge",
        role="Lead Developer",
        headquarters="Seattle",
        team_size=120,
        notable_credits=["Test Quest"],
        technology_stack=["PyEngine"],
    )
    json_path = tmp_path / "studio.json"
    profile.to_json(json_path)
    loaded = StudioProfile.from_json(json_path)
    assert loaded.model_dump() == profile.model_dump()
    raw = json_path.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["name"] == "Fixture Forge"
    assert data["role"] == "Lead Developer"
