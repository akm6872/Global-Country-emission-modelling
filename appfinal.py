import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="CO₂ & GHG Emissions Dashboard",
    layout="wide"
)

st.title("🌍 CO₂ & GHG Emissions Dashboard")
st.caption(
    "📜 Historical data: 1975–2024\n\n"
    "🔍 Focused view: ± 4 years\n\n"
    "🔮 Forecast up to +10 years"
)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    return pd.read_csv("owid_co2_dataset.csv")

@st.cache_resource
def load_models():
    return {
        "global_co2": joblib.load("global_co2_arima.joblib"),
        "global_ghg": joblib.load("global_ghg_arima.joblib"),
        "country_co2": joblib.load("co2_country_models.joblib"),
        "country_ghg": joblib.load("ghg_country_models.joblib"),
    }

df = load_data()
models = load_models()

# ------------------ SIDEBAR ------------------
st.sidebar.header("Controls")

level = st.sidebar.selectbox("Level", ["Global", "Country"])
target = st.sidebar.selectbox("Target variable", ["CO₂", "Total GHG"])
mode = st.sidebar.radio("Mode", ["Historical lookup", "Forecast"])

if level == "Country":
    country = st.sidebar.selectbox(
        "Country",
        sorted(df["country"].dropna().unique())
    )

# ------------------ PREPARE SERIES ------------------
if level == "Global":
    if target == "CO₂":
        series = df.groupby("year")["co2"].sum(min_count=1)
        model = models["global_co2"]
        label = "Global CO₂ emissions"
    else:
        series = df.groupby("year")["total_ghg"].sum(min_count=1)
        model = models["global_ghg"]
        label = "Global total GHG emissions"
else:
    col = "co2" if target == "CO₂" else "total_ghg"
    series = (
        df[df["country"] == country]
        .set_index("year")[col]
    )
    model = models[f"country_{'co2' if target=='CO₂' else 'ghg'}"].get(country)
    label = f"{country} {target} emissions"

    if model is None:
        st.warning("Not enough data for this country.")
        st.stop()

series = series.dropna()
series.index = pd.PeriodIndex(series.index, freq="Y")

MIN_YEAR = 1975
MAX_YEAR = 2024

# ==================================================
# HISTORICAL LOOKUP
# ==================================================
if mode == "Historical lookup":

    year = st.slider("Select year", MIN_YEAR, MAX_YEAR, MIN_YEAR)
    selected_period = pd.Period(year, freq="Y")
    selected_value = series.loc[selected_period]

    focus_start = max(MIN_YEAR, year - 4)
    focus_end = min(MAX_YEAR, year + 4)

    focus_series = series.loc[
        (series.index.year >= focus_start) &
        (series.index.year <= focus_end)
    ]

    st.metric(
        f"{label} in {year}",
        f"{selected_value:,.2f}"
    )

    # Safe Y-range
    y_min = focus_series.min()
    y_max = focus_series.max()
    padding = max((y_max - y_min) * 0.25, y_max * 0.03)

    fig = go.Figure()

    # Historical line
    fig.add_trace(go.Scatter(
        x=focus_series.index.to_timestamp(),
        y=focus_series.values,
        mode="lines+markers",
        line=dict(width=3, color="#4C6EF5"),
        marker=dict(size=6),
        name="Historical",
        hovertemplate="Year %{x|%Y}<br>Value %{y:,.2f}<extra></extra>"
    ))

    # Halo (magnifying effect)
    fig.add_trace(go.Scatter(
        x=[selected_period.to_timestamp()],
        y=[selected_value],
        mode="markers",
        marker=dict(size=30, color="rgba(255,99,132,0.25)"),
        hoverinfo="skip",
        showlegend=False
    ))

    # Main highlighted point
    fig.add_trace(go.Scatter(
        x=[selected_period.to_timestamp()],
        y=[selected_value],
        mode="markers+text",
        marker=dict(
            size=10,
            color="crimson",
            line=dict(width=2, color="white")
        ),
        text=[f"{selected_value:,.2f}"],
        textposition="top center",
        textfont=dict(size=14),
        name="Selected year"
    ))

    fig.update_layout(
    title=f"{label} — {focus_start} to {focus_end}",
    xaxis_title="Year",
    yaxis_title=target,
    template="plotly_dark",
    transition=dict(duration=300),
    autosize=True,
    height=500
    )

    left_pad = pd.DateOffset(months=6) if focus_start == MIN_YEAR else pd.DateOffset(months=0)

    fig.update_xaxes(
    tickmode="linear",
    dtick="M12",
    tickformat="%Y"
)   

    fig.update_yaxes(
        nticks=5
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "responsive": True,
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["toggleFullscreen"]
        },
        key=f"historical_{year}"
    )

# ==================================================
# FORECAST
# ==================================================
else:
    horizon = st.slider("Forecast horizon (years)", 1, 10, 5)

    forecast = model.forecast(steps=horizon)

    last_forecast_year = forecast.index[-1].year
    last_forecast_value = forecast.iloc[-1]

    st.metric(
        f"{label} in {last_forecast_year}",
        f"{last_forecast_value:,.2f}"
    )

    last_year = series.index[-1].year
    forecast.index = pd.PeriodIndex(
        range(last_year + 1, last_year + 1 + horizon),
        freq="Y"
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=series.index.to_timestamp(),
        y=series.values,
        mode="lines",
        line=dict(width=3),
        name="Historical"
    ))

    # Bridge last historical point to forecast
    bridge_x = [
        series.index[-1].to_timestamp(),
        forecast.index[0].to_timestamp()
    ]

    bridge_y = [
        series.values[-1],
        forecast.values[0]
    ]

    fig.add_trace(go.Scatter(
    x=bridge_x,
    y=bridge_y,
    mode="lines",
    line=dict(width=3, color="#4C6EF5"),  # SAME blue as historical
    showlegend=False
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=forecast.index.to_timestamp(),
        y=forecast.values,
        mode="lines+markers",
        line=dict(width=3, dash="dash", color="red"),
        marker=dict(size=6),
        name="Forecast"
    ))

    fig.update_layout(
    title=f"{label} — {horizon}-year forecast",
    xaxis_title="Year",
    yaxis_title=target,
    template="plotly_dark",
    autosize=True,
    height=500
    )

    fig.update_xaxes(
    tickmode="linear",
    dtick=5 * 365 * 24 * 60 * 60 * 1000,  # 5 years in milliseconds
    tickformat="%Y"
    )

    fig.update_yaxes(
    rangemode="normal",
    automargin=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"responsive": True},
    )

    # ------------------ FORECAST TABLE ------------------
    forecast_df = pd.DataFrame({
        "Year": forecast.index.year,
        target: forecast.values
    })

    st.subheader("📋 Forecast values")
    st.dataframe(forecast_df, use_container_width=True)

    # ------------------ DOWNLOAD CSV ------------------
    csv = forecast_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download forecast as CSV",
        data=csv,
        file_name=f"{label.replace(' ', '_').lower()}_forecast.csv",
        mime="text/csv"
    )