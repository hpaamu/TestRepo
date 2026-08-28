# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the downloaded dataset from your project folder
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get the maximum payload mass
max_payload = spacex_df["Payload Mass (kg)"].max()

# Create a Dash application
app = dash.Dash(__name__)

# Create the application layout
app.layout = html.Div(children=[
    html.H1(
        "SpaceX Launch Records Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "font-size": 40
        }
    ),

    # TASK 1: Launch Site dropdown
    dcc.Dropdown(
        id="site-dropdown",
        options=[
            {"label": "All Sites", "value": "ALL"},
            {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
            {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
            {"label": "KSC LC-39A", "value": "KSC LC-39A"},
            {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"}
        ],
        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # Pie chart
    html.Div(
        dcc.Graph(id="success-pie-chart")
    ),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload range slider
    dcc.RangeSlider(
        id="payload-slider",
        min=0,
        max=max_payload,
        step=1000,
        marks={
            0: "0",
            2500: "2500",
            5000: "5000",
            7500: "7500",
            10000: "10000"
        },
        value=[0, max_payload]
    ),

    html.Br(),

    # Scatter chart
    html.Div(
        dcc.Graph(id="success-payload-scatter-chart")
    )
])


# TASK 2: Callback for the pie chart
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value")
)
def get_pie_chart(entered_site):

    # When "All Sites" is selected, show successful launches by site
    if entered_site == "ALL":
        success_df = spacex_df[spacex_df["class"] == 1]

        fig = px.pie(
            success_df,
            names="Launch Site",
            title="Total Success Launches by Site"
        )

    # When one launch site is selected, show success vs failure
    else:
        filtered_df = spacex_df[
            spacex_df["Launch Site"] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names="class",
            title=f"Total Success Launches for site {entered_site}"
        )

    return fig


# TASK 4: Callback for the scatter chart
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [
        Input("site-dropdown", "value"),
        Input("payload-slider", "value")
    ]
)
def get_scatter_chart(entered_site, payload_range):

    low, high = payload_range

    # Filter data based on selected payload range
    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low) &
        (spacex_df["Payload Mass (kg)"] <= high)
    ]

    # Display data for every launch site
    if entered_site == "ALL":
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            hover_data=["Launch Site"],
            title="Correlation between Payload and Success for All Sites"
        )

    # Display data for the selected launch site only
    else:
        site_df = filtered_df[
            filtered_df["Launch Site"] == entered_site
        ]

        fig = px.scatter(
            site_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Success for {entered_site}"
        )

    return fig


# Run the Dash application
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)