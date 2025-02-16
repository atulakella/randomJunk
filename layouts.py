from dash import html, dcc

def create_navbar():
    return html.Div(
        children=[
            html.A("Dashboard", href="/", className="nav-button"),
            html.A("Life Analysis", href="/life-analysis", className="nav-button"),
        ],
        className="navbar"
    )

def create_layout(relaxed_df):
    return html.Div([
        create_navbar(),  # Add the navbar here

        html.H1("EEG Frequency Dashboard", style={"textAlign": "center", "color": "#fff"}),

        html.Div([
            html.Label("Select EEG State:", style={"color": "#fff"}),
            dcc.Dropdown(
                id="state-selector",
                options=[
                    {"label": "Relaxed", "value": "Relaxed"},
                    {"label": "Stressed", "value": "Stressed"},
                    {"label": "Active", "value": "Active"}
                ],
                value="Relaxed",
                clearable=False,
                style={"width": "50%", "margin-bottom": "20px"}
            )
        ], style={"textAlign": "center"}),

        html.Div([
            dcc.Graph(id="frequency-bar-chart", style={"width": "50%", "display": "inline-block"}),
            dcc.Graph(id="frequency-pie-chart", style={"width": "50%", "display": "inline-block"})
        ], style={"display": "flex"}),

        html.Hr(),

        html.Div([
            html.Label("Chatbot:", style={"color": "#fff"}),
            dcc.Input(id="chat-input", type="text", placeholder="Ask a question...", style={"width": "50%"}),
            html.Button("Submit", id="chat-submit", n_clicks=0, style={"margin-left": "10px"}),
            html.Div(id="chat-response", style={"color": "#fff", "margin-top": "40px","margin-bottom": "40px"})
        ], style={"textAlign": "center"}),

        html.Hr(),

        html.Div([
            html.Label("Generate Report:", style={"color": "#fff"}),
            dcc.Input(id="user-name", type="text", placeholder="Enter your name"),
            dcc.Input(id="user-age", type="number", placeholder="Enter your age"),
            html.Button("Download PDF", id="download-pdf-btn"),
            dcc.Download(id="pdf-download")
        ], style={"textAlign": "center", "margin-top": "20px"})
    ], style={"backgroundColor": "#2E1A47", "padding": "20px","margin":"-8px"})
