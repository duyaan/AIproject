from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROUND_LABELS = {
    "round_of_32": "Round of 32",
    "round_of_16": "Round of 16",
    "quarterfinals": "Quarter-finals",
    "semifinals": "Semi-finals",
    "final": "Final",
}

ROUND_ORDER = ["round_of_32", "round_of_16", "quarterfinals", "semifinals", "final"]


@dataclass(frozen=True)
class MatchCard:
    team_a: str
    team_b: str
    score_a: int
    score_b: int
    winner: str


SAMPLE_BRACKET = {
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
}


def _to_match_cards(matches: Iterable[dict]) -> list[MatchCard]:
    cards: list[MatchCard] = []
    for match in matches:
        winner = match.get("winner")
        if winner is None:
            winner = match["team_a"] if match["score_a"] >= match["score_b"] else match["team_b"]
        cards.append(
            MatchCard(
                team_a=match["team_a"],
                team_b=match["team_b"],
                score_a=int(match["score_a"]),
                score_b=int(match["score_b"]),
                winner=str(winner),
            )
        )
    return cards


def _active_rounds(bracket_data: dict[str, Sequence[dict]]) -> list[str]:
    return [round_name for round_name in ROUND_ORDER if round_name in bracket_data and bracket_data[round_name]]


def _side_y_positions(match_count: int) -> list[float]:
    top, bottom = 0.12, 0.84
    if match_count == 1:
        return [0.48]
    gap = (bottom - top) / (match_count - 1)
    return [top + gap * idx for idx in range(match_count)]


def _advance_positions(previous_positions: Sequence[float]) -> list[float]:
    return [(previous_positions[idx] + previous_positions[idx + 1]) / 2 for idx in range(0, len(previous_positions), 2)]


def _draw_card(
    ax: plt.Axes,
    x: float,
    y: float,
    card: MatchCard,
    width: float,
    height: float,
    theme: dict[str, str],
) -> None:
    left = x - width / 2
    bottom = y - height / 2

    shell = FancyBboxPatch(
        (left, bottom),
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=1.6,
        edgecolor=theme["card_edge"],
        facecolor=theme["card_fill"],
        zorder=3,
    )
    ax.add_patch(shell)

    divider_y = bottom + height / 2
    ax.plot([left + 0.01, left + width - 0.01], [divider_y, divider_y], color=theme["divider"], lw=1.0, zorder=4)

    winner_is_a = card.winner == card.team_a
    top_fill = theme["winner_fill"] if winner_is_a else theme["loser_fill"]
    bottom_fill = theme["winner_fill"] if not winner_is_a else theme["loser_fill"]

    top_row = FancyBboxPatch(
        (left + 0.006, divider_y),
        width - 0.012,
        height / 2 - 0.008,
        boxstyle="round,pad=0.008,rounding_size=0.014",
        linewidth=0,
        facecolor=top_fill,
        zorder=3.5,
    )
    bottom_row = FancyBboxPatch(
        (left + 0.006, bottom + 0.006),
        width - 0.012,
        height / 2 - 0.012,
        boxstyle="round,pad=0.008,rounding_size=0.014",
        linewidth=0,
        facecolor=bottom_fill,
        zorder=3.5,
    )
    ax.add_patch(top_row)
    ax.add_patch(bottom_row)

    ax.text(left + 0.015, bottom + height * 0.74, card.team_a, ha="left", va="center", fontsize=10.5, color=theme["text"], weight="bold" if winner_is_a else "normal", zorder=5)
    ax.text(left + width - 0.018, bottom + height * 0.74, str(card.score_a), ha="right", va="center", fontsize=11, color=theme["text"], weight="bold" if winner_is_a else "normal", zorder=5)
    ax.text(left + 0.015, bottom + height * 0.24, card.team_b, ha="left", va="center", fontsize=10.5, color=theme["text"], weight="bold" if not winner_is_a else "normal", zorder=5)
    ax.text(left + width - 0.018, bottom + height * 0.24, str(card.score_b), ha="right", va="center", fontsize=11, color=theme["text"], weight="bold" if not winner_is_a else "normal", zorder=5)


def _connect_cards(ax: plt.Axes, start_x: float, start_y: float, end_x: float, end_y: float, theme: dict[str, str]) -> None:
    elbow_x = start_x + (end_x - start_x) * 0.55
    ax.plot([start_x, elbow_x], [start_y, start_y], color=theme["connector"], lw=2.0, zorder=2)
    ax.plot([elbow_x, elbow_x], [start_y, end_y], color=theme["connector"], lw=2.0, zorder=2)
    ax.plot([elbow_x, end_x], [end_y, end_y], color=theme["connector"], lw=2.0, zorder=2)


