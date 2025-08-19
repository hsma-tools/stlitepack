import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

st.title("stlitepack Test App")

# Create a sample dataframe
np.random.seed(42)
df = pd.DataFrame({
    "x": np.arange(10),
    "y": np.random.randn(10).cumsum(),
    "category": np.random.choice(["A", "B"], size=10)
})

st.subheader("📊 DataFrame")
st.dataframe(df)

# Plotly plot
st.subheader("📈 Plotly Line Plot")
fig = px.line(df, x="x", y="y", color="category", title="Plotly Line Plot")
st.plotly_chart(fig)

# Matplotlib plot
st.subheader("📉 Matplotlib Scatter Plot")
fig, ax = plt.subplots()
for cat, group in df.groupby("category"):
    ax.scatter(group["x"], group["y"], label=cat)
ax.legend()
ax.set_title("Matplotlib Scatter Plot")
st.pyplot(fig)
