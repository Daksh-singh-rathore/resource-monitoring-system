
import streamlit as st
import pandas as pd

from database import get_records


def show_reports():
    st.title("📄 Resource Usage Reports")

    records = get_records()

    if not records:
        st.info("No records available to generate reports.")
        return

    df = pd.DataFrame(records)

    df["usage_date"] = pd.to_datetime(
        df["usage_date"], errors="coerce"
    )
    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    ).fillna(0)
    df["wastage_quantity"] = pd.to_numeric(
        df["wastage_quantity"], errors="coerce"
    ).fillna(0)

    valid_dates = df["usage_date"].dropna()

    if valid_dates.empty:
        st.warning("No valid dates found.")
        return

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_range = st.date_input(
        "Select report date range",
        value=(min_date, max_date)
    )

    resource_options = [
        "All Resources",
        "Water",
        "Electricity",
        "Materials"
    ]

    selected_resource = st.selectbox(
        "Filter by Resource",
        resource_options
    )

    if not isinstance(selected_range, (tuple, list)) or len(selected_range) != 2:
        st.info("Please select both a start date and an end date.")
        return

    start_date, end_date = selected_range

    filtered = df[
        (df["usage_date"].dt.date >= start_date)
        & (df["usage_date"].dt.date <= end_date)
    ].copy()

    if selected_resource != "All Resources":
        filtered = filtered[
            filtered["resource_type"] == selected_resource
        ]

    st.subheader("Report Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Entries", len(filtered))
    c2.metric("Total Quantity", f"{filtered['quantity'].sum():,.2f}")
    c3.metric("Total Wastage", f"{filtered['wastage_quantity'].sum():,.2f}")

    st.subheader("Detailed Report")

    display_columns = [
        "usage_date",
        "classroom",
        "resource_type",
        "resource_name",
        "quantity",
        "unit",
        "wastage_quantity",
        "purpose",
        "remarks"
    ]

    st.dataframe(
        filtered[display_columns],
        use_container_width=True
    )

    csv_data = filtered[display_columns].to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download CSV Report",
        data=csv_data,
        file_name="resource_usage_report.csv",
        mime="text/csv"
    )
