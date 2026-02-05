# Wine Quality Analysis
🍷 Vinho Verde Wine Quality Analytics

🎯 Project Objective
The goal of this project is to perform an in-depth Exploratory Data Analysis (EDA) on the "Vinho Verde" wine dataset from the UCI Machine Learning Repository. By analyzing chemical properties like acidity, sugar, and alcohol, this project seeks to uncover the key drivers behind wine quality ratings.

📊 Analytical Questions Addressed
As per the project requirements, this analysis explores 10 core questions:

Distribution: What is the frequency of each quality score across the dataset?

Alcohol Impact: Does higher alcohol content result in higher quality ratings?

Acidity vs. Density: How does fixed acidity influence the physical density of the wine?

Acidity Volatility: How does volatile acidity vary between Red and White wines?

pH Balance: What is the typical pH range for high-quality vs. low-quality samples?

Chemical Interaction: Is there a relationship between sulphates and chlorides?

Sulfur Dioxide: How does total sulfur dioxide concentration differ by wine type?

Sugar Content: Do sweeter wines (residual sugar) correlate with specific quality scores?

Trend Analysis: How does free sulfur dioxide trend across the quality spectrum?

Global Correlation: Which chemical features have the strongest positive and negative correlations with quality?

🛠️ Technical Procedure
Data Integration: Merged Red and White wine datasets using Pandas, implementing a type feature for categorical analysis.

Data Cleaning: Handled semicolon-delimited files and verified data integrity for 6,497 samples.

Interactive UI: Developed a multi-view dashboard using Streamlit with dynamic filtering.

Advanced Plotting: Utilized Plotly Express for interactive charts and Seaborn for statistical heatmaps and KDE plots.
