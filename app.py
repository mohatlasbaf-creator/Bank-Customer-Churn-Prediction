
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Bank Customer Churn Analysis",
    layout="wide"
)

st.title("Bank Customer Churn Analysis")

# Load dataset
#df = pd.read_csv("Bank Customer Churn Prediction.csv")
from pathlib import Path

file_path = Path(__file__).parent / "Bank Customer Churn Prediction.csv"

df = pd.read_csv(file_path)

# Group customers by country and gender
churn_summary = df.groupby(
    ["country", "gender"], as_index=False
).agg(
    total_customers=("customer_id", "count"),
    churned_customers=("churn", "sum")
)

# Calculate churn percentage
churn_summary["churn_percentage"] = (
    churn_summary["churned_customers"] /
    churn_summary["total_customers"] * 100
).round(2)

# Create labels containing count and percentage
churn_summary["label"] = (
    churn_summary["churned_customers"].astype(str)
    + " (" +
    churn_summary["churn_percentage"].astype(str)
    + "%)"
)

# Section title
st.subheader("Customer Churn by Country and Gender")

# Select chart type
chart_type = st.radio(
    "Select visualization metric:",
    ["Number of Churned Customers", "Churn Percentage"],
    horizontal=True
)

if chart_type == "Number of Churned Customers":
    y_column = "churned_customers"
else:
    y_column = "churn_percentage"

# Create grouped bar chart
fig = px.bar(
    churn_summary,
    x="country",
    y=y_column,
    color="gender",
    barmode="group",
    text="label",
    color_discrete_map={
        "Female": "#EC4899",
        "Male": "#3B82F6"
    },
    category_orders={
        "gender": ["Female", "Male"]
    },
    hover_data={
        "total_customers": True,
        "churned_customers": True,
        "churn_percentage": ":.2f",
        "label": False
    },
    labels={
        "country": "Country",
        "gender": "Gender",
        "churned_customers": "Churned Customers",
        "churn_percentage": "Churn Rate (%)",
        "total_customers": "Total Customers"
    }
)

# Customize chart appearance
fig.update_traces(
    textposition="outside",
    cliponaxis=False,
    marker_line_width=0
)

fig.update_layout(
    height=550,
    template="plotly_white",
    legend_title_text="Gender",
    bargap=0.25,
    bargroupgap=0.1,
    margin=dict(t=60, b=40, l=40, r=40)
)

fig.update_yaxes(
    range=[0, churn_summary[y_column].max() * 1.25]
)

# Display percentage symbol when needed
if y_column == "churn_percentage":
    fig.update_yaxes(ticksuffix="%")

# Display chart
st.plotly_chart(fig, use_container_width=True)

# Display summary table
st.subheader("Churn Summary Table")

st.dataframe(
    churn_summary.drop(columns=["label"]),
    use_container_width=True,
    hide_index=True
)

# ==========================================
# Customer Churn by Membership Status
# ==========================================

st.subheader("Customer Churn by Membership Status")

# Group customers by membership status
member_summary = df.groupby(
    "active_member", as_index=False
).agg(
    total_customers=("customer_id", "count"),
    churned_customers=("churn", "sum")
)

# Convert membership status into readable labels
member_summary["membership_status"] = (
    member_summary["active_member"].map({
        0: "Inactive Members",
        1: "Active Members"
    })
)

# Calculate churn percentage
member_summary["churn_percentage"] = (
    member_summary["churned_customers"] /
    member_summary["total_customers"] * 100
).round(2)

# Create labels with count and percentage
member_summary["label"] = (
    member_summary["churned_customers"].astype(str)
    + " (" +
    member_summary["churn_percentage"].astype(str)
    + "%)"
)

# Select visualization metric
member_metric = st.radio(
    "Select membership visualization metric:",
    ["Number of Churned Customers", "Churn Percentage"],
    horizontal=True,
    key="membership_metric"
)

if member_metric == "Number of Churned Customers":
    member_y = "churned_customers"
else:
    member_y = "churn_percentage"

