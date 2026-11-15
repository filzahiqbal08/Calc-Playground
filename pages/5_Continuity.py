import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from plot_style import apply_style
apply_style()

st.title("Continuity and Discontinuity")

names = [
    "Continuous: x^2",
    "Hole: (x^2-1)/(x-1)",
    "Wrong value: x^2 but f(1) = 3",
    "Jump: x, then x+1",
    "Infinite: 1/(x-1)",
    "Oscillating: sin(1/x)",
]
choice = st.selectbox("Example", names)
case = names.index(choice)

# Each example sets:
#   f(x)                     the function
#   a                        the point we are testing
#   xmin, xmax, ymin, ymax   the graph window
#   left_lim, right_lim      the true one-sided limits at a (None = no finite limit)
#   left_text, right_text    those limits in words
#   kind                     the type of discontinuity (if any)
if case == 0:
    def f(x):
        return x**2
    a = 1.0
    xmin, xmax, ymin, ymax = 0.0, 2.0, -0.5, 4.5
    left_lim, right_lim = 1.0, 1.0
    left_text, right_text = "1", "1"
    kind = "none"
elif case == 1:
    def f(x):
        return (x**2 - 1) / (x - 1)
    a = 1.0
    xmin, xmax, ymin, ymax = 0.0, 2.0, 0.0, 3.5
    left_lim, right_lim = 2.0, 2.0
    left_text, right_text = "2", "2"
    kind = "removable discontinuity (a hole)"
elif case == 2:
    def f(x):
        return np.where(x == 1, 3.0, x**2)
    a = 1.0
    xmin, xmax, ymin, ymax = 0.0, 2.0, -0.5, 4.5
    left_lim, right_lim = 1.0, 1.0
    left_text, right_text = "1", "1"
    kind = "removable discontinuity (the limit is 1 but f(1) = 3)"
elif case == 3:
    def f(x):
        return np.where(x < 1, x, x + 1)
    a = 1.0
    xmin, xmax, ymin, ymax = 0.0, 2.0, 0.0, 3.5
    left_lim, right_lim = 1.0, 2.0
    left_text, right_text = "1", "2"
    kind = "jump discontinuity"
elif case == 4:
    def f(x):
        return 1 / (x - 1)
    a = 1.0
    xmin, xmax, ymin, ymax = 0.0, 2.0, -10.0, 10.0
    left_lim, right_lim = None, None
    left_text, right_text = "-infinity", "+infinity"
    kind = "infinite discontinuity (vertical asymptote)"
else:
    def f(x):
        return np.sin(1 / x)
    a = 0.0
    xmin, xmax, ymin, ymax = -0.5, 0.5, -1.5, 1.5
    left_lim, right_lim = None, None
    left_text = right_text = "does not exist (oscillates)"
    kind = "oscillating discontinuity"

h = st.slider("h (distance from a)", 0.01, 0.5, 0.4, 0.01)
st.caption("Drag h toward 0. Do the left and right numbers settle on the same value?")


def at(x0):
    with np.errstate(all="ignore"):
        return f(np.array([x0], dtype=float))[0]


def show(v):
    return f"{v:.4f}" if np.isfinite(v) else "undefined"


fa = at(a)
y_left = at(a - h)
y_right = at(a + h)

defined = bool(np.isfinite(fa))
limit_exists = (left_lim is not None and right_lim is not None
                and abs(left_lim - right_lim) < 1e-9)
matches = limit_exists and defined and abs(fa - left_lim) < 1e-9

x = np.linspace(xmin, xmax, 10000)
xl = x[x < a]          # points left of a
xr = x[x > a]          # points right of a

fig, ax = plt.subplots()
ax.plot(xl, f(xl), color="tab:blue", label=choice)
ax.plot(xr, f(xr), color="tab:blue")
ax.axvline(a, linestyle=":", color="gray")

# filled dot where f(a) exists; open circles where the curve "wants" to be
if defined:
    ax.plot([a], [fa], "o", color="tab:blue")
for lim in (left_lim, right_lim):
    if lim is not None and not (defined and abs(lim - fa) < 1e-9):
        ax.plot([a], [lim], "o", markerfacecolor="white", markeredgecolor="tab:blue")

ax.plot([a - h], [y_left], "o", color="tab:green", label="x = a - h (from the left)")
ax.plot([a + h], [y_right], "o", color="tab:orange", label="x = a + h (from the right)")
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_xlabel("x")
ax.legend()
st.pyplot(fig)

c1, c2, c3 = st.columns(3)
c1.metric("f(a - h), from the left", show(y_left))
c2.metric("f(a + h), from the right", show(y_right))
c3.metric("f(a)", show(fa))

st.write(f"Left-hand limit: {left_text}  |  Right-hand limit: {right_text}")
st.write("**The three conditions at x = a**")
st.write(f"1. f(a) is defined: {'Yes' if defined else 'No'}")
st.write(f"2. The limit exists (left = right): {'Yes' if limit_exists else 'No'}")
st.write(f"3. The limit equals f(a): {'Yes' if matches else 'No'}")

if matches:
    st.success("Continuous at x = a.")
else:
    st.error(f"Not continuous at x = a: {kind}.")