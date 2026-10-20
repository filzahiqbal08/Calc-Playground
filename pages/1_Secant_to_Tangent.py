import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

BG = "#0e1117"
GREEN = "#26a69a"
RED = "#ef5350"
GOLD = "#f5c518"
TEXT = "#c9d1d9"
GRID = "#2a2f3a"

def secant_slope(a, h):
    return (f(a + h) - f(a)) / h

st.title("Secant to Tangent")
st.write("Drag h toward 0 and watch the red secant line rotate onto the dashed tangent line.")

def square(x):
    return x**2

def d_square(x):
    return 2 * x

def cube(x):
    return x**3

def d_cube(x):
    return 3 * x**2

FUNCTIONS = {
    "x²": (square, d_square),
    "x³": (cube, d_cube),
    "sin(x)": (np.sin, np.cos),
    "eˣ": (np.exp, np.exp),
}

choice = st.selectbox("Function", list(FUNCTIONS))
f, df = FUNCTIONS[choice]

a = 1.0
h = st.slider("h (distance between the two points)", 0.01, 2.0, 1.0, 0.01)

x = np.linspace(0, 3, 300)

fig, ax = plt.subplots()
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

m = secant_slope(a, h)

ax.plot(x, f(x), color=GREEN, linewidth=2.5, label=f"f(x) = {choice}")
ax.plot(x, f(a) + m * (x - a), color=RED, linewidth=1.8, label="Secant line")
ax.plot(x, f(a) + df(a) * (x - a), "--", color=GOLD, linewidth=1.5, label="Tangent line")
ax.plot([a], [f(a)], "o", color="white", label="Point 1")
ax.plot([a + h], [f(a + h)], "o", color=RED, label="Point 2")
ax.set_ylim(f(x).min() - 0.5, f(x).max() + 0.5)

ax.set_xlabel("x", color=TEXT)
ax.set_ylabel("f(x)", color=TEXT)
ax.tick_params(colors=TEXT)
ax.grid(color=GRID, linewidth=0.8)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color(GRID)

legend = ax.legend(facecolor=BG, edgecolor=GRID)
for t in legend.get_texts():
    t.set_color(TEXT)

st.pyplot(fig)

c1, c2, c3 = st.columns(3)
c1.metric("h", f"{h:.2f}")
c2.metric("Secant slope", f"{m:.4f}", delta=f"{m - df(a):.4f} from tangent", delta_color="inverse")
c3.metric("Tangent slope", f"{df(a):.2f}")