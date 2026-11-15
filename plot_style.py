import matplotlib.pyplot as plt


def apply_style():
    plt.style.use("dark_background")
    plt.rcParams.update({
        "figure.facecolor": "#0b1020",
        "axes.facecolor": "#141a2e",
        "axes.edgecolor": "#2a3350",
        "grid.color": "#2a3350",
        "axes.grid": True,
        "lines.linewidth": 2.5,
        "font.size": 11,
    })