# Create bar chart
fig_member = px.bar(
    member_summary,
    x="membership_status",
    y=member_y,
    color="membership_status",
    text="label",
    color_discrete_map={
        "Active Members": "#2ECC71",
        "Inactive Members": "#E74C3C"
    },
    hover_data={
        "total_customers": True,
        "churned_customers": True,
        "churn_percentage": ":.2f",
        "label": False
    },
    labels={
        "membership_status": "Membership Status",
        "churned_customers": "Churned Customers",
        "churn_percentage": "Churn Rate (%)",
        "total_customers": "Total Customers"
    }
)

# Customize chart appearance
fig_member.update_traces(
    textposition="outside",
    textfont_size=15,
    width=0.45,
    cliponaxis=False
)

fig_member.update_layout(
    title="Active vs. Inactive Customer Churn",
    template="plotly_white",
    height=500,
    showlegend=False
)

fig_member.update_yaxes(
    range=[0, member_summary[member_y].max() * 1.25]
)

# Add percentage symbol when needed
if member_y == "churn_percentage":
    fig_member.update_yaxes(ticksuffix="%")

# Display chart
st.plotly_chart(fig_member, use_container_width=True)

# Display summary table
st.dataframe(
    member_summary[[
        "membership_status",
        "total_customers",
        "churned_customers",
        "churn_percentage"
    ]],
    hide_index=True,
    use_container_width=True
)

# ==========================================
# Customer Churn by Number of Products
# ==========================================

st.subheader("Customer Churn by Number of Products")

# Group customers by number of products
product_summary = df.groupby(
    "products_number", as_index=False
).agg(
    total_customers=("customer_id", "count"),
    churned_customers=("churn", "sum")
)

# Calculate churn percentage
product_summary["churn_percentage"] = (
    product_summary["churned_customers"] /
    product_summary["total_customers"] * 100
).round(2)

# Create labels with count and percentage
product_summary["label"] = (
    product_summary["churned_customers"].astype(str)
    + " (" +
    product_summary["churn_percentage"].astype(str)
    + "%)"
)

# Convert product numbers to categorical labels
product_summary["products_number"] = (
    product_summary["products_number"].astype(str)
)

# Select visualization metric
product_metric = st.radio(
    "Select product visualization metric:",
    ["Number of Churned Customers", "Churn Percentage"],
    horizontal=True,
    key="product_metric"
)

if product_metric == "Number of Churned Customers":
    product_y = "churned_customers"
else:
    product_y = "churn_percentage"

# Create bar chart
fig_product = px.bar(
    product_summary,
    x="products_number",
    y=product_y,
    color="products_number",
    text="label",
    color_discrete_map={
        "1": "#3498DB",
        "2": "#2ECC71",
        "3": "#F39C12",
        "4": "#E74C3C"
    },
    hover_data={
        "total_customers": True,
        "churned_customers": True,
        "churn_percentage": ":.2f",
        "label": False
    },
    labels={
        "products_number": "Number of Products",
        "churned_customers": "Churned Customers",
        "churn_percentage": "Churn Rate (%)",
        "total_customers": "Total Customers"
    }
)

# Customize chart appearance
fig_product.update_traces(
    textposition="outside",
    textfont_size=14,
    width=0.5,
    cliponaxis=False
)

fig_product.update_layout(
    title="Customer Churn by Number of Products Used",
    template="plotly_white",
    height=550,
    showlegend=False
)

fig_product.update_yaxes(
    range=[0, product_summary[product_y].max() * 1.25]
)

# Add percentage symbol when needed
if product_y == "churn_percentage":
    fig_product.update_yaxes(ticksuffix="%")

# Display chart
st.plotly_chart(fig_product, use_container_width=True)

# Display summary table
st.dataframe(
    product_summary[[
        "products_number",
        "total_customers",
        "churned_customers",
        "churn_percentage"
    ]],
    hide_index=True,
    use_container_width=True
)

# ==========================================
# Customer Churn by Age Group
# ==========================================

st.subheader("Customer Churn by Age Group")

# Find minimum and maximum age
min_age = df["age"].min()
max_age = df["age"].max()

# Create 10 equal-width age buckets
age_data = df.copy()

age_data["age_group"] = pd.cut(
    age_data["age"],
    bins=10,
    include_lowest=True
)

# Group customers by age bucket
age_summary = age_data.groupby(
    "age_group",
    observed=False,
    as_index=False
).agg(
    total_customers=("customer_id", "count"),
    churned_customers=("churn", "sum")
)

