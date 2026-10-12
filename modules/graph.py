
import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_records


RESOURCE_COLORS = {
    "Water": "#2196F3",
    "Electricity": "#F59E0B",
    "Materials": "#10B981",
}

WASTAGE_COLOR = "#EF4444"


def show_graphs(daily_limit=500.0):
    st.title("Resource Usage - Graphs & Insights")

    records = get_records()

    if not records:
        st.info("No records found. Please add resource usage first.")
        return

    df = pd.DataFrame(records)

    required_columns = [
        "resource_type",
        "classroom",
        "usage_date",
        "quantity",
        "wastage_quantity",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(
            "Database columns missing: "
            + ", ".join(missing)
            + ". Please check database.py."
        )
        return

    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    ).fillna(0)

    df["wastage_quantity"] = pd.to_numeric(
        df["wastage_quantity"], errors="coerce"
    ).fillna(0)

    df["usage_date"] = pd.to_datetime(
        df["usage_date"], errors="coerce"
    )

    df["resource_type"] = (
        df["resource_type"].astype(str).str.strip()
    )

    df = df.dropna(subset=["usage_date"])

    if df.empty:
        st.info("No valid usage dates found in the database.")
        return

    resource_type = st.selectbox(
        "Select Resource",
        ["Water", "Electricity", "Materials"],
        key="graph_resource_selector",
    )

    resource_df = df[
        df["resource_type"].str.lower()
        == resource_type.lower()
    ].copy()

    if resource_df.empty:
        st.info(
            f"No {resource_type.lower()} records found yet. "
            "Add some entries to view their graphs."
        )
        return

    color = RESOURCE_COLORS[resource_type]

    # -------------------------------
    # WATER AND ELECTRICITY GRAPHS
    # -------------------------------
    if resource_type in ["Water", "Electricity"]:
        unit = "Litres" if resource_type == "Water" else "kWh"

        total_used = resource_df["quantity"].sum()
        total_wasted = resource_df["wastage_quantity"].sum()

        col1, col2 = st.columns(2)

        col1.metric(
            f"Total {resource_type} Used",
            f"{total_used:,.2f} {unit}",
        )

        col2.metric(
            f"Total {resource_type} Wasted",
            f"{total_wasted:,.2f} {unit}",
        )

        st.subheader(f"{resource_type} Usage by Classroom")

        classroom_data = (
            resource_df.groupby("classroom", as_index=False)
            .agg(
                Used=("quantity", "sum"),
                Wasted=("wastage_quantity", "sum"),
            )
        )

        classroom_long = classroom_data.melt(
            id_vars="classroom",
            value_vars=["Used", "Wasted"],
            var_name="Category",
            value_name="Quantity",
        )

        classroom_long["Color"] = classroom_long[
            "Category"
        ].map({
            "Used": color,
            "Wasted": WASTAGE_COLOR,
        })

        fig_bar = px.bar(
            classroom_long,
            x="classroom",
            y="Quantity",
            color="Category",
            barmode="group",
            color_discrete_map={
                "Used": color,
                "Wasted": WASTAGE_COLOR,
            },
            labels={
                "classroom": "Classroom",
                "Quantity": f"Quantity ({unit})",
            },
            title=f"{resource_type} Used vs Wasted",
            template="plotly_white",
        )

        fig_bar.update_layout(
            legend_title_text="",
            xaxis_title="Classroom",
            yaxis_title=f"Quantity ({unit})",
            hovermode="x unified",
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader(f"Date-wise {resource_type} Consumption")

        daily_data = (
            resource_df.groupby(
                resource_df["usage_date"].dt.date
            )
            .agg(
                Used=("quantity", "sum"),
                Wasted=("wastage_quantity", "sum"),
            )
            .reset_index()
            .rename(columns={"usage_date": "Date"})
        )

        daily_data["Date"] = pd.to_datetime(daily_data["Date"])

        daily_long = daily_data.melt(
            id_vars="Date",
            value_vars=["Used", "Wasted"],
            var_name="Category",
            value_name="Quantity",
        )

        fig_line = px.line(
            daily_long,
            x="Date",
            y="Quantity",
            color="Category",
            markers=True,
            color_discrete_map={
                "Used": color,
                "Wasted": WASTAGE_COLOR,
            },
            labels={
                "Date": "Date",
                "Quantity": f"Quantity ({unit})",
            },
            title=f"Daily {resource_type} Consumption",
            template="plotly_white",
        )

        fig_line.update_layout(
            legend_title_text="",
            hovermode="x unified",
        )

        st.plotly_chart(fig_line, use_container_width=True)

        # Water usage limit alert
        if resource_type == "Water":
            st.subheader("Daily Water Usage Limit")

            limit = st.number_input(
                "Set daily water usage limit (Litres)",
                min_value=1.0,
                value=float(daily_limit),
                step=50.0,
                key="water_daily_limit",
            )

            daily_water = (
                resource_df.groupby(
                    resource_df["usage_date"].dt.date
                )["quantity"]
                .sum()
                .reset_index()
            )

            daily_water.columns = ["Date", "Water Used"]

            exceeded = daily_water[
                daily_water["Water Used"] > limit
            ]

            if not exceeded.empty:
                st.warning(
                    f"Water usage limit exceeded on "
                    f"{len(exceeded)} date(s)!"
                )
                st.dataframe(
                    exceeded,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.success("Daily water usage is within the set limit.")

    # -------------------------------
    # MATERIALS GRAPHS
    # -------------------------------
    else:
        if "resource_name" not in resource_df.columns:
            st.error(
                "The resource_name column is missing. "
                "Please check database.py."
            )
            return

        if "unit" not in resource_df.columns:
            resource_df["unit"] = "Units"

        resource_df["resource_name"] = (
            resource_df["resource_name"].fillna("Unnamed Material")
        )

        resource_df["unit"] = (
            resource_df["unit"].fillna("Units")
        )

        total_used = resource_df["quantity"].sum()
        total_wasted = resource_df["wastage_quantity"].sum()

        col1, col2 = st.columns(2)

        col1.metric("Total Material Used", f"{total_used:,.2f}")
        col2.metric("Total Material Wasted", f"{total_wasted:,.2f}")

        # Keep units separate so kilograms and pieces aren't added together.
        material_data = (
            resource_df.groupby(
                ["resource_name", "unit"], as_index=False
            )
            .agg(
                Used=("quantity", "sum"),
                Wasted=("wastage_quantity", "sum"),
            )
        )

        st.subheader("Material Used by Type")

        fig_used = px.bar(
            material_data,
            x="resource_name",
            y="Used",
            color="unit",
            barmode="group",
            color_discrete_sequence=[
                "#10B981",
                "#34D399",
                "#059669",
                "#6EE7B7",
            ],
            labels={
                "resource_name": "Material",
                "Used": "Quantity Used",
                "unit": "Unit",
            },
            title="Material-wise Usage",
            template="plotly_white",
        )

        st.plotly_chart(fig_used, use_container_width=True)

        st.subheader("Material Wastage by Type")

        fig_wasted = px.bar(
            material_data,
            x="resource_name",
            y="Wasted",
            color="unit",
            barmode="group",
            color_discrete_sequence=[
                "#EF4444",
                "#F87171",
                "#DC2626",
                "#FCA5A5",
            ],
            labels={
                "resource_name": "Material",
                "Wasted": "Quantity Wasted",
                "unit": "Unit",
            },
            title="Material-wise Wastage",
            template="plotly_white",
        )

        st.plotly_chart(fig_wasted, use_container_width=True)

        st.subheader("Date-wise Material Usage")

        daily_material = (
            resource_df.groupby(
                resource_df["usage_date"].dt.date
            )
            .agg(
                Used=("quantity", "sum"),
                Wasted=("wastage_quantity", "sum"),
            )
            .reset_index()
            .rename(columns={"usage_date": "Date"})
        )

        daily_material["Date"] = pd.to_datetime(
            daily_material["Date"]
        )

        daily_long = daily_material.melt(
            id_vars="Date",
            value_vars=["Used", "Wasted"],
            var_name="Category",
            value_name="Quantity",
        )

        fig_material_line = px.line(
            daily_long,
            x="Date",
            y="Quantity",
            color="Category",
            markers=True,
            color_discrete_map={
                "Used": "#10B981",
                "Wasted": "#EF4444",
            },
            title="Date-wise Material Usage and Wastage",
            template="plotly_white",
            labels={
                "Date": "Date",
                "Quantity": "Quantity",
            },
        )

        st.plotly_chart(
            fig_material_line,
            use_container_width=True,
        )