def _draw_side(
    ax: plt.Axes,
    rounds: list[str],
    side_cards: dict[str, list[MatchCard]],
    x_positions: dict[str, float],
    card_width: float,
    card_height: float,
    theme: dict[str, str],
    direction: str,
) -> dict[str, list[float]]:
    y_positions: dict[str, list[float]] = {}
    y_positions[rounds[0]] = _side_y_positions(len(side_cards[rounds[0]]))
    for previous_round, next_round in zip(rounds, rounds[1:]):
        y_positions[next_round] = _advance_positions(y_positions[previous_round])

    for round_name in rounds:
        x = x_positions[round_name]
        for card, y in zip(side_cards[round_name], y_positions[round_name]):
            _draw_card(ax, x, y, card, card_width, card_height, theme)

    for previous_round, next_round in zip(rounds, rounds[1:]):
        source_x = x_positions[previous_round] + card_width / 2 if direction == "left" else x_positions[previous_round] - card_width / 2
        target_x = x_positions[next_round] - card_width / 2 if direction == "left" else x_positions[next_round] + card_width / 2
        for index, y in enumerate(y_positions[previous_round]):
            _connect_cards(ax, source_x, y, target_x, y_positions[next_round][index // 2], theme)

    return y_positions


def plot_world_cup_bracket(
    bracket_data: dict[str, Sequence[dict]],
    output_png: str | Path = "world_cup_bracket.png",
) -> Path:
    rounds = _active_rounds(bracket_data)
    if len(rounds) < 2 or rounds[-1] != "final":
        raise ValueError("Bracket data must include at least two rounds and end with 'final'.")

    cards = {round_name: _to_match_cards(bracket_data[round_name]) for round_name in rounds}
    initial_matches = len(cards[rounds[0]])
    if initial_matches % 2 != 0:
        raise ValueError("The first round must contain an even number of matches.")

    left_cards = {}
    right_cards = {}
    for round_name in rounds[:-1]:
        half = len(cards[round_name]) // 2
        left_cards[round_name] = cards[round_name][:half]
        right_cards[round_name] = cards[round_name][half:]

    final_card = cards["final"][0]
    side_rounds = rounds[:-1]

    theme = {
        "figure_bg": "#0b1220",
        "axes_bg": "#0f172a",
        "card_fill": "#111c30",
        "card_edge": "#334155",
        "winner_fill": "#163c68",
        "loser_fill": "#142032",
        "divider": "#475569",
        "connector": "#22d3ee",
        "text": "#e2e8f0",
        "title": "#f8fafc",
        "subtitle": "#94a3b8",
        "champion_fill": "#2a1a4a",
        "champion_edge": "#c084fc",
        "champion_text": "#f5d0fe",
    }

    card_width = 0.16
    card_height = 0.11
    champion_width = 0.16
    champion_height = 0.12

    fig, ax = plt.subplots(figsize=(18, 10.5), facecolor=theme["figure_bg"])
    ax.set_facecolor(theme["axes_bg"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    left_x_positions = {}
    right_x_positions = {}
    left_start = 0.10
    right_start = 0.90
    left_step = 0.15
    right_step = 0.15
    for idx, round_name in enumerate(side_rounds):
        left_x_positions[round_name] = left_start + idx * left_step
        right_x_positions[round_name] = right_start - idx * right_step

    final_x = 0.50
    champion_x = 0.50
    final_y = 0.48
    champion_y = 0.16

    left_y_positions = _draw_side(ax, side_rounds, left_cards, left_x_positions, card_width, card_height, theme, "left")
    right_y_positions = _draw_side(ax, side_rounds, right_cards, right_x_positions, card_width, card_height, theme, "right")

    _draw_card(ax, final_x, final_y, final_card, card_width, card_height, theme)

    left_source_x = left_x_positions[side_rounds[-1]] + card_width / 2
    right_source_x = right_x_positions[side_rounds[-1]] - card_width / 2
    _connect_cards(ax, left_source_x, left_y_positions[side_rounds[-1]][0], final_x - card_width / 2, final_y, theme)
    _connect_cards(ax, right_source_x, right_y_positions[side_rounds[-1]][0], final_x + card_width / 2, final_y, theme)

    champion_box = FancyBboxPatch(
        (champion_x - champion_width / 2, champion_y - champion_height / 2),
        champion_width,
        champion_height,
        boxstyle="round,pad=0.015,rounding_size=0.02",
        linewidth=2.0,
        edgecolor=theme["champion_edge"],
        facecolor=theme["champion_fill"],
        zorder=3,
    )
    ax.add_patch(champion_box)
    ax.text(champion_x, champion_y + 0.02, final_card.winner, ha="center", va="center", fontsize=18, color=theme["champion_text"], weight="bold", zorder=5)
    ax.text(champion_x, champion_y - 0.02, "World Champion", ha="center", va="center", fontsize=10.5, color=theme["subtitle"], zorder=5)

    ax.plot([final_x, champion_x], [final_y - card_height / 2, champion_y + champion_height / 2], color=theme["champion_edge"], lw=2.2, zorder=2)

    title_y = 0.965
    for round_name, x in left_x_positions.items():
        ax.text(x, title_y, ROUND_LABELS[round_name], ha="center", va="center", fontsize=13, color=theme["subtitle"], weight="bold")
    ax.text(final_x, title_y, "Final", ha="center", va="center", fontsize=14, color=theme["title"], weight="bold")
    ax.text(champion_x, 0.07, "Champion", ha="center", va="center", fontsize=14, color=theme["title"], weight="bold")
    for round_name, x in reversed(list(right_x_positions.items())):
        ax.text(x, title_y, ROUND_LABELS[round_name], ha="center", va="center", fontsize=13, color=theme["subtitle"], weight="bold")

    ax.text(0.02, 0.985, "FIFA WORLD CUP KNOCKOUT BRACKET", ha="left", va="top", fontsize=20, color=theme["title"], weight="bold")
    ax.text(0.02, 0.955, "Dark-themed presentation bracket with editable sample data", ha="left", va="top", fontsize=11.5, color=theme["subtitle"])

    output_path = Path(output_png)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path


def main() -> None:
    output_path = Path(__file__).with_name("world_cup_bracket_sample.png")
    saved_path = plot_world_cup_bracket(SAMPLE_BRACKET, output_png=output_path)
    print(f"Saved bracket PNG to {saved_path}")


if __name__ == "__main__":
    main()
