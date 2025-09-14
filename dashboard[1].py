import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Education Program Dashboard")

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load Excel
    data_df = pd.read_excel(uploaded_file, sheet_name="Data")
    calc_df = pd.read_excel(uploaded_file, sheet_name="Calc")
    filters_df = pd.read_excel(uploaded_file, sheet_name="Filters")

    # --- Sidebar Filters ---
    st.sidebar.header("Filters")
    regions = filters_df["Regions"].dropna().unique().tolist()
    coordinators = filters_df["Coordinators"].dropna().unique().tolist()

    selected_region = st.sidebar.multiselect("Select Region", regions, default=regions)
    selected_coord = st.sidebar.multiselect("Select Coordinator", coordinators, default=coordinators)

    # --- Apply Filters ---
    filtered_df = data_df[
        (data_df["Region"].isin(selected_region)) &
        (data_df["Coordinator"].isin(selected_coord))
    ]

    # --- KPIs ---
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    active_24_25 = filtered_df.loc[filtered_df["Year"]=="24-25", "Active_Users"].sum()
    active_25_26 = filtered_df.loc[filtered_df["Year"]=="25-26", "Active_Users"].sum()
    children_total = filtered_df["Unique_Children"].sum()
    usage_hours_total = filtered_df["Usage_Hours"].sum()

    col1.metric("Active Users 24-25", active_24_25)
    col2.metric("Active Users 25-26", active_25_26)
    col3.metric("Unique Children", children_total)
    col4.metric("Usage Hours", usage_hours_total)

    # --- Charts ---
    st.subheader("Visual Insights")

    # 1. Active Users by Region
    fig1 = px.bar(filtered_df.groupby("Region")["Active_Users"].sum().reset_index(),
                  x="Region", y="Active_Users", color="Region",
                  title="Active Users by Region")
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Active Users by Coordinator
    fig2 = px.bar(filtered_df.groupby("Coordinator")["Active_Users"].sum().reset_index(),
                  x="Coordinator", y="Active_Users", color="Coordinator",
                  title="Active Users by Coordinator")
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Active Users Over Years
    fig3 = px.bar(filtered_df.groupby("Year")["Active_Users"].sum().reset_index(),
                  x="Year", y="Active_Users", text="Active_Users",
                  title="Active Users Comparison by Year")
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Usage Hours Over Time (by Year & Region)
    fig4 = px.line(filtered_df.groupby(["Year","Region"])["Usage_Hours"].sum().reset_index(),
                   x="Year", y="Usage_Hours", color="Region",
                   title="Usage Hours by Year & Region", markers=True)
    st.plotly_chart(fig4, use_container_width=True)

    # --- Data Table ---
    st.subheader("Underlying Data (Filtered)")
    st.dataframe(filtered_df)

else:
    st.info("👆 Please upload an Excel file to get started.")
