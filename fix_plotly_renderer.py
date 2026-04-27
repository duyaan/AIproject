import json
from pathlib import Path


NOTEBOOK_PATH = Path(r"c:\Ai_H\AIproject\world_cup_2026_sim.ipynb")


with NOTEBOOK_PATH.open("r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    source = "".join(cell.get("source", []))
    if "def plot_interactive_knockout_bracket(simulation: Dict[str, object]) -> None:" in source:
        if "from IPython.display import HTML, display" not in source:
            source = source.replace(
                "def plot_interactive_knockout_bracket(simulation: Dict[str, object]) -> None:\n    import plotly.graph_objects as go\n",
                "def plot_interactive_knockout_bracket(simulation: Dict[str, object]) -> None:\n    import plotly.graph_objects as go\n    from IPython.display import HTML, display\n",
            )
        source = source.replace(
            "    fig.show()\n",
            "    display(HTML(fig.to_html(include_plotlyjs='cdn', full_html=False)))\n",
        )
        cell["source"] = [line + '\n' for line in source.splitlines()]
        break

with NOTEBOOK_PATH.open("w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
    f.write("\n")
