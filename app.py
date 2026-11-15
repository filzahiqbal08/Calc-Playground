import streamlit as st

st.set_page_config(page_title="Calc Playground", page_icon="📐")

st.markdown(
    """
    <h1 style="font-size:3.2rem; margin-bottom:0;
    background: linear-gradient(90deg, #2dd4bf, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
    Calc Playground</h1>
    """,
    unsafe_allow_html=True,
)
st.markdown("#### *Math you can see, not just memorize.*")
st.write("Interactive calculus visualizations, made by a student, for students.")
st.divider()

st.subheader("What's inside")
st.markdown(
    """
- **Secant to Tangent:** shrink h and watch the secant line turn into the tangent line.
- **Improper Integrals:** push the upper limit toward infinity and see whether the area settles.
- **Riemann Sums:** left, right, and midpoint rectangles, and how the error shrinks as n grows.
- **Continuity:** approach a point from both sides and test the three conditions.
"""
)
st.caption("Pick a page from the sidebar.")
