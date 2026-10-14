# ============================================================
# HOTEL BUSINESS ANALYTICS
# Professional Streamlit Business Intelligence Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hotel Business Analytics",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL DARK THEME
# ============================================================

st.markdown("""
<style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    .main {
        background-color: #0f172a;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* ========================================================
       HEADERS
       ======================================================== */

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }

    .subtitle {
        font-size: 15px;
        color: #94a3b8;
        margin-bottom: 24px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .section-description {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* ========================================================
       KPI CARDS
       ======================================================== */

    .kpi-card {
        background: #1e293b;
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        min-height: 115px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.20);
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .kpi-value {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 800;
    }

    .kpi-subtitle {
        color: #64748b;
        font-size: 11px;
        margin-top: 5px;
    }

    /* ========================================================
       INSIGHT CARDS
       ======================================================== */

    .insight-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .insight-title {
        color: #f8fafc;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .insight-text {
        color: #cbd5e1;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ========================================================
       STATUS CARDS
       ======================================================== */

    .status-card {
        background: #172033;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        margin-top: 8px;
    }

    /* ========================================================
       STREAMLIT ELEMENTS
       ======================================================== */

    .stMarkdown,
    .stText,
    label,
    p {
        color: #f8fafc;
    }

    div[data-baseweb="select"] > div {
        background-color: #1e293b;
        border-color: #334155;
    }

    div[data-baseweb="select"] span {
        color: #f8fafc !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 8px;
    }

    hr {
        border-color: #334155;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #334155;
        background-color: #1e293b;
        color: #f8fafc;
    }

    .stButton > button:hover {
        border-color: #64748b;
        color: #ffffff;
    }

        /* ========================================================
       HIDE STREAMLIT DEFAULT UI
       ======================================================== */

    header[data-testid="stHeader"] {
        display: none !important;
    }

    div[data-testid="stToolbar"] {
        display: none !important;
    }

    #MainMenu {
        display: none !important;
    }

    footer {
        display: none !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CONSTANTS
# ============================================================

DATA_FILE = "hotel_bookings_data.csv"

MONTH_ORDER = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

MONTH_NUMBER = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_FILE)

    return df


# ============================================================
# DATA PREPARATION
# ============================================================

@st.cache_data
def prepare_data(df):

    df = df.copy()

    # --------------------------------------------------------
    # Numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "is_canceled",
        "lead_time",
        "arrival_date_year",
        "arrival_date_week_number",
        "arrival_date_day_of_month",
        "stays_in_weekend_nights",
        "stays_in_week_nights",
        "adults",
        "children",
        "babies",
        "previous_cancellations",
        "previous_bookings_not_canceled",
        "booking_changes",
        "days_in_waiting_list",
        "adr",
        "required_car_parking_spaces",
        "total_of_special_requests",
        "agent",
        "company",
        "is_repeated_guest"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # --------------------------------------------------------
    # Fill important numeric values
    # --------------------------------------------------------

    for col in [
        "adults",
        "children",
        "babies",
        "stays_in_weekend_nights",
        "stays_in_week_nights",
        "adr",
        "lead_time",
        "is_canceled"
    ]:

        if col in df.columns:

            df[col] = df[col].fillna(0)

    # --------------------------------------------------------
    # Total Nights
    # --------------------------------------------------------

    df["total_nights"] = (
        df.get(
            "stays_in_weekend_nights",
            pd.Series(0, index=df.index)
        ).fillna(0)
        +
        df.get(
            "stays_in_week_nights",
            pd.Series(0, index=df.index)
        ).fillna(0)
    )

    # --------------------------------------------------------
    # Total Guests
    # --------------------------------------------------------

    adults = df.get(
        "adults",
        pd.Series(0, index=df.index)
    ).fillna(0)

    children = df.get(
        "children",
        pd.Series(0, index=df.index)
    ).fillna(0)

    babies = df.get(
        "babies",
        pd.Series(0, index=df.index)
    ).fillna(0)

    df["total_guests"] = (
        adults + children + babies
    )

    # --------------------------------------------------------
    # Total Rooms / Booking Volume
    # --------------------------------------------------------

    if "is_canceled" in df.columns:

        df["booking_status"] = np.where(
            df["is_canceled"] == 1,
            "Cancelled",
            "Confirmed"
        )

    # --------------------------------------------------------
    # Booking Value
    #
    # ADR = Average Daily Rate
    # Estimated Booking Value = ADR × Total Nights
    # --------------------------------------------------------

    df["estimated_booking_value"] = (
        df["adr"].fillna(0)
        *
        df["total_nights"]
    )

    # --------------------------------------------------------
    # Realized Revenue
    #
    # Cancelled bookings are excluded because they do not
    # represent realized hotel revenue.
    # --------------------------------------------------------

    df["realized_revenue"] = np.where(
        df["is_canceled"] == 0,
        df["estimated_booking_value"],
        0
    )

    # --------------------------------------------------------
    # Arrival Date
    # --------------------------------------------------------

    if all(
        col in df.columns
        for col in [
            "arrival_date_year",
            "arrival_date_month",
            "arrival_date_day_of_month"
        ]
    ):

        df["arrival_month_number"] = (
            df["arrival_date_month"]
            .map(MONTH_NUMBER)
        )

        df["arrival_date"] = pd.to_datetime(
            dict(
                year=df["arrival_date_year"],
                month=df["arrival_month_number"],
                day=df["arrival_date_day_of_month"]
            ),
            errors="coerce"
        )

    # --------------------------------------------------------
    # Arrival Month
    # --------------------------------------------------------

    if "arrival_date_month" in df.columns:

        df["arrival_date_month"] = pd.Categorical(
            df["arrival_date_month"],
            categories=MONTH_ORDER,
            ordered=True
        )

    # --------------------------------------------------------
    # Guest Type
    # --------------------------------------------------------

    df["guest_type"] = np.select(
        [
            df["total_guests"] == 1,
            df["total_guests"] == 2,
            df["total_guests"] >= 3
        ],
        [
            "Single",
            "Couple",
            "Group / Family"
        ],
        default="Unknown"
    )

    # --------------------------------------------------------
    # Lead Time Segment
    # --------------------------------------------------------

    df["lead_time_segment"] = pd.cut(
        df["lead_time"],
        bins=[
            -1,
            7,
            30,
            90,
            180,
            np.inf
        ],
        labels=[
            "0–7 Days",
            "8–30 Days",
            "31–90 Days",
            "91–180 Days",
            "180+ Days"
        ]
    )

    # --------------------------------------------------------
    # Stay Length Segment
    # --------------------------------------------------------

    df["stay_length_segment"] = pd.cut(
        df["total_nights"],
        bins=[
            -1,
            1,
            3,
            7,
            14,
            np.inf
        ],
        labels=[
            "1 Night",
            "2–3 Nights",
            "4–7 Nights",
            "8–14 Nights",
            "15+ Nights"
        ]
    )

    return df


# ============================================================
# LOAD + PREPARE
# ============================================================

try:

    df = load_data()

    df = prepare_data(df)

except FileNotFoundError:

    st.error(
        f"❌ Could not find `{DATA_FILE}`. "
        "Make sure app.py and the CSV file are in the same folder."
    )

    st.stop()

except Exception as e:

    st.error(
        f"❌ Error while loading the dataset: {e}"
    )

    st.stop()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_currency(value):

    if pd.isna(value):
        return "$0"

    if abs(value) >= 1_000_000:

        return f"${value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:

        return f"${value / 1_000:.1f}K"

    return f"${value:,.0f}"


def format_number(value):

    if pd.isna(value):
        return "0"

    return f"{int(value):,}"


def kpi_card(title, value, subtitle=""):

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(title, description=""):

    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-description">{description}</div>
        """,
        unsafe_allow_html=True
    )


