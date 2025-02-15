
from dash import Input, Output, State, dcc
import pandas as pd
from api import generate_gemini_response
from reports import generate_pdf

def register_callbacks(app, relaxed_df, stressed_df, active_df):
    @app.callback(
        [Output('chat-response', 'children'),
         Output('chat-input', 'value')],
        [Input('chat-submit', 'n_clicks')],
        [State('chat-input', 'value')]
    )
    def chat_response(n_clicks, user_input):
        if n_clicks and user_input:
            response = generate_gemini_response(user_input)
            return response, ""
        return "", ""

    @app.callback(
        [Output('frequency-bar-chart', 'figure'),
         Output('frequency-pie-chart', 'figure')],
        [Input('state-selector', 'value')]
    )
    def update_charts(selected_state):
        if selected_state == "Relaxed":
            df = relaxed_df
        elif selected_state == "Stressed":
            df = stressed_df
        else:
            df = active_df

        from charts import create_bar_figure, create_pie_figure
        return create_bar_figure(df, f'Frequency Bands ({selected_state} State)'), \
               create_pie_figure(df, f'Distribution of Frequency Bands ({selected_state} State)')

    @app.callback(
        Output("pdf-download", "data"),
        [Input("download-pdf-btn", "n_clicks")],
        [State("user-name", "value"),
         State("user-age", "value")]
    )
    def download_pdf(n_clicks, name, age):
        if n_clicks:
            pdf_buffer = generate_pdf(name, age, relaxed_df.iloc[0], stressed_df.iloc[0], active_df.iloc[0])
            return dcc.send_bytes(pdf_buffer.getvalue(), filename="EEG_Report.pdf")
        return None
