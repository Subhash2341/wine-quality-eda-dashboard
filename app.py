import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

# ---------------- 1. Page Configuration ----------------
st.set_page_config(
    page_title="Wine Quality Analysis",
    page_icon="🍷",
    layout="wide"
)

# ---------------- 2. Portable Data Loading ----------------
@st.cache_data
def load_data():
    # Relative path logic: automatically detects the directory of app.py
    BASE_DIR = Path(__file__).parent
    
    red_file = "winequality-red.csv"
    white_file = "winequality-white.csv"
    
    red_path = BASE_DIR / red_file
    white_path = BASE_DIR / white_file

    if not red_path.exists() or not white_path.exists():
        st.error("❌ Data files not found. Ensure CSVs are in the root directory of your repository.")
        st.stop()

    # Loading datasets with semicolon separator
    red = pd.read_csv(red_path, sep=";")
    red["type"] = "Red"
    
    white = pd.read_csv(white_path, sep=";")
    white["type"] = "White"
    
    return pd.concat([red, white], ignore_index=True)

df = load_data()

# ---------------- 3. Sidebar Filters ----------------
st.sidebar.title("Configuration")
st.sidebar.markdown("Filter the dataset to explore specific wine profiles.")

wine_selection = st.sidebar.multiselect("Wine Variant", ["Red", "White"], default=["Red", "White"])
quality_range = st.sidebar.slider("Quality Rating", int(df.quality.min()), int(df.quality.max()), (4, 8))

# Apply Filter Logic
filtered_df = df[
    (df['type'].isin(wine_selection)) & 
    (df['quality'].between(quality_range[0], quality_range[1]))
]

# ---------------- 4. Dashboard Header & Key Metrics ----------------
st.title("🍷 Wine Quality Analysis")
st.markdown(f"Exploring chemical properties across **{len(filtered_df)}** wine samples.")

# Real-time metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Avg Quality Score", f"{filtered_df['quality'].mean():.2f}")
m2.metric("Avg Alcohol Content", f"{filtered_df['alcohol'].mean():.1f}%")
m3.metric("Median pH Level", f"{filtered_df['pH'].median():.2f}")
m4.metric("Avg Residual Sugar", f"{filtered_df['residual sugar'].mean():.2f} g/L")

st.divider()

# ---------------- 5. The 10 Visualizations (Analytical Questions) ----------------

# Row 1: Distribution & Primary Driver
col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Quality Score Distribution")
    fig1 = px.histogram(filtered_df, x="quality", color="type", barmode="group", text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.subheader("2. Alcohol Impact on Quality")
    fig2 = px.box(filtered_df, x="quality", y="alcohol", color="type")
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Acidity & Physical Properties
col3, col4 = st.columns(2)
with col3:
    st.subheader("3. Fixed Acidity vs. Density")
    fig3 = px.scatter(filtered_df, x="fixed acidity", y="density", color="type", trendline="ols")
    st.plotly_chart(fig3, use_container_width=True)
with col4:
    st.subheader("4. Volatile Acidity Variance")
    fig4 = px.violin(filtered_df, y="volatile acidity", x="type", color="type", box=True)
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Chemical Balance
col5, col6 = st.columns(2)
with col5:
    st.subheader("5. pH Level Density Profile")
    fig5, ax5 = plt.subplots()
    sns.kdeplot(data=filtered_df, x="pH", hue="type", fill=True, ax=ax5)
    st.pyplot(fig5)
with col6:
    st.subheader("6. Sulphates vs. Chlorides Interaction")
    fig6 = px.scatter(filtered_df, x="sulphates", y="chlorides", size="alcohol", color="quality")
    st.plotly_chart(fig6, use_container_width=True)

# Row 4: Sulfur & Composition
col7, col8 = st.columns(2)
with col7:
    st.subheader("7. Total Sulfur Dioxide Analysis")
    fig7 = px.histogram(filtered_df, x="total sulfur dioxide", color="type", marginal="box")
    st.plotly_chart(fig7, use_container_width=True)
with col8:
    st.subheader("8. Residual Sugar Comparison")
    fig8 = px.strip(filtered_df, x="type", y="residual sugar", color="quality")
    st.plotly_chart(fig8, use_container_width=True)

# Row 5: Trends & Global Correlation
col9, col10 = st.columns(2)
with col9:
    st.subheader("9. Free Sulfur Dioxide Trend")
    avg_fsd = filtered_df.groupby('quality')['free sulfur dioxide'].mean().reset_index()
    fig9 = px.area(avg_fsd, x="quality", y="free sulfur dioxide")
    st.plotly_chart(fig9, use_container_width=True)
with col10:
    st.subheader("10. Global Feature Correlation Matrix")
    fig10, ax10 = plt.subplots(figsize=(10, 8))
    sns.heatmap(filtered_df.drop(columns=['type']).corr(), annot=True, cmap="coolwarm", fmt=".2f")
    st.pyplot(fig10)

st.divider()

# ---------------- 6. Raw Data Explorer ----------------
with st.expander("📂 Explore Raw Data Records"):
    st.dataframe(filtered_df, use_container_width=True)