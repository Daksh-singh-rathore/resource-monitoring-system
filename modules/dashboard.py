
import streamlit as st
import pandas as pd

from database import get_records


def show_dashboard(daily_limit=500.0):
    st.title("📊 Resource Wastage Dashboard")

    records = get_records()

    if not records:
        st.info("No data available. Add some resource entries first.")
        return

    df = pd.DataFrame(records)

    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    ).fillna(0)

    df["wastage_quantity"] = pd.to_numeric(
        df["wastage_quantity"], errors="coerce"
    ).fillna(0)

    water = df[df["resource_type"] == "Water"]
    electricity = df[df["resource_type"] == "Electricity"]
    materials = df[df["resource_type"] == "Materials"]

    total_water = water["quantity"].sum()
    total_electricity = electricity["quantity"].sum()
    total_material_used = materials["quantity"].sum()
    total_records = len(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Water Consumed", f"{total_water:,.1f} L")
    c2.metric("Electricity Used", f"{total_electricity:,.1f} kWh")
    c3.metric("Material Used", f"{total_material_used:,.1f}")
    c4.metric("Total Entries", total_records)

    st.subheader("Resource-wise Consumption")

    summary = (
        df.groupby("resource_type", as_index=False)
        ["quantity"].sum()
    )
    st.bar_chart(
        summary,
        x="resource_type",
        y="quantity"
    )

    st.subheader("Resource Wastage")

    wastage_summary = (
        df.groupby("resource_type", as_index=False)
        ["wastage_quantity"].sum()
    )
    st.bar_chart(
        wastage_summary,
        x="resource_type",
        y="wastage_quantity"
    )

    st.subheader("Classroom-wise Consumption")

    classroom_summary = (
        df.groupby(["classroom", "resource_type"], as_index=False)
        ["quantity"].sum()
    )

    st.dataframe(classroom_summary, use_container_width=True)

    st.subheader("Recent Entries")
    st.dataframe(
        df[[
            "usage_date",
            "classroom",
            "resource_type",
            "resource_name",
            "quantity",
            "unit",
            "wastage_quantity",
            "purpose"
        ]].head(10),
        use_container_width=True
    )

    st.subheader("Usage Alerts")

    water_daily = water.copy()
    if not water_daily.empty:
        water_daily["usage_date"] = pd.to_datetime(
            water_daily["usage_date"], errors="coerce"
        )

        daily_water = (
            water_daily.groupby(
                water_daily["usage_date"].dt.date
            )["quantity"].sum()
        )

        exceeded = daily_water[daily_water > daily_limit]

        if not exceeded.empty:
            for day, amount in exceeded.items():
                st.warning(
                    f"Water limit exceeded on {day}: "
                    f"{amount:.1f} L (limit: {daily_limit:.1f} L)"
                )
        else:
            st.success("No daily water limit exceeded.")
