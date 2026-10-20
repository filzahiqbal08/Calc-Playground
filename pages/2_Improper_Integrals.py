import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Improper Integrals")

choice = st.selectbox("Function", ["1/xᵖ", "e^(-k·x)", "x·e^(−x)", "1/(1+x²)"])

# Each choice sets up 3 things:
#   f(x)     the curve
#   area(b)  the integral of f from 1 to b (derived by hand)
#   limit    what the area approaches as b -> infinity (None = no limit)

if choice == "1/xᵖ":
    p = st.slider("p (the exponent)", 0.2, 3.0, 2.0, 0.1)
    p = round(p, 1)

    def f(x):
        return 1 / x**p

    def area(b):
        if p == 1:
            return np.log(b)
        return (1 - b**(1 - p)) / (p - 1)

    limit = 1 / (p - 1) if p > 1 else None
    label = f"1/x^{p:g}"

elif choice == "e^(-k·x)":
    k = st.slider("k (how fast it decays)", 0.1, 3.0, 1.0, 0.1)
    k = round(k, 1)

    def f(x):
        return np.exp(-k * x)

    def area(b):
        return (np.exp(-k) - np.exp(-k * b)) / k

    limit = np.exp(-k) / k
    label = f"e^(-{k:g}x)"

elif choice == "x·e^(−x)":
    def f(x):
        return x * np.exp(-x)

    def area(b):
        return 2 * np.exp(-1) - (b + 1) * np.exp(-b)

    limit = 2 * np.exp(-1)
    label = "x·e^(-x)"

else:
    def f(x):
        return 1 / (1 + x**2)

    def area(b):
        return np.arctan(b) - np.pi / 4

    limit = np.pi / 4
    label = "1/(1+x²)"

b = st.slider("b (how far right the area goes)", 1.5, 50.0, 5.0, 0.5)

x = np.linspace(1, 50, 500)      # the whole curve
xs = np.linspace(1, b, 200)      # just the part from 1 to b

left, right = st.columns(2)

# left graph: the curve with the area from 1 to b shaded
with left:
    fig1, ax1 = plt.subplots()
    ax1.plot(x, f(x), label=f"f(x) = {label}")
    ax1.fill_between(xs, f(xs), alpha=0.4, label="area from 1 to b")
    ax1.set_ylim(0, f(x).max() * 1.05)
    ax1.set_xlabel("x")
    ax1.legend()
    st.pyplot(fig1)

# right graph: the area as b grows (this is the limit happening)
with right:
    bs = np.linspace(1, 50, 500)
    fig2, ax2 = plt.subplots()
    ax2.plot(bs, area(bs))
    ax2.plot([b], [area(b)], "o")
    if limit is not None:
        ax2.axhline(limit, linestyle="--", color="gray", label=f"limit = {limit:.4f}")
        ax2.legend()
    ax2.set_xlabel("b")
    ax2.set_ylabel("area from 1 to b")
    st.pyplot(fig2)

st.write(f"Area from 1 to {b:g} = {area(b):.4f}")
if limit is not None:
    st.write(f"As b → ∞ the area → {limit:.4f}. It converges.")
else:
    st.write("As b → ∞ the area grows without bound. It diverges.")