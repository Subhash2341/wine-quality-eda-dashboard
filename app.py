import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ---------------- Page Config ----------------
st.set_page_config(page_title="Pro Wine Analytics", page_icon="🍷", layout="wide")

# ---------------- Data Loading (Your Paths) ----------------
BASE_DIR = Path(r"C:\Users\SUBHASH\Wine_Quality_Project")
RED_WINE_PATH = BASE_DIR / "winequality-red.csv"
WHITE_WINE_PATH = BASE_DIR / "winequality-white.csv"

@st.cache_data
def load_data():
    red = pd.read_csv(RED_WINE_PATH, sep=";")
    red["type"] = "Red"
    white = pd.read_csv(WHITE_WINE_PATH, sep=";")
    white["type"] = "White"
    return pd.concat([red, white], ignore_index=True)

df = load_data()

# ---------------- Sidebar Filters ----------------
st.sidebar.header("📊 Dashboard Filters")
wine_type = st.sidebar.multiselect("Select Wine Type", ["Red", "White"], default=["Red", "White"])
quality_filter = st.sidebar.slider("Quality Range", int(df.quality.min()), int(df.quality.max()), (5, 8))

# Apply Filters
mask = (df['type'].isin(wine_type)) & (df['quality'].between(quality_filter[0], quality_filter[1]))
filtered_df = df[mask]

st.title("🍷 Advanced Wine Quality EDA")
st.markdown(f"Displaying analysis for **{len(filtered_df)}** samples.")

# ---------------- Visualizations (The Top 10) ----------------

# 1. Quality Score Distribution (Histogram)
st.subheader("1. Distribution of Wine Quality")
fig1 = px.histogram(filtered_df, x="quality", color="type", barmode="group", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # 2. Alcohol vs Quality (Box Plot)
    st.subheader("2. Alcohol Impact on Quality")
    fig2 = px.box(filtered_df, x="quality", y="alcohol", color="type")
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Fixed Acidity vs Density (Scatter Plot)
    st.subheader("3. Density vs. Fixed Acidity")
    fig3 = px.scatter(filtered_df, x="fixed acidity", y="density", color="type", trendline="ols")
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Volatile Acidity Distribution (Violin Plot)
    st.subheader("4. Volatile Acidity Spread")
    fig4 = px.violin(filtered_df, y="volatile acidity", x="type", color="type", box=True)
    st.plotly_chart(fig4, use_container_width=True)

    # 5. pH Levels (KDE/Density Plot)
    st.subheader("5. pH Level Distribution")
    fig5, ax5 = plt.subplots()
    sns.kdeplot(data=filtered_df, x="pH", hue="type", fill=True, ax=ax5)
    st.pyplot(fig5)

with col2:
    # 6. Sulphates vs Chlorides (Scatter)
    st.subheader("6. Sulphates vs. Chlorides")
    fig6 = px.scatter(filtered_df, x="sulphates", y="chlorides", size="alcohol", color="quality")
    st.plotly_chart(fig6, use_container_width=True)

    # 7. Total Sulfur Dioxide (Histogram)
    st.subheader("7. Total Sulfur Dioxide Analysis")
    fig7 = px.histogram(filtered_df, x="total sulfur dioxide", color="type", marginal="box")
    st.plotly_chart(fig7, use_container_width=True)

    # 8. Residual Sugar vs Type (Strip Plot)
    st.subheader("8. Residual Sugar Levels")
    fig8 = px.strip(filtered_df, x="type", y="residual sugar", color="quality")
    st.plotly_chart(fig8, use_container_width=True)

    # 9. Free Sulfur Dioxide (Area Chart)
    st.subheader("9. Free Sulfur Dioxide Trends")
    avg_free_sulfur = filtered_df.groupby('quality')['free sulfur dioxide'].mean().reset_index()
    fig9 = px.area(avg_free_sulfur, x="quality", y="free sulfur dioxide")
    st.plotly_chart(fig9, use_container_width=True)

# 10. Correlation Heatmap (Full Width)
st.subheader("10. Global Feature Correlation Heatmap")
fig10, ax10 = plt.subplots(figsize=(12, 8))
sns.heatmap(filtered_df.drop(columns=['type']).corr(), annot=True, cmap="coolwarm", fmt=".2f")
st.pyplot(fig10)

st.divider()
st.dataframe(filtered_df.head(100))