def dark_layout(fig, height=420):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1e293b",
        plot_bgcolor="#1e293b",
        font=dict(
            color="#f8fafc"
        ),
        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        ),
        height=height
    )

    return fig


def empty_chart(message="No data available"):

    fig = go.Figure()

    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(
            size=16,
            color="#94a3b8"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1e293b",
        plot_bgcolor="#1e293b",
        height=350
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:24px;
        font-weight:800;
        margin-bottom:4px;
    ">
        🏨 Hotel Analytics
    </div>

    <div style="
        font-size:12px;
        color:#94a3b8;
        margin-bottom:15px;
    ">
        Business Intelligence Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Dashboard",
    [
        "Executive Overview",
        "Booking Analysis",
        "Revenue Analysis",
        "Customer Analysis",
        "Cancellation Analysis",
        "Hotel Performance",
        "Time & Seasonal Analysis",
        "Business Insights",
        "Data Explorer"
    ]
)


# ============================================================
# DATASET INFORMATION
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown("### 📁 Dataset")

st.sidebar.write(
    f"Records: **{len(df):,}**"
)

st.sidebar.write(
    f"Columns: **{df.shape[1]:,}**"
)

if "arrival_date_year" in df.columns:

    min_year = int(df["arrival_date_year"].min())
    max_year = int(df["arrival_date_year"].max())

    st.sidebar.write(
        f"Period: **{min_year} – {max_year}**"
    )


# ============================================================
# GLOBAL FILTERS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown("### 🔎 Global Filters")

filtered_df = df.copy()


# ------------------------------------------------------------
# Hotel Filter
# ------------------------------------------------------------

