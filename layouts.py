from dash import html, dcc
import dash

# Initialize the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Define the navigation bar
def create_navbar():
    return html.Div(
        style={
            "background-color": "#ffffff",
            "width": "70%",
            "margin": "20px auto",
            "padding": "10px 20px",
            "display": "flex",
            "justify-content": "space-between",
            "align-items": "center",
            "box-shadow": "0 2px 10px rgba(0, 0, 0, 0.1)",
            "border-radius": "8px",
            "font-family": "Trebuchet MS, sans-serif",  # Updated font
        },
        children=[
            # Left side: Logo and "Cognilift" heading
            html.Div(
                style={"display": "flex", "align-items": "center"},
                children=[
                    html.Img(src="assets/Brain.png", style={"height": "40px", "margin-right": "10px"}),  # Logo
                    html.Div("Cognilift", style={"font-size": "1.5em", "font-weight": "bold", "color": "#F84BAE"}),  # Heading
                ]
            ),
            # Right side: Navigation buttons
            html.Div(
                style={"display": "flex", "gap": "20px", "align-items": "center"},
                children=[
                    html.A("Dashboard", href="/dashboard", style={"color": "#231630", "text-decoration": "none", "padding": "5px 10px", "border-radius": "5px", "transition": "background-color 0.3s, transform 0.3s"}),
                    html.A("Live Analysis", href="/live-analysis", style={"color": "#231630", "text-decoration": "none", "padding": "5px 10px", "border-radius": "5px", "transition": "background-color 0.3s, transform 0.3s"}),
                ]
            ),
            # Login button
            html.Button(
                "Login",
                style={
                    "background": "linear-gradient(135deg, #F84BAE, #5A73EE)",
                    "color": "#ffffff",
                    "border": "none",
                    "padding": "10px 20px",
                    "border-radius": "5px",
                    "cursor": "pointer",
                    "transition": "background 0.3s, transform 0.3s",
                }
            )
        ]
    )
# Define the layout
def create_layout(relaxed_df):
    return html.Div(
        style={
            "backgroundColor": "#2E1A47",
            "padding": "20px",
            "margin": "-8px",
            "font-family": "Trebuchet MS, sans-serif",  # Updated font for the entire layout
        },
        children=[
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

            # Updated Chatbot section with logo aligned beside the search box
            html.Div(
                style={"display": "flex", "alignItems": "center", "justifyContent": "center", "margin-bottom": "20px"},
                children=[
                    html.Img(src="assets/CHATBBOT.png", style={"height": "60px", "margin-right": "10px"}),  # Chatbot logo with increased size
                    html.Div(
                        style={"display": "flex", "alignItems": "center"},
                        children=[
                            dcc.Input(id="chat-input", type="text", placeholder="Ask a question...", style={"width": "300px", "margin-right": "10px"}),
                            html.Button("Submit", id="chat-submit", n_clicks=0),
                        ]
                    )
                ]
            ),

            html.Div(id="chat-response", style={"color": "#fff", "textAlign": "center", "margin-top": "20px", "margin-bottom": "40px"}),

            html.Hr(),

            # Generate Report section
            html.Div(
                style={"position": "fixed", "bottom": "20px", "left": "20px"},
                children=[
                    html.Button(
                        "Generate Report",
                        id="generate-report-btn",
                        style={
                            "background-color": "#5A73EE",
                            "color": "#fff",
                            "border": "none",
                            "padding": "10px 20px",
                            "border-radius": "5px",
                            "cursor": "pointer",
                            "font-family": "Trebuchet MS, sans-serif",
                        }
                    ),
                    html.Div(
                        id="report-form",
                        style={"display": "none", "margin-top": "10px"},
                        children=[
                            dcc.Input(id="user-name", type="text", placeholder="Enter your name", style={"margin-right": "10px", "padding": "5px"}),
                            dcc.Input(id="user-age", type="number", placeholder="Enter your age", style={"margin-right": "10px", "padding": "5px"}),
                            html.Button(
                                "Download PDF",
                                id="download-pdf-btn",
                                style={
                                    "background-color": "#FF6B6B",  # Light red color
                                    "color": "#fff",
                                    "border": "none",
                                    "padding": "10px 20px",
                                    "border-radius": "5px",
                                    "cursor": "pointer",
                                    "font-family": "Trebuchet MS, sans-serif",
                                }
                            ),
                            dcc.Download(id="pdf-download")
                        ]
                    )
                ]
            )
        ]
    )
