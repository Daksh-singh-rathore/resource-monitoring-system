
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import init_db, add_record, get_records


RESOURCE_COLORS = {
    "Water": "#2196F3",
    "Electricity": "#F59E0B",
    "Materials": "#10B981",
}

WASTAGE_COLOR = "#EF4444"


def show_add_usage():
    init_db()

    st.title("Add Resource Usage")

    resource_type = st.selectbox(
        "Select Resource Type",
        ["Water", "Electricity", "Materials"],
        key="add_resource_selector",
    )

    resource_name = resource_type
    unit = "Litres"

    if resource_type == "Water":
        unit = "Litres"
    elif resource_type == "Electricity":
        unit = "kWh"
    else:
        resource_name = st.text_input("Material Name")
        unit = st.selectbox(
            "Select Unit",
            ["Pieces", "Kg", "Packets", "Sheets"],
        )

    with st.form("resource_usage_form"):
        usage_date = st.date_input(
            "Usage Date",
            value=date.today(),
        )

        classroom = st.text_input("Classroom")

        if resource_type == "Water":
            quantity = st.number_input(
                "Water Consumed (Litres)",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

            wastage_quantity = st.number_input(
                "Water Wasted (Litres)",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

        elif resource_type == "Electricity":
            quantity = st.number_input(
                "Electricity Consumed (kWh)",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

            wastage_quantity = st.number_input(
                "Electricity Wasted (kWh)",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

        else:
            quantity = st.number_input(
                f"Material Used ({unit})",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

            wastage_quantity = st.number_input(
                f"Material Wasted ({unit})",
                min_value=0.0,
                value=0.0,
                step=1.0,
            )

        purpose = st.text_input("Purpose")
        remarks = st.text_area("Remarks")

        submitted = st.form_submit_button(
            "Save Usage",
            use_container_width=True,
        )

    if submitted:
        if not classroom.strip():
            st.error("Please enter a classroom name.")

        elif resource_type == "Materials" and not resource_name.strip():
            st.error("Please enter a material name.")

        elif quantity <= 0:
            st.error("Quantity must be greater than zero.")

        elif wastage_quantity > quantity:
            st.error("Wasted quantity cannot exceed total quantity.")

        else:
            try:
                add_record(
                    usage_date.isoformat(),
                    classroom.strip(),
                    resource_type,
                    resource_name.strip(),
                    quantity,
                    unit,
                    wastage_quantity,
                    purpose.strip(),
                    remarks.strip(),
                )

                st.success(
                    f"{resource_type} usage saved successfully!"
                )

            except Exception as e:
                st.error(f"Could not save the record: {e}")

    # Show graphs for the selected resource
    st.divider()
    st.subheader(f"{resource_type} Graphs")

    try:
        records = get_records()

        if not records:
            st.info(
                "No records yet. Save a usage entry to see the graphs."
            )
            return

        df = pd.DataFrame(records)

        required_columns = [
            "resource_type",
            "classroom",
            "usage_date",
            "quantity",
            "wastage_quantity",
        ]

        if not all(col in df.columns for col in required_columns):
            st.warning(
                "Your database schema does not match the graph code. "
                "Please check database.py."
            )
            return

        df["resource_type"] = (
            df["resource_type"].astype(str).str.strip()
        )

        df = df[
            df["resource_type"].str.lower()
            == resource_type.lower()
        ].copy()

        if df.empty:
            st.info(
                f"No {resource_type.lower()} data is available yet."
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

        df = df.dropna(subset=["usage_date"])

        if df.empty:
            st.info("No valid dates are available for graphing.")
            return

        color = RESOURCE_COLORS[resource_type]

        if resource_type in ["Water", "Electricity"]:
            unit_label = (
                "Litres" if resource_type == "Water" else "kWh"
            )

            c1, c2 = st.columns(2)

            c1.metric(
                f"Total {resource_type} Used",
                f"{df['quantity'].sum():,.2f} {unit_label}",
            )

            c2.metric(
                f"Total {resource_type} Wasted",
                f"{df['wastage_quantity'].sum():,.2f} {unit_label}",
            )

            # Classroom-wise bar graph
            classroom_data = (
                df.groupby("classroom", as_index=False)
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
                title=f"{resource_type} Usage by Classroom",
                template="plotly_white",
                labels={
                    "classroom": "Classroom",
                    "Quantity": f"Quantity ({unit_label})",
                },
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True,
                key=f"add_{resource_type}_classroom_graph",
            )

            # Date-wise line graph
            daily_data = (
                df.groupby(df["usage_date"].dt.date)
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
                title=f"Date-wise {resource_type} Usage",
                template="plotly_white",
                labels={
                    "Date": "Date",
                    "Quantity": f"Quantity ({unit_label})",
                },
            )

            st.plotly_chart(
                fig_line,
                use_container_width=True,
                key=f"add_{resource_type}_date_graph",
            )

        else:
            if "resource_name" not in df.columns:
                st.error("The resource_name column is missing.")
                return

            if "unit" not in df.columns:
                df["unit"] = "Units"

            df["resource_name"] = (
                df["resource_name"].fillna("Unnamed Material")
            )

            df["unit"] = df["unit"].fillna("Units")

            c1, c2 = st.columns(2)

            c1.metric("Total Material Used", f"{df['quantity'].sum():,.2f}")
            c2.metric(
                "Total Material Wasted",
                f"{df['wastage_quantity'].sum():,.2f}",
            )

            material_data = (
                df.groupby(["resource_name", "unit"], as_index=False)
                .agg(
                    Used=("quantity", "sum"),
                    Wasted=("wastage_quantity", "sum"),
                )
            )

            fig_used = px.bar(
                material_data,
                x="resource_name",
                y="Used",
                color="unit",
                title="Material-wise Usage",
                color_discrete_sequence=[
                    "#10B981", "#34D399", "#059669", "#6EE7B7"
                ],
                template="plotly_white",
                labels={
                    "resource_name": "Material",
                    "Used": "Quantity Used",
                    "unit": "Unit",
                },
            )

            st.plotly_chart(
                fig_used,
                use_container_width=True,
                key="add_material_used_graph",
            )

            fig_wasted = px.bar(
                material_data,
                x="resource_name",
                y="Wasted",
                color="unit",
                title="Material-wise Wastage",
                color_discrete_sequence=[
                    "#EF4444", "#F87171", "#DC2626", "#FCA5A5"
                ],
                template="plotly_white",
                labels={
                    "resource_name": "Material",
                    "Wasted": "Quantity Wasted",
                    "unit": "Unit",
                },
            )

            st.plotly_chart(
                fig_wasted,
                use_container_width=True,
                key="add_material_wasted_graph",
            )

            daily_data = (
                df.groupby(df["usage_date"].dt.date)
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
                    "Used": "#10B981",
                    "Wasted": WASTAGE_COLOR,
                },
                title="Date-wise Material Usage and Wastage",
                template="plotly_white",
            )

            st.plotly_chart(
                fig_line,
                use_container_width=True,
                key="add_material_date_graph",
            )

    except Exception as e:
        st.error(f"Unable to display graphs: {e}")
