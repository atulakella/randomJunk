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
        create_navbar(),
        
        html.H1("EEG Frequency Dashboard", style={
            "textAlign": "center", 
            "color": "#F84BAE",
            "fontFamily": "Arial, sans-serif",
            "marginTop": "20px"
        }),

        html.Div([
            html.Label("Select EEG State:", style={
                "color": "#F0EEE9", 
                "fontFamily": "Arial, sans-serif",
                "marginRight": "10px"
            }),
            dcc.Dropdown(
                id="state-selector",
                options=[
                    {"label": "Relaxed", "value": "Relaxed"},
                    {"label": "Stressed", "value": "Stressed"},
                    {"label": "Active", "value": "Active"}
                ],
                value="Relaxed",
                clearable=False,
                style={
                    "width": "50%",
                    "backgroundColor": "#F0EEE9",
                    "borderRadius": "5px",
                    "fontFamily": "Arial, sans-serif"
                }
            )
        ], style={"textAlign": "center", "margin": "20px 0"}),

        html.Div([
            dcc.Graph(id="frequency-bar-chart", style={"width": "50%", "display": "inline-block"}),
            dcc.Graph(id="frequency-pie-chart", style={"width": "50%", "display": "inline-block"})
        ], style={"display": "flex", "gap": "20px", "padding": "0 20px"}),

        html.Hr(style={"borderColor": "#5A73EE", "margin": "40px 0"}),

        html.Div([
            html.Div([
                html.Label("Chatbot:", style={
                    "color": "#F0EEE9",
                    "fontFamily": "Arial, sans-serif",
                    "marginBottom": "10px",
                    "display": "block"
                }),
                dcc.Input(
                    id="chat-input",
                    type="text",
                    placeholder="Ask a question...",
                    style={
                        "width": "50%",
                        "padding": "10px",
                        "borderRadius": "5px",
                        "border": "none",
                        "backgroundColor": "#F0EEE9",
                        "color": "#231630"
                    }
                ),
                html.Button(
                    "Submit", 
                    id="chat-submit", 
                    n_clicks=0,
                    className="btn"
                ),
            ], style={"marginBottom": "40px"}),
            
            html.Div(id="chat-response", style={
                "color": "#F0EEE9",
                "fontFamily": "Arial, sans-serif",
                "padding": "20px",
                "backgroundColor": "#38235D",
                "borderRadius": "10px",
                "width": "60%",
                "margin": "0 auto"
            })
        ], style={"textAlign": "center"}),

        html.Hr(style={"borderColor": "#5A73EE", "margin": "40px 0"}),

        html.Div([
            html.Label("Generate Report:", style={
                "color": "#F0EEE9",
                "fontFamily": "Arial, sans-serif",
                "marginBottom": "20px",
                "display": "block"
            }),
            html.Div([
                dcc.Input(
                    id="user-name",
                    type="text",
                    placeholder="Enter your name",
                    style={
                        "margin": "0 10px",
                        "padding": "10px",
                        "borderRadius": "5px",
                        "border": "none",
                        "backgroundColor": "#F0EEE9"
                    }
                ),
                dcc.Input(
                    id="user-age",
                    type="number",
                    placeholder="Enter your age",
                    style={
                        "margin": "0 10px",
                        "padding": "10px",
                        "borderRadius": "5px",
                        "border": "none",
                        "backgroundColor": "#F0EEE9"
                    }
                ),
                html.Button(
                    "Download PDF", 
                    id="download-pdf-btn", 
                    className="btn"
                )
            ]),
            dcc.Download(id="pdf-download")
        ], style={"textAlign": "center", "margin": "40px 0"}),
    ], style={
        "backgroundColor": "#231630",
        "minHeight": "100vh",
        "padding": "20px",
        "margin": "-8px",
        "fontFamily": "Arial, sans-serif"
    })