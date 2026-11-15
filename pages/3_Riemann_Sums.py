import numpy as np
import matplotlib.pyplot as plt
import streamlit as st 

from plot_style import apply_style
apply_style()

st.title("Riemann Sums")

choice = st.selectbox("Function", ["x²", "x³", "sin(x)", "eˣ", "√x"])

#Each choise sets: f(x) the curve, a and b the interval, exact the true area
if choice == "x²":
    def f(x):
        return x**2
    a, b = 0.0, 2.0
    exact = 8/3
elif choice == "x³":
    def f(x):
        return x**3 
    a, b = 0.0, 2.0
    exact = 4.0
elif choice == "sin(x)":
    def f(x):
        return np.sin(x)
    a, b = 0.0, np.pi
    exact = 2.0
elif choice == "eˣ":
    def f(x):
        return np.exp(x)
    a, b = 0.0, 1.0
    exact = np.e - 1
else:
    def f(x):
        return np.sqrt(x)
    a, b = 0.0, 4.0
    exact = 16/3

method = st.selectbox("Rectangle height uses the...", ["Left", "Right", "Midpoint"])
n = st.slider("N (number of rectangles)", 1, 100, 5, 1)

def rectangles(m):
    d = (b-a) / m       #width of each rectangle
    lefts = a + d * np.arange(m)  #left edge of each rectangle 
    if method == "Left":
        pts = lefts    #height measured at the left edge
    elif method == "Right":
        pts = lefts + d  #height measured at the right edge 
    else:
        pts = lefts - d #height measured at the middle 
    return lefts, pts, d

def riemann(m):
    lefts, pts, d = rectangles(m)
    return np.sum(f(pts)) * d  #add up (height * width)

lefts, pts, dx = rectangles(n)
heights = f(pts)
estimate = riemann(n)
error = estimate - exact

x = np.linspace(a, b, 400)
col_a, col_b = st.columns(2)

#--------------------------------------------------
# left graph: the curve with the rectangles
with col_a:
    fig1, ax1 = plt.subplots()
    ax1.plot(x, f(x), label=f"f(x) = {choice}")
    ax1.bar(lefts, heights, width=dx, align="edge", alpha=0.4,
            edgecolor="black", label=f"{n} rectangles")
    ax1.set_ylim(0, max(f(x).max(), heights.max()) * 1.05)
    ax1.set_xlabel("x")
    ax1.legend()
    st.pyplot(fig1)

# right graph: the estimate for every n from 1 to 100
with col_b:
    ns = np.arange(1, 101)
    estimates = [riemann(m) for m in ns]
    fig2, ax2 = plt.subplots()
    ax2.plot(ns, estimates, label=f"{method} sum")
    ax2.plot([n], [estimate], "o")
    ax2.axhline(exact, linestyle="--", color="gray", label=f"exact = {exact:.4f}")
    ax2.set_xlabel("n (number of rectangles)")
    ax2.set_ylabel("estimated area")
    ax2.legend()
    st.pyplot(fig2)

c1, c2, c3 = st.columns(3)
c1.metric("Estimate", f"{estimate:.4f}")
c2.metric("Exact area", f"{exact:.4f}")
c3.metric("Error (estimate − exact)", f"{error:.4f}")