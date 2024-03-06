import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# URLs for Bootstrap themes
THEMES = {
    "light": dbc.themes.BOOTSTRAP,
    "dark": dbc.themes.DARKLY,
}

app = dash.Dash(__name__, external_stylesheets=[THEMES["light"]])

# Navigation bar with theme toggler
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
        dbc.NavItem(dbc.NavLink("About Us", href="/about")),
        dbc.NavItem(dbc.NavLink("Contact", href="/contact")),
        dbc.Button("Toggle Theme", id="theme-toggler", n_clicks=0),
    ],
    brand="Fujairah Research Centre",
    brand_href="https://www.frc.ae",
    color="primary",
    dark=True,
    sticky="top",
)

# Footer adjusted to be part of the document flow
footer = html.Footer(
    children=[
        dbc.Container([
            html.P("© 2024 All Rights Reserved Fujairah Research Centre"),
            html.P("PHONE: +971 92222411"),
            html.P("E-MAIL: info@frc.ae"),
            html.P("Location: Sakamkam, Fujairah, UAE"),
            html.A("Visit our website", href="https://frc.ae", target="_blank"),
        ], fluid=True),
    ],
    style={'backgroundColor': '#AAB7B8', 'padding': '1rem', 'text-align': 'center', 'marginTop': '2rem'}
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dcc.Dropdown(
        id='file-selector',
        options=[
            {'label': 'Camel 1', 'value': 'final.csv'},
            {'label': 'Camel 2', 'value': 'final1.csv'},
            {'label': 'Camel 3', 'value': 'final2.csv'}
        ],
        value=['final1.csv'],  # Default value
        multi=True,  # Allow multiple selections
        style={'width': '50%', 'margin': '10px auto'}
    ),
    html.Div(id='page-content'),
    footer
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'), Input('file-selector', 'value')]
)
# def display_page(pathname, selected_files):
#     # Page content rendering logic remains the same
#     pass  # Replace with the existing display_page function's body
def display_page(pathname, selected_files):
    if pathname == '/':
        # Assuming all files have "Time", "Speed", and "Acceleration" columns
        parameters = ['Speed', 'Acceleration']  # Focused parameters

        # Create a subplot for each parameter (Speed, Acceleration)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=[f'Time vs. {param}' for param in parameters])

        for selected_file in selected_files:
            file_path = f'/Users/simon/Desktop/Builds/Dashy/{selected_file}'  # Adjust to your file path
            data = pd.read_csv(file_path)
            data['Time'] = pd.to_datetime(data['Time'], errors='coerce')  # Ensuring Time is datetime

            for i, parameter in enumerate(parameters, start=1):
                fig.add_trace(
                    go.Scatter(x=data['Time'], y=data[parameter], mode='lines+markers', name=f'{selected_file} - {parameter}'),
                    row=i, col=1
                )

        # Update the figure layout
        fig.update_layout(height=1600, width=1000, title_text="Comparison of Camels: Speed and Acceleration", hovermode='x unified')
        fig.update_xaxes(title_text="Time")
        fig.update_yaxes(title_text="Value", automargin=True)

        return dcc.Graph(figure=fig)
    else:
        # Handle other paths as before or return a '404' message
        return '404'

@app.callback(
    [Output('app', 'external_stylesheets'), Output('theme-toggler', 'children')],
    [Input('theme-toggler', 'n_clicks')],
    [State('app', 'external_stylesheets')]
)
def toggle_theme(n, current_stylesheet):
    if n % 2 == 0:  # If even, light theme; if odd, dark theme
        theme, button_label = "light", "Switch to Dark Theme"
    else:
        theme, button_label = "dark", "Switch to Light Theme"
    return [THEMES[theme]], button_label

if __name__ == '__main__':
    app.run_server(debug=True)
