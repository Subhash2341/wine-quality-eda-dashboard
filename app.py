import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

# ---------------- 1. Page Configuration ----------------
st.set_page_config(
    page_title="Vinho Verde Wine Analysis",
    page_icon="🍷",
    layout="wide"
)

# ---------------- 2. Portable Data Loading ----------------
@st.cache_data
def load_data():
    # This finds the folder where app.py is located (Works on PC and Cloud)
    BASE_DIR = Path(__file__).parent
    
    red_path = BASE_DIR / "winequality-red.csv"
    white_path = BASE_DIR / "winequality-white.csv"

    if not red_path.exists() or not white_path.exists():
        st.error(f"❌ Missing CSV files in: {BASE_DIR}")
        st.stop()

    # Load and combine
    red = pd.read_csv(red_path, sep=";")
    red["type"] = "Red"
    white = pd.read_csv(white_path, sep=";")
    white["type"] = "White"
    
    return pd.concat([red, white], ignore_index=True)

df = load_data()

# ---------------- 3. Sidebar Filters ----------------
st.sidebar.title("📊 Filter Controls")
wine_selection = st.sidebar.multiselect("Wine Type", ["Red", "White"], default=["Red", "White"])
quality_range = st.sidebar.slider("Quality Score", int(df.quality.min()), int(df.quality.max()), (5, 8))

# Apply filtering logic
filtered_df = df[
    (df['type'].isin(wine_selection)) & 
    (df['quality'].between(quality_range[0], quality_range[1]))
]

# ---------------- 4. Header & Metrics ----------------
st.title("🍷 Vinho Verde Wine Quality Dashboard")
st.markdown(f"Currently analyzing **{len(filtered_df)}** wine samples.")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Avg Quality", f"{filtered_df['quality'].mean():.2f}")
m2.metric("Avg Alcohol", f"{filtered_df['alcohol'].mean():.1f}%")
m3.metric("Avg pH", f"{filtered_df['pH'].mean():.2f}")
m4.metric("Avg Density", f"{filtered_df['density'].mean():.4f}")

st.divider()

# ---------------- 5. The 10 Visualizations ----------------

# Row 1
col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Quality Distribution")
    fig1 = px.histogram(filtered_df, x="quality", color="type", barmode="group", text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("2. Alcohol vs. Quality")
    fig2 = px.box(filtered_df, x="quality", y="alcohol", color="type")
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col3, col4 = st.columns(2)
with col3:
    st.subheader("3. Density vs. Fixed Acidity")
    fig3 = px.scatter(filtered_df, x="fixed acidity", y="density", color="type", trendline="ols")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("4. Volatile Acidity Spread")
    fig4 = px.violin(filtered_df, y="volatile acidity", x="type", color="type", box=True)
    st.plotly_chart(fig4, use_container_width=True)

# Row 3
col5, col6 = st.columns(2)
with col5:
    st.subheader("5. pH Level Density")
    fig5, ax5 = plt.subplots()
    sns.kdeplot(data=filtered_df, x="pH", hue="type", fill=True, ax=ax5)
    st.pyplot(fig5)

with col6:
    st.subheader("6. Sulphates vs. Chlorides")
    fig6 = px.scatter(filtered_df, x="sulphates", y="chlorides", size="alcohol", color="quality")
    st.plotly_chart(fig6, use_container_width=True)

# Row 4
col7, col8 = st.columns(2)
with col7:
    st.subheader("7. Total Sulfur Dioxide per Type")
    fig7 = px.histogram(filtered_df, x="total sulfur dioxide", color="type", marginal="box")
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.subheader("8. Residual Sugar Comparison")
    fig8 = px.strip(filtered_df, x="type", y="residual sugar", color="quality")
    st.plotly_chart(fig8, use_container_width=True)

# Row 5
col9, col10 = st.columns(2)
with col9:
    st.subheader("9. Free Sulfur Dioxide Trend")
    avg_fsd = filtered_df.groupby('quality')['free sulfur dioxide'].mean().reset_index()
    fig9 = px.area(avg_fsd, x="quality", y="free sulfur dioxide")
    st.plotly_chart(fig9, use_container_width=True)

with col10:
    st.subheader("10. Correlation Heatmap")
    fig10, ax10 = plt.subplots()
    sns.heatmap(filtered_df.drop(columns=['type']).corr(), cmap="RdBu_r", center=0)
    st.pyplot(fig10)

st.divider()
# ---------------- 6. Raw Data Table ----------------
with st.expander("📂 View Raw Filtered Data"):
    st.dataframe(filtered_df)