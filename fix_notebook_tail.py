import json
from pathlib import Path


NOTEBOOK_PATH = Path(r"c:\Ai_H\AIproject\world_cup_2026_sim.ipynb")


def to_source(text: str) -> list[str]:
    return [line + "\n" for line in text.splitlines()]


with NOTEBOOK_PATH.open("r", encoding="utf-8") as f:
    nb = json.load(f)

cells = nb["cells"]

cells[69]["source"] = to_source(
    """## Run The Pipeline

Run these cells in order.
The first run cell loads the datasets, prepares the features, builds the team context table, and loads or trains the best model.
The second run cell simulates the tournament, including the knockout phase after the group stage using the selected model.
The third run cell repeats the tournament to estimate title odds."""
)

cells[70]["source"] = to_source(
    """### Suggested Execution Order

1. Run the setup cell to load data and prepare the model.
2. Run the tournament simulation cell to create `simulation`.
3. Run the title-odds cell if you want repeated tournament estimates.
4. Run the bracket video cell at the end to visualize the model-driven knockout phase."""
)

cells[71]["source"] = to_source(
    """results, elo = load_data()
fifa_ranking, world_cup_matches, world_cup_summary = load_external_data()

latest_elo = get_latest_elo(elo)
latest_form = get_latest_team_form(results)
fifa_profile = build_fifa_team_profile(fifa_ranking)
world_cup_profile = build_world_cup_team_profile(world_cup_matches, world_cup_summary)

team_ratings = ensure_team_ratings(latest_elo)
team_form = ensure_team_form(latest_form)
team_context_table = build_team_context(team_ratings, team_form, fifa_profile, world_cup_profile)
team_context = make_team_context_lookup(team_context_table)

training_df = prepare_training_data(results, elo)
model, metrics, comparison = get_or_train_best_model(training_df)

print(f"Model cache status: {metrics['cache_status']}")
print(f"Selected model: {metrics['model_name']}")
comparison"""
)
cells[71]["execution_count"] = None
cells[71]["outputs"] = []

cells[72]["source"] = to_source(
    """simulation = simulate_tournament(model, team_ratings, team_form, team_context, SEED)
print_tournament_report(simulation, metrics, latest_elo["date"].max(), team_context_table)"""
)
cells[72]["execution_count"] = None
cells[72]["outputs"] = []

cells[73]["source"] = to_source(
    """title_table = monte_carlo_champions(model, team_ratings, team_form, team_context, SIMULATION_RUNS)
title_table.head(15)"""
)
cells[73]["execution_count"] = None
cells[73]["outputs"] = []

cells[74]["source"] = to_source(
    """## Space Bracket Video

This section visualizes the knockout phase that comes out of the model-driven tournament simulation.
Run it after the `simulation = simulate_tournament(...)` cell so the bracket uses the actual knockout matches produced after the group stage.

The sample data is kept only as a backup demo, but the final run cell below is set up to use the real `simulation` first."""
)

cells[75]["source"] = to_source(
    """SAMPLE_SPACE_BRACKET = {
    "round_of_16": [
        {"team_a": "Brazil", "team_b": "Mexico", "score_a": 3, "score_b": 1, "winner": "Brazil"},
        {"team_a": "France", "team_b": "Senegal", "score_a": 2, "score_b": 0, "winner": "France"},
        {"team_a": "Argentina", "team_b": "Japan", "score_a": 2, "score_b": 1, "winner": "Argentina"},
        {"team_a": "Spain", "team_b": "Germany", "score_a": 1, "score_b": 0, "winner": "Spain"},
        {"team_a": "Portugal", "team_b": "Uruguay", "score_a": 2, "score_b": 1, "winner": "Portugal"},
        {"team_a": "England", "team_b": "Netherlands", "score_a": 1, "score_b": 2, "winner": "Netherlands"},
        {"team_a": "Croatia", "team_b": "Belgium", "score_a": 1, "score_b": 1, "winner": "Croatia"},
        {"team_a": "Morocco", "team_b": "Colombia", "score_a": 2, "score_b": 0, "winner": "Morocco"},
    ],
    "quarterfinals": [
        {"team_a": "Brazil", "team_b": "France", "score_a": 2, "score_b": 1, "winner": "Brazil"},
        {"team_a": "Argentina", "team_b": "Spain", "score_a": 1, "score_b": 2, "winner": "Spain"},
        {"team_a": "Portugal", "team_b": "Netherlands", "score_a": 2, "score_b": 3, "winner": "Netherlands"},
        {"team_a": "Croatia", "team_b": "Morocco", "score_a": 0, "score_b": 1, "winner": "Morocco"},
    ],
    "semifinals": [
        {"team_a": "Brazil", "team_b": "Spain", "score_a": 2, "score_b": 3, "winner": "Spain"},
        {"team_a": "Netherlands", "team_b": "Morocco", "score_a": 1, "score_b": 2, "winner": "Morocco"},
    ],
    "final": [
        {"team_a": "Spain", "team_b": "Morocco", "score_a": 2, "score_b": 1, "winner": "Spain"},
    ],
}"""
)
cells[75]["execution_count"] = None
cells[75]["outputs"] = []

cells[78]["execution_count"] = None
cells[78]["outputs"] = []

cells[79]["source"] = to_source(
    """if "simulation" not in globals():
    raise RuntimeError("Run the tournament simulation cell first so the bracket uses the model outcome after the group stage.")

space_bracket_data = simulation_to_bracket_data(simulation)
render_space_bracket_video(
    space_bracket_data,
    title=f"2026 World Cup Knockout Mission | Champion: {simulation['champion']}",
    interval=1300,
)"""
)
cells[79]["execution_count"] = None
cells[79]["outputs"] = []

with NOTEBOOK_PATH.open("w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
