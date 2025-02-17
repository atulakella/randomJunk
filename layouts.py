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
                    html.Img(src="assets/logo.png", style={"height": "40px", "margin-right": "10px"}),  # Logo
                    html.Div("Cognilift", style={"font-size": "1.5em", "font-weight": "bold", "color": "#F84BAE"}),  # Heading
                ]
            ),
            # Right side: Navigation buttons
            html.Div(
                style={"display": "flex", "gap": "20px", "align-items": "center"},
                children=[
                    html.A(
                        "Home",
                        href="/dashboard",
                        style={
                            "background": "linear-gradient(135deg, #F84BAE, #5A73EE)",
                            "color": "#ffffff",
                            "text-decoration": "none",
                            "padding": "10px 20px",
                            "border-radius": "15px",  # Rounded edges
                            "transition": "background-color 0.3s, transform 0.3s",
                        }
                    ),
                    html.A(
                        "Live Analysis",
                        href="http://127.0.0.1:5000",
                        style={
                            "background": "linear-gradient(135deg, #F84BAE, #5A73EE)",
                            "color": "#ffffff",
                            "text-decoration": "none",
                            "padding": "10px 20px",
                            "border-radius": "15px",  # Rounded edges
                            "transition": "background-color 0.3s, transform 0.3s",
                        }
                    ),
                ]
            ),
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
            html.Div(style={"height": "100px"}),  # Spacer div
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
                    style={
                        "width": "300px",  # Fixed width for consistent sizing
                        "margin": "0px auto auto",  # Centered with bottom margin
                        "color": "#2E1A47",  # Dark purple text for contrast
                        "backgroundColor": "#ffffff",
                        "border": "1px solid #F84BAE",  # Accent border
                        "borderRadius": "5px",
                        "padding": "0px 0px",  # Internal spacing
                        "fontSize": "16px"  # Larger text
                    }
                )
            ], style={"textAlign": "center"}),

            # Wrapper for both graphs with enhanced box shadow
            html.Div(
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "gap": "20px",
                    "margin": "20px 0",
                },
                children=[
                    # Division for the bar chart
                    html.Div(
                        style={
                            "background-color": "#2E1A47",  # White background for contrast
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.3)",  # Stronger shadow
                            "width": "48%",
                        },
                        children=[
                            dcc.Graph(id="frequency-bar-chart")
                        ]
                    ),
                    # Division for the pie chart
                    html.Div(
                        style={
                            "background-color": "#2E1A47",  # White background for contrast
                            "padding": "20px",
                            "border-radius": "10px",
                            "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.3)",  # Stronger shadow
                            "width": "48%",
                        },
                        children=[
                            dcc.Graph(id="frequency-pie-chart")
                        ]
                    ),
                ]
            ),

            # Updated Chatbot section with logo aligned beside the search box
            html.Div(
                style={"display": "flex", "alignItems": "center", "justifyContent": "center", "margin-bottom": "20px"},
                children=[
                    # Chatbot image (larger size)
                    html.Img(src="assets/CHATBBOT.png", style={"height": "100px", "margin-right": "20px"}),  # Increased size
                    html.Div(
                        style={"display": "flex", "alignItems": "center"},
                        children=[
                            # Input field (larger and rounded corners)
                            dcc.Input(
                                id="chat-input",
                                type="text",
                                placeholder="Ask a question...",
                                style={
                                    "width": "70%",  # Increased width
                                    "margin-right": "10px",
                                    "padding": "10px 15px",  # Increased padding
                                    "border-radius": "25px",  # Rounded corners
                                    "border": "1px solid #ccc",  # Subtle border
                                    "font-size": "1em",  # Larger font size
                                }
                            ),
                            # Submit button (gradient background and rounded corners)
                            html.Button(
                                "Submit",
                                id="chat-submit",
                                n_clicks=0,
                                style={
                                    "background": "linear-gradient(135deg, #F84BAE, #5A73EE)",  # Gradient background
                                    "color": "#ffffff",
                                    "border": "none",
                                    "padding": "10px 20px",
                                    "border-radius": "25px",  # Rounded corners
                                    "cursor": "pointer",
                                    "font-size": "1em",  # Larger font size
                                    "transition": "background-color 0.3s, transform 0.3s",
                                }
                            ),
                        ]
                    )
                ]
            ),

            html.Div(id="chat-response", style={"color": "#fff", "textAlign": "center", "margin-top": "20px", "margin-bottom": "40px"}),

            # Generate Report section
            html.Div(
                style={"position": "fixed", "bottom": "20px", "left": "20px"},
                children=[
                    html.Button(
                        "Generate Report",
                        id="generate-report-btn",
                        style={
                            "background": "linear-gradient(135deg, #F84BAE, #5A73EE)",
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
                        style={
                            "background": "linear-gradient(135deg, #F84BAE, #5A73EE)",
                            "display": "none", "margin-top": "10px"},
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