if "hotel" in df.columns:

    hotel_options = [
        "All Hotels"
    ] + sorted(
        df["hotel"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_hotel = st.sidebar.selectbox(
        "Hotel Type",
        hotel_options
    )

    if selected_hotel != "All Hotels":

        filtered_df = filtered_df[
            filtered_df["hotel"] == selected_hotel
        ]


# ------------------------------------------------------------
# Year Filter
# ------------------------------------------------------------

if "arrival_date_year" in df.columns:

    year_options = sorted(
        df["arrival_date_year"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    selected_years = st.sidebar.multiselect(
        "Arrival Year",
        year_options,
        default=year_options
    )

    if selected_years:

        filtered_df = filtered_df[
            filtered_df[
                "arrival_date_year"
            ].isin(selected_years)
        ]

    else:

        filtered_df = filtered_df.iloc[0:0]


# ------------------------------------------------------------
# Market Segment Filter
# ------------------------------------------------------------

if "market_segment" in df.columns:

    segment_options = [
        "All Segments"
    ] + sorted(
        df["market_segment"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_segment = st.sidebar.selectbox(
        "Market Segment",
        segment_options
    )

    if selected_segment != "All Segments":

        filtered_df = filtered_df[
            filtered_df["market_segment"]
            == selected_segment
        ]


# ------------------------------------------------------------
# Booking Status Filter
# ------------------------------------------------------------

if "booking_status" in df.columns:

    status_options = [
        "All Bookings",
        "Confirmed",
        "Cancelled"
    ]

    selected_status = st.sidebar.selectbox(
        "Booking Status",
        status_options
    )

    if selected_status != "All Bookings":

        filtered_df = filtered_df[
            filtered_df["booking_status"]
            == selected_status
        ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏨 HOTEL BUSINESS ANALYTICS</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Executive business intelligence platform for hotel
        bookings, revenue, customers, cancellations and
        seasonal performance.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    section_header(
        "Executive Overview",
        "High-level business performance and hotel booking KPIs."
    )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_bookings = len(filtered_df)

    confirmed_bookings = (
        (filtered_df["is_canceled"] == 0).sum()
        if "is_canceled" in filtered_df.columns
        else 0
    )

    cancelled_bookings = (
        (filtered_df["is_canceled"] == 1).sum()
        if "is_canceled" in filtered_df.columns
        else 0
    )

    cancellation_rate = (
        cancelled_bookings / total_bookings * 100
        if total_bookings > 0
        else 0
    )

    total_revenue = filtered_df[
        "realized_revenue"
    ].sum()

    estimated_value = filtered_df[
        "estimated_booking_value"
    ].sum()

    avg_adr = filtered_df[
        "adr"
    ].mean()

    total_nights = filtered_df[
        "total_nights"
    ].sum()

    avg_lead_time = filtered_df[
        "lead_time"
    ].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        kpi_card(
            "Total Bookings",
            format_number(total_bookings),
            "All selected bookings"
        )

    with col2:
        kpi_card(
            "Realized Revenue",
            format_currency(total_revenue),
            "Confirmed stays only"
        )

    with col3:
        kpi_card(
            "Average ADR",
            format_currency(avg_adr),
            "Average daily room rate"
        )

    with col4:
        kpi_card(
            "Cancellation Rate",
            f"{cancellation_rate:.1f}%",
            f"{cancelled_bookings:,} cancelled"
        )

    with col5:
        kpi_card(
            "Room Nights",
            format_number(total_nights),
            "Total booked nights"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SECOND KPI ROW
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            "Confirmed Bookings",
            format_number(confirmed_bookings),
            "Successful bookings"
        )

    with col2:
        kpi_card(
            "Avg Lead Time",
            f"{avg_lead_time:.0f} days",
            "Days before arrival"
        )

    with col3:
        kpi_card(
            "Avg Stay Length",
            f"{filtered_df['total_nights'].mean():.1f} nights",
            "Average stay duration"
        )

    with col4:
        kpi_card(
            "Booking Value",
            format_currency(estimated_value),
            "Estimated booking value"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # BOOKING TREND
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Booking Trend")

        if "arrival_date" in filtered_df.columns:

            trend = (
                filtered_df
                .dropna(subset=["arrival_date"])
                .groupby("arrival_date")
                .size()
                .reset_index(name="Bookings")
            )

            fig = px.line(
                trend,
                x="arrival_date",
                y="Bookings",
                title="Daily Booking Volume",
                markers=False
            )

            fig.update_traces(
                line=dict(width=2)
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # HOTEL DISTRIBUTION
    # --------------------------------------------------------

    with col2:

        st.subheader("🏨 Hotel Booking Mix")

        if "hotel" in filtered_df.columns:

            hotel_mix = (
                filtered_df["hotel"]
                .value_counts()
                .reset_index()
            )

            hotel_mix.columns = [
                "Hotel",
                "Bookings"
            ]

            fig = px.pie(
                hotel_mix,
                names="Hotel",
                values="Bookings",
                hole=0.55,
                title="Bookings by Hotel Type"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # REVENUE + CANCELLATION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("💰 Revenue by Hotel")

        if "hotel" in filtered_df.columns:

            revenue_hotel = (
                filtered_df
                .groupby("hotel")
                .agg(
                    Revenue=(
                        "realized_revenue",
                        "sum"
                    )
                )
                .reset_index()
            )

            fig = px.bar(
                revenue_hotel,
                x="hotel",
                y="Revenue",
                text_auto=".2s",
                title="Realized Revenue by Hotel"
            )

            fig.update_layout(
                xaxis_title="Hotel",
                yaxis_title="Revenue"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    with col2:

        st.subheader("❌ Booking Status")

        status_data = (
            filtered_df["booking_status"]
            .value_counts()
            .reset_index()
        )

        status_data.columns = [
            "Status",
            "Bookings"
        ]

        fig = px.bar(
            status_data,
            x="Status",
            y="Bookings",
            text="Bookings",
            title="Confirmed vs Cancelled Bookings"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )


# ============================================================
# BOOKING ANALYSIS
# ============================================================

elif page == "Booking Analysis":

    section_header(
        "Booking Analysis",
        "Understand booking volume, lead time, channels and market segments."
    )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_bookings = len(filtered_df)

    avg_lead = filtered_df["lead_time"].mean()

    avg_changes = filtered_df[
        "booking_changes"
    ].mean()

    special_requests = filtered_df[
        "total_of_special_requests"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            "Bookings",
            format_number(total_bookings)
        )

    with col2:
        kpi_card(
            "Avg Lead Time",
            f"{avg_lead:.0f} days"
        )

    with col3:
        kpi_card(
            "Avg Booking Changes",
            f"{avg_changes:.2f}"
        )

    with col4:
        kpi_card(
            "Special Requests",
            format_number(special_requests)
        )

    st.markdown("---")

    # --------------------------------------------------------
    # LEAD TIME
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("⏳ Lead Time Distribution")

        lead_data = (
            filtered_df
            .groupby("lead_time_segment")
            .size()
            .reset_index(name="Bookings")
        )

        fig = px.bar(
            lead_data,
            x="lead_time_segment",
            y="Bookings",
            title="Bookings by Lead Time"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )

    # --------------------------------------------------------
    # MARKET SEGMENT
    # --------------------------------------------------------

    with col2:

        st.subheader("🎯 Market Segment")

        if "market_segment" in filtered_df.columns:

            segment_data = (
                filtered_df["market_segment"]
                .value_counts()
                .reset_index()
            )

            segment_data.columns = [
                "Segment",
                "Bookings"
            ]

            fig = px.bar(
                segment_data,
                x="Segment",
                y="Bookings",
                title="Bookings by Market Segment"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # DISTRIBUTION CHANNEL
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📡 Distribution Channel")

        if "distribution_channel" in filtered_df.columns:

            channel_data = (
                filtered_df["distribution_channel"]
                .value_counts()
                .reset_index()
            )

            channel_data.columns = [
                "Channel",
                "Bookings"
            ]

            fig = px.pie(
                channel_data,
                names="Channel",
                values="Bookings",
                hole=0.5
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # DEPOSIT TYPE
    # --------------------------------------------------------

    with col2:

        st.subheader("💳 Deposit Type")

        if "deposit_type" in filtered_df.columns:

            deposit_data = (
                filtered_df["deposit_type"]
                .value_counts()
                .reset_index()
            )

            deposit_data.columns = [
                "Deposit Type",
                "Bookings"
            ]

            fig = px.bar(
                deposit_data,
                x="Deposit Type",
                y="Bookings",
                title="Booking Deposit Structure"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # TOP COUNTRIES
    # --------------------------------------------------------

    if "country" in filtered_df.columns:

        st.subheader("🌍 Top Guest Markets")

        country_data = (
            filtered_df["country"]
            .value_counts()
            .head(15)
            .reset_index()
        )

        country_data.columns = [
            "Country",
            "Bookings"
        ]

        fig = px.bar(
            country_data.sort_values(
                "Bookings"
            ),
            x="Bookings",
            y="Country",
            orientation="h",
            title="Top 15 Guest Countries"
        )

        st.plotly_chart(
            dark_layout(fig, 500),
            use_container_width=True
        )


# ============================================================
# REVENUE ANALYSIS
# ============================================================

elif page == "Revenue Analysis":

    section_header(
        "Revenue Analysis",
        "Analyze realized revenue, ADR, booking value and revenue trends."
    )

    total_revenue = filtered_df[
        "realized_revenue"
    ].sum()

    avg_adr = filtered_df[
        "adr"
    ].mean()

    confirmed = filtered_df[
        filtered_df["is_canceled"] == 0
    ]

    revenue_per_booking = (
        confirmed["realized_revenue"].mean()
        if len(confirmed) > 0
        else 0
    )

    total_room_nights = filtered_df[
        "total_nights"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            "Realized Revenue",
            format_currency(total_revenue)
        )

    with col2:
        kpi_card(
            "Average ADR",
            format_currency(avg_adr)
        )

    with col3:
        kpi_card(
            "Revenue / Booking",
            format_currency(revenue_per_booking)
        )

    with col4:
        kpi_card(
            "Room Nights",
            format_number(total_room_nights)
        )

    st.markdown("---")

    # --------------------------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------------------------

    if "arrival_date_month" in filtered_df.columns:

        monthly = (
            filtered_df
            .groupby(
                "arrival_date_month",
                observed=True
            )
            .agg(
                Revenue=(
                    "realized_revenue",
                    "sum"
                ),
                ADR=(
                    "adr",
                    "mean"
                ),
                Bookings=(
                    "is_canceled",
                    "count"
                )
            )
            .reset_index()
        )

        monthly["Month"] = monthly[
            "arrival_date_month"
        ].astype(str)

        monthly["Month Number"] = (
            monthly["Month"]
            .map(MONTH_NUMBER)
        )

        monthly = monthly.sort_values(
            "Month Number"
        )

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                monthly,
                x="Month",
                y="Revenue",
                title="Monthly Realized Revenue"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

        with col2:

            fig = px.line(
                monthly,
                x="Month",
                y="ADR",
                markers=True,
                title="Monthly Average Daily Rate"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # REVENUE BY MARKET SEGMENT
    # --------------------------------------------------------

    if "market_segment" in filtered_df.columns:

        segment_revenue = (
            filtered_df
            .groupby("market_segment")
            .agg(
                Revenue=(
                    "realized_revenue",
                    "sum"
                ),
                Bookings=(
                    "is_canceled",
                    "count"
                ),
                ADR=(
                    "adr",
                    "mean"
                )
            )
            .reset_index()
        )

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                segment_revenue,
                x="market_segment",
                y="Revenue",
                title="Revenue by Market Segment"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

        with col2:

            fig = px.scatter(
                segment_revenue,
                x="Bookings",
                y="Revenue",
                size="ADR",
                text="market_segment",
                title="Bookings vs Revenue by Segment"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # ADR DISTRIBUTION
    # --------------------------------------------------------

    st.subheader("💵 ADR Distribution")

    adr_data = filtered_df[
        filtered_df["adr"] >= 0
    ]

    fig = px.histogram(
        adr_data,
        x="adr",
        nbins=50,
        title="Distribution of Average Daily Rate"
    )

    st.plotly_chart(
        dark_layout(fig),
        use_container_width=True
    )


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

elif page == "Customer Analysis":

    section_header(
        "Customer Analysis",
        "Understand guest composition, repeat customers and geographic demand."
    )

    total_guests = filtered_df[
        "total_guests"
    ].sum()

    avg_guests = filtered_df[
        "total_guests"
    ].mean()

    repeat_guests = (
        filtered_df["is_repeated_guest"].sum()
        if "is_repeated_guest" in filtered_df.columns
        else 0
    )

    repeat_rate = (
        repeat_guests / len(filtered_df) * 100
        if len(filtered_df) > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            "Total Guests",
            format_number(total_guests)
        )

    with col2:
        kpi_card(
            "Avg Guests / Booking",
            f"{avg_guests:.1f}"
        )

    with col3:
        kpi_card(
            "Repeat Guests",
            format_number(repeat_guests)
        )

    with col4:
        kpi_card(
            "Repeat Guest Rate",
            f"{repeat_rate:.1f}%"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # GUEST TYPE
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        guest_type = (
            filtered_df["guest_type"]
            .value_counts()
            .reset_index()
        )

        guest_type.columns = [
            "Guest Type",
            "Bookings"
        ]

        fig = px.pie(
            guest_type,
            names="Guest Type",
            values="Bookings",
            hole=0.5,
            title="Guest Composition"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )

    # --------------------------------------------------------
    # CUSTOMER TYPE
    # --------------------------------------------------------

    with col2:

        if "customer_type" in filtered_df.columns:

            customer_type = (
                filtered_df["customer_type"]
                .value_counts()
                .reset_index()
            )

            customer_type.columns = [
                "Customer Type",
                "Bookings"
            ]

            fig = px.bar(
                customer_type,
                x="Customer Type",
                y="Bookings",
                title="Customer Type Distribution"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # TOP COUNTRIES
    # --------------------------------------------------------

    if "country" in filtered_df.columns:

        st.subheader("🌍 Geographic Customer Demand")

        country = (
            filtered_df
            .groupby("country")
            .agg(
                Bookings=(
                    "is_canceled",
                    "count"
                ),
                Revenue=(
                    "realized_revenue",
                    "sum"
                )
            )
            .reset_index()
            .sort_values(
                "Bookings",
                ascending=False
            )
            .head(20)
        )

        fig = px.bar(
            country.sort_values("Bookings"),
            x="Bookings",
            y="country",
            orientation="h",
            title="Top 20 Customer Countries"
        )

        st.plotly_chart(
            dark_layout(fig, 550),
            use_container_width=True
        )

    # --------------------------------------------------------
    # FAMILY / GUEST SIZE
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            filtered_df,
            x="total_guests",
            nbins=10,
            title="Guests per Booking"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )

    with col2:

        if "is_repeated_guest" in filtered_df.columns:

            repeat_data = (
                filtered_df[
                    "is_repeated_guest"
                ]
                .map({
                    0: "New Guest",
                    1: "Repeat Guest"
                })
                .value_counts()
                .reset_index()
            )

            repeat_data.columns = [
                "Customer",
                "Bookings"
            ]

            fig = px.bar(
                repeat_data,
                x="Customer",
                y="Bookings",
                title="New vs Repeat Guests"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )


# ============================================================
# CANCELLATION ANALYSIS
# ============================================================

elif page == "Cancellation Analysis":

    section_header(
        "Cancellation Analysis",
        "Identify cancellation patterns, risk factors and high-risk booking segments."
    )

    total = len(filtered_df)

    cancelled = (
        filtered_df["is_canceled"] == 1
    ).sum()

    confirmed = (
        filtered_df["is_canceled"] == 0
    ).sum()

    cancellation_rate = (
        cancelled / total * 100
        if total > 0
        else 0
    )

    avg_cancelled_lead = (
        filtered_df[
            filtered_df["is_canceled"] == 1
        ]["lead_time"].mean()
        if cancelled > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            "Cancellation Rate",
            f"{cancellation_rate:.1f}%"
        )

    with col2:
        kpi_card(
            "Cancelled Bookings",
            format_number(cancelled)
        )

    with col3:
        kpi_card(
            "Confirmed Bookings",
            format_number(confirmed)
        )

    with col4:
        kpi_card(
            "Avg Cancelled Lead Time",
            f"{avg_cancelled_lead:.0f} days"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # CANCELLATION BY HOTEL
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if "hotel" in filtered_df.columns:

            hotel_cancel = (
                filtered_df
                .groupby("hotel")
                .agg(
                    Bookings=(
                        "is_canceled",
                        "count"
                    ),
                    Cancellations=(
                        "is_canceled",
                        "sum"
                    )
                )
                .reset_index()
            )

            hotel_cancel["Cancellation Rate"] = (
                hotel_cancel["Cancellations"]
                /
                hotel_cancel["Bookings"]
                *
                100
            )

            fig = px.bar(
                hotel_cancel,
                x="hotel",
                y="Cancellation Rate",
                text=hotel_cancel[
                    "Cancellation Rate"
                ].round(1),
                title="Cancellation Rate by Hotel"
            )

            fig.update_layout(
                yaxis_title="Cancellation Rate (%)"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # CANCELLATION BY MARKET SEGMENT
    # --------------------------------------------------------

    with col2:

        if "market_segment" in filtered_df.columns:

            segment_cancel = (
                filtered_df
                .groupby("market_segment")
                .agg(
                    Bookings=(
                        "is_canceled",
                        "count"
                    ),
                    Cancellations=(
                        "is_canceled",
                        "sum"
                    )
                )
                .reset_index()
            )

            segment_cancel[
                "Cancellation Rate"
            ] = (
                segment_cancel["Cancellations"]
                /
                segment_cancel["Bookings"]
                *
                100
            )

            fig = px.bar(
                segment_cancel.sort_values(
                    "Cancellation Rate",
                    ascending=False
                ),
                x="market_segment",
                y="Cancellation Rate",
                title="Cancellation Rate by Market Segment"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

    # --------------------------------------------------------
    # LEAD TIME VS CANCELLATION
    # --------------------------------------------------------

    st.subheader("⏳ Cancellation Risk by Lead Time")

    lead_cancel = (
        filtered_df
        .groupby("lead_time_segment", observed=True)
        .agg(
            Bookings=(
                "is_canceled",
                "count"
            ),
            Cancellations=(
                "is_canceled",
                "sum"
            )
        )
        .reset_index()
    )

    lead_cancel["Cancellation Rate"] = (
        lead_cancel["Cancellations"]
        /
        lead_cancel["Bookings"]
        *
        100
    )

    fig = px.bar(
        lead_cancel,
        x="lead_time_segment",
        y="Cancellation Rate",
        text=lead_cancel[
            "Cancellation Rate"
        ].round(1),
        title="Cancellation Rate by Lead-Time Segment"
    )

    st.plotly_chart(
        dark_layout(fig),
        use_container_width=True
    )

    # --------------------------------------------------------
    # DEPOSIT TYPE
    # --------------------------------------------------------

    if "deposit_type" in filtered_df.columns:

        deposit_cancel = (
            filtered_df
            .groupby("deposit_type")
            .agg(
                Bookings=(
                    "is_canceled",
                    "count"
                ),
                Cancellations=(
                    "is_canceled",
                    "sum"
                )
            )
            .reset_index()
        )

        deposit_cancel[
            "Cancellation Rate"
        ] = (
            deposit_cancel["Cancellations"]
            /
            deposit_cancel["Bookings"]
            *
            100
        )

        st.subheader("💳 Cancellation Risk by Deposit Type")

        fig = px.bar(
            deposit_cancel,
            x="deposit_type",
            y="Cancellation Rate",
            title="Cancellation Rate by Deposit Type"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )


# ============================================================
# HOTEL PERFORMANCE
# ============================================================

elif page == "Hotel Performance":

    section_header(
        "Hotel Performance",
        "Compare City Hotel and Resort Hotel business performance."
    )

    if "hotel" in filtered_df.columns:

        performance = (
            filtered_df
            .groupby("hotel")
            .agg(
                Bookings=(
                    "is_canceled",
                    "count"
                ),
                Confirmed=(
                    "is_canceled",
                    lambda x: (x == 0).sum()
                ),
                Cancellations=(
                    "is_canceled",
                    "sum"
                ),
                Revenue=(
                    "realized_revenue",
                    "sum"
                ),
                ADR=(
                    "adr",
                    "mean"
                ),
                Room_Nights=(
                    "total_nights",
                    "sum"
                ),
                Guests=(
                    "total_guests",
                    "sum"
                )
            )
            .reset_index()
        )

        performance[
            "Cancellation Rate"
        ] = (
            performance["Cancellations"]
            /
            performance["Bookings"]
            *
            100
        )

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        best_revenue_hotel = performance.loc[
            performance["Revenue"].idxmax(),
            "hotel"
        ]

        best_adr_hotel = performance.loc[
            performance["ADR"].idxmax(),
            "hotel"
        ]

        with col1:
            kpi_card(
                "Best Revenue Hotel",
                str(best_revenue_hotel)
            )

        with col2:
            kpi_card(
                "Highest ADR",
                str(best_adr_hotel)
            )

        with col3:
            kpi_card(
                "Total Room Nights",
                format_number(
                    performance[
                        "Room_Nights"
                    ].sum()
                )
            )

        with col4:
            kpi_card(
                "Total Guests",
                format_number(
                    performance[
                        "Guests"
                    ].sum()
                )
            )

        st.markdown("---")

        # ----------------------------------------------------
        # PERFORMANCE TABLE
        # ----------------------------------------------------

        display_performance = performance.copy()

        display_performance[
            "Revenue"
        ] = display_performance[
            "Revenue"
        ].round(0)

        display_performance[
            "ADR"
        ] = display_performance[
            "ADR"
        ].round(2)

        display_performance[
            "Cancellation Rate"
        ] = display_performance[
            "Cancellation Rate"
        ].round(1)

        st.subheader("📋 Hotel Performance Scorecard")

        st.dataframe(
            display_performance,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # VISUAL COMPARISON
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            fig = px.bar(
                performance,
                x="hotel",
                y="Revenue",
                text_auto=".2s",
                title="Revenue Comparison"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

        with col2:

            fig = px.bar(
                performance,
                x="hotel",
                y="ADR",
                text_auto=".2f",
                title="ADR Comparison"
            )

            st.plotly_chart(
                dark_layout(fig),
                use_container_width=True
            )

        # ----------------------------------------------------
        # CANCELLATION
        # ----------------------------------------------------

        fig = px.bar(
            performance,
            x="hotel",
            y="Cancellation Rate",
            text=performance[
                "Cancellation Rate"
            ].round(1),
            title="Cancellation Rate Comparison"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )


# ============================================================
# TIME & SEASONAL ANALYSIS
# ============================================================

elif page == "Time & Seasonal Analysis":

    section_header(
        "Time & Seasonal Analysis",
        "Identify high-demand periods, monthly trends and seasonal patterns."
    )

    # --------------------------------------------------------
    # MONTHLY BOOKINGS
    # --------------------------------------------------------

    monthly = (
        filtered_df
        .groupby(
            "arrival_date_month",
            observed=True
        )
        .agg(
            Bookings=(
                "is_canceled",
                "count"
            ),
            Revenue=(
                "realized_revenue",
                "sum"
            ),
            ADR=(
                "adr",
                "mean"
            ),
            Room_Nights=(
                "total_nights",
                "sum"
            )
        )
        .reset_index()
    )

    monthly["Month"] = monthly[
        "arrival_date_month"
    ].astype(str)

    monthly["Month Number"] = (
        monthly["Month"]
        .map(MONTH_NUMBER)
    )

    monthly = monthly.sort_values(
        "Month Number"
    )

    # --------------------------------------------------------
    # PEAK MONTH
    # --------------------------------------------------------

    if len(monthly) > 0:

        peak_month = monthly.loc[
            monthly["Bookings"].idxmax(),
            "Month"
        ]

        peak_revenue_month = monthly.loc[
            monthly["Revenue"].idxmax(),
            "Month"
        ]

        col1, col2, col3 = st.columns(3)

        with col1:
            kpi_card(
                "Peak Booking Month",
                peak_month
            )

        with col2:
            kpi_card(
                "Peak Revenue Month",
                peak_revenue_month
            )

        with col3:
            kpi_card(
                "Peak Monthly Bookings",
                format_number(
                    monthly["Bookings"].max()
                )
            )

    st.markdown("---")

    # --------------------------------------------------------
    # MONTHLY BOOKING TREND
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.line(
            monthly,
            x="Month",
            y="Bookings",
            markers=True,
            title="Monthly Booking Trend"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            monthly,
            x="Month",
            y="Revenue",
            title="Monthly Revenue Trend"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )

    # --------------------------------------------------------
    # ADR TREND
    # --------------------------------------------------------

    fig = px.line(
        monthly,
        x="Month",
        y="ADR",
        markers=True,
        title="Average Daily Rate by Month"
    )

    st.plotly_chart(
        dark_layout(fig),
        use_container_width=True
    )

    # --------------------------------------------------------
    # YEARLY PERFORMANCE
    # --------------------------------------------------------

    if "arrival_date_year" in filtered_df.columns:

        yearly = (
            filtered_df
            .groupby("arrival_date_year")
            .agg(
                Bookings=(
                    "is_canceled",
                    "count"
                ),
                Revenue=(
                    "realized_revenue",
                    "sum"
                ),
                ADR=(
                    "adr",
                    "mean"
                )
            )
            .reset_index()
        )

        st.subheader("📊 Year-over-Year Performance")

        fig = px.bar(
            yearly,
            x="arrival_date_year",
            y="Bookings",
            text="Bookings",
            title="Bookings by Year"
        )

        st.plotly_chart(
            dark_layout(fig),
            use_container_width=True
        )

        st.dataframe(
            yearly.round(2),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

elif page == "Business Insights":

    section_header(
        "Business Insights",
        "Automatically generated observations from the selected dataset and filters."
    )

    # --------------------------------------------------------
    # BASIC CALCULATIONS
    # --------------------------------------------------------

    total = len(filtered_df)

    cancelled = (
        filtered_df["is_canceled"] == 1
    ).sum()

    confirmed = (
        filtered_df["is_canceled"] == 0
    ).sum()

    cancellation_rate = (
        cancelled / total * 100
        if total > 0
        else 0
    )

    avg_adr = filtered_df[
        "adr"
    ].mean()

    avg_lead = filtered_df[
        "lead_time"
    ].mean()

    avg_stay = filtered_df[
        "total_nights"
    ].mean()

    # --------------------------------------------------------
    # HOTEL INSIGHT
    # --------------------------------------------------------

    if "hotel" in filtered_df.columns:

        hotel_bookings = (
            filtered_df["hotel"]
            .value_counts()
        )

        top_hotel = hotel_bookings.idxmax()

        top_hotel_share = (
            hotel_bookings.iloc[0]
            /
            hotel_bookings.sum()
            *
            100
        )

    else:

        top_hotel = "N/A"
        top_hotel_share = 0

    # --------------------------------------------------------
    # SEGMENT INSIGHT
    # --------------------------------------------------------

    if "market_segment" in filtered_df.columns:

        segment_bookings = (
            filtered_df["market_segment"]
            .value_counts()
        )

        top_segment = segment_bookings.idxmax()

    else:

        top_segment = "N/A"

    # --------------------------------------------------------
    # MONTH INSIGHT
    # --------------------------------------------------------

    if len(filtered_df) > 0:

        monthly_insight = (
            filtered_df
            .groupby(
                "arrival_date_month",
                observed=True
            )
            .size()
        )

        if len(monthly_insight) > 0:

            peak_month = (
                monthly_insight
                .idxmax()
            )

        else:

            peak_month = "N/A"

    else:

        peak_month = "N/A"

    # --------------------------------------------------------
    # INSIGHT CARDS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    🏨 Hotel Demand
                </div>
                <div class="insight-text">
                    <b>{top_hotel}</b> generates the highest
                    booking volume, representing approximately
                    <b>{top_hotel_share:.1f}%</b> of the selected
                    booking portfolio.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    🎯 Leading Market Segment
                </div>
                <div class="insight-text">
                    The <b>{top_segment}</b> segment represents
                    the largest source of bookings in the
                    selected dataset.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    ❌ Cancellation Risk
                </div>
                <div class="insight-text">
                    The current cancellation rate is
                    <b>{cancellation_rate:.1f}%</b>.
                    This indicates that cancellation management
                    should be an important revenue-protection
                    priority.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    📅 Seasonal Demand
                </div>
                <div class="insight-text">
                    <b>{peak_month}</b> has the highest booking
                    volume within the selected analysis period.
                    This period can be targeted for pricing and
                    marketing optimization.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    💰 Pricing Indicator
                </div>
                <div class="insight-text">
                    The average daily rate is
                    <b>{format_currency(avg_adr)}</b>.
                    Management can compare this against seasonal
                    demand and cancellation patterns to optimize
                    pricing.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    ⏳ Booking Window
                </div>
                <div class="insight-text">
                    Guests book approximately
                    <b>{avg_lead:.0f} days</b> before arrival
                    on average, while the average stay length is
                    <b>{avg_stay:.1f} nights</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    st.subheader("💡 Business Recommendations")

    recommendations = [
        (
            "Dynamic Pricing",
            "Adjust room rates according to monthly demand, "
            "ADR trends and seasonal booking patterns."
        ),
        (
            "Cancellation Management",
            "Monitor high-risk booking segments and consider "
            "appropriate deposit or cancellation policies."
        ),
        (
            "Demand Forecasting",
            "Use historical booking trends to prepare staffing, "
            "inventory and promotional campaigns."
        ),
        (
            "Customer Retention",
            "Develop loyalty campaigns for repeat guests and "
            "high-value customer segments."
        ),
        (
            "Channel Optimization",
            "Compare distribution channels based on booking "
            "volume, revenue and cancellation behavior."
        )
    ]

    for title, recommendation in recommendations:

        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">
                    {title}
                </div>
                <div class="insight-text">
                    {recommendation}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    section_header(
        "Data Explorer",
        "Explore, filter and download the underlying hotel booking dataset."
    )

    # --------------------------------------------------------
    # DATASET KPIs
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            "Rows",
            format_number(len(filtered_df))
        )

    with col2:
        kpi_card(
            "Columns",
            format_number(filtered_df.shape[1])
        )

    with col3:
        kpi_card(
            "Missing Values",
            format_number(
                filtered_df.isna().sum().sum()
            )
        )

    with col4:
        kpi_card(
            "Duplicate Rows",
            format_number(
                filtered_df.duplicated().sum()
            )
        )

    st.markdown("---")

    # --------------------------------------------------------
    # COLUMN FILTER
    # --------------------------------------------------------

    columns = filtered_df.columns.tolist()

    selected_columns = st.multiselect(
        "Select Columns",
        columns,
        default=columns[:min(12, len(columns))]
    )

    if selected_columns:

        st.dataframe(
            filtered_df[selected_columns],
            use_container_width=True,
            height=500,
            hide_index=True
        )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv_data,
        file_name="hotel_filtered_data.csv",
        mime="text/csv"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # DATA QUALITY
    # --------------------------------------------------------

    st.subheader("📋 Data Quality Summary")

    quality = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": [
            str(dtype)
            for dtype in filtered_df.dtypes
        ],
        "Missing Values": [
            filtered_df[col].isna().sum()
            for col in filtered_df.columns
        ],
        "Missing %": [
            round(
                filtered_df[col].isna().mean() * 100,
                2
            )
            for col in filtered_df.columns
        ],
        "Unique Values": [
            filtered_df[col].nunique()
            for col in filtered_df.columns
        ]
    })

    st.dataframe(
        quality,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # NUMERIC SUMMARY
    # --------------------------------------------------------

    st.subheader("📊 Statistical Summary")

    numeric_summary = (
        filtered_df
        .select_dtypes(
            include=np.number
        )
        .describe()
        .T
        .reset_index()
    )

    numeric_summary = numeric_summary.rename(
        columns={
            "index": "Column"
        }
    )

    st.dataframe(
        numeric_summary.round(2),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748b;
        font-size:12px;
        padding:10px;
    ">
        🏨 Hotel Business Analytics Dashboard
        &nbsp;•&nbsp;
        Built with Python, Pandas, Plotly & Streamlit
        &nbsp;•&nbsp;
        Business Intelligence Portfolio Project
    </div>
    """,
    unsafe_allow_html=True
)