# Calculate churn percentage
age_summary["churn_percentage"] = (
    age_summary["churned_customers"] /
    age_summary["total_customers"] * 100
).fillna(0).round(2)

# Create readable age group labels
age_summary["age_group"] = age_summary["age_group"].apply(
    lambda x: f"{int(x.left) + 1}-{int(x.right)}"
).astype(str)

# Create labels with count and percentage
age_summary["label"] = age_summary.apply(
    lambda x: f'{x["churned_customers"]} '
              f'({x["churn_percentage"]:.2f}%)',
    axis=1
)

# Display minimum and maximum age
st.write(f"Customer age range: {min_age} to {max_age} years")

# Select visualization metric
age_metric = st.radio(
    "Select age visualization metric:",
    ["Number of Churned Customers", "Churn Percentage"],
    horizontal=True,
    key="age_metric"
)

if age_metric == "Number of Churned Customers":
    age_y = "churned_customers"
else:
    age_y = "churn_percentage"

# Create bar chart
fig_age = px.bar(
    age_summary,
    x="age_group",
    y=age_y,
    text="label",
    color="churn_percentage",
    color_continuous_scale="RdYlGn_r",
    category_orders={
        "age_group": age_summary["age_group"].tolist()
    },
    hover_data={
        "total_customers": True,
        "churned_customers": True,
        "churn_percentage": ":.2f",
        "label": False
    },
    labels={
        "age_group": "Age Group",
        "churned_customers": "Churned Customers",
        "churn_percentage": "Churn Rate (%)",
        "total_customers": "Total Customers"
    }
)

# Customize chart appearance
fig_age.update_traces(
    textposition="outside",
    textfont_size=13,
    cliponaxis=False
)

fig_age.update_layout(
    title="Customer Churn Across 10 Age Groups",
    template="plotly_white",
    height=550,
    bargap=0.25,
    coloraxis_colorbar=dict(
        title="Churn Rate (%)"
    )
)

fig_age.update_yaxes(
    range=[0, age_summary[age_y].max() * 1.25]
)

# Add percentage symbol when needed
if age_y == "churn_percentage":
    fig_age.update_yaxes(ticksuffix="%")

# Display chart
st.plotly_chart(fig_age, use_container_width=True)

# Display summary table
st.dataframe(
    age_summary[[
        "age_group",
        "total_customers",
        "churned_customers",
        "churn_percentage"
    ]],
    hide_index=True,
    use_container_width=True
)

# ==========================================
# Correlation Heatmap with Churn
# ==========================================

st.subheader("Feature Correlation with Customer Churn")

# Remove customer_id
df_corr = df.drop(columns=["customer_id"])

# Convert categorical columns into numerical columns
df_corr = pd.get_dummies(
    df_corr,
    columns=["country", "gender"],
    dtype=int
)

# Calculate Pearson correlation with churn
churn_corr = df_corr.corr()["churn"].drop("churn")

# Sort correlations from highest to lowest
churn_corr = churn_corr.sort_values(ascending=False)

# Convert to DataFrame for heatmap
heatmap_data = churn_corr.to_frame(name="Churn")

# Create correlation heatmap
fig_heatmap = px.imshow(
    heatmap_data,
    text_auto=".3f",
    color_continuous_scale="RdBu_r",
    color_continuous_midpoint=0,
    zmin=-1,
    zmax=1,
    aspect="auto",
    labels={
        "x": "Target Variable",
        "y": "Customer Features",
        "color": "Correlation"
    }
)

# Customize heatmap
fig_heatmap.update_layout(
    title="Correlation Between Customer Features and Churn",
    height=650,
    template="plotly_white",
    xaxis_title="",
    yaxis_title="Features"
)

fig_heatmap.update_traces(
    textfont_size=14
)

# Display heatmap in Streamlit
st.plotly_chart(fig_heatmap, use_container_width=True)

st.subheader("Full Correlation Matrix")

corr_matrix = df_corr.corr()

fig_matrix = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    color_continuous_midpoint=0,
    zmin=-1,
    zmax=1,
    aspect="equal"
)

fig_matrix.update_layout(
    title="Customer Features Correlation Matrix",
    height=800
)

fig_matrix.update_xaxes(tickangle=-45)

st.plotly_chart(fig_matrix, use_container_width=True)