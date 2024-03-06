import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dark mode toggle switch
dark_mode_switch = dbc.Switch(
    id="dark-mode-toggle",
    label="Dark Mode",
    className="me-2",
    style={"display": "flex"},
)

# Navigation bar
navbar = dbc.Navbar(
    children=[
        dbc.NavbarBrand("Fujairah Research Centre", href="https://www.frc.ae"),
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
                dbc.NavItem(dbc.NavLink("About Us", href="/about")),
                dbc.NavItem(dbc.NavLink("Contact", href="/contact")),
            ],
            className="mr-auto",  # Aligns the nav items to the left
        ),
        dbc.Nav(
            [dark_mode_switch],
            className="ml-auto",  # Aligns the dark mode switch to the right
        ),
    ],
    color="primary",
    dark=True,
    sticky="top",
    className="fade-in",
)

# Footer
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
    style={'backgroundColor': '#AAB7B8', 'padding': '1rem', 'width': '100%', 'text-align': 'center', 'marginTop': '30px', 'position': 'relative'},
    className="fade-in",  # And here
)

# Dropdown for file selection allowing multiple selections
dropdown = dcc.Dropdown(
    id='file-selector',
    options=[
        {'label': 'Camel 1', 'value': 'camel1.csv'},
        {'label': 'Camel 2', 'value': 'camel2.csv'},
        {'label': 'Camel 3', 'value': 'camel3.csv'}
    ],
    value=['camel1.csv'],  # Default value
    multi=True,  # Allow multiple selections
    style={'width': '50%', 'margin': '10px auto'}
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dropdown,
    html.Div(id='page-content'),
    html.Div(style={'padding': '30px'}),
    footer
], id='main-content')

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'), Input('file-selector', 'value')]
)
def display_page(pathname, selected_files):
    if pathname == '/about':
        return html.Div([
            html.H1('Our Mission', style={'textAlign': 'center'}),
            html.P('To be recognized as an innovative and socially driven world-class Research Centre striving to support the economic transformation in Fujairah, UAE, and other tropical and desert regions worldwide.',
                style={
                    'textAlign': 'center',
                    'marginTop': '50px',
                    'marginBottom': '50px',
                    'fontSize': '20px',
                    'fontWeight': 'normal',
                    'color': '#505050',
                    'maxWidth': '800px',
                    'marginLeft': 'auto',
                    'marginRight': 'auto',
                    'lineHeight': '1.6',
                }),
            html.H1('Our Vision', style={'textAlign': 'center'}),
            html.P('To achieve a sustainable economy in Fujairah through cutting-edge innovative research for Efficient, safe, and sustainable use of natural resources. Strengthening regional agriculture, sustainable and fisheries. Promoting local employment opportunities. Addressing the challenges relating to environment, marine life conservation, ecosystem preservation, food security, and desert agriculture.',
                style={
                    'textAlign': 'center',
                    'marginTop': '50px',
                    'marginBottom': '50px',
                    'fontSize': '20px',
                    'fontWeight': 'normal',
                    'color': '#505050',
                    'maxWidth': '800px',
                    'marginLeft': 'auto',
                    'marginRight': 'auto',
                    'lineHeight': '1.6',
                }),
            html.Img(src="/Users/simon/Desktop/Builds/Dashy/camel.png", 
                style={
                    'display': 'block',
                    'marginLeft': 'auto',
                    'marginRight': 'auto',
                    'width': '50%',  
                    'marginTop': '20px',  
                    'marginBottom': '50px',  
                })
        ], style={'textAlign': 'center'})
    elif pathname == '/contact':
        return html.Div([
            html.H1('Contact Us', style={'textAlign': 'center', 'marginTop': '20px'}),
            html.Div([
                html.P('PHONE: +971 92222411', style={'textAlign': 'center', 'margin': '10px 0'}),
                html.P('E-MAIL: info@frc.ae', style={'textAlign': 'center', 'margin': '10px 0'}),
                html.P('Location: Sakamkam, Fujairah, UAE', style={'textAlign': 'center', 'margin': '10px 0'}),
            ], style={'width': '100%', 'maxWidth': '600px', 'margin': '0 auto', 'padding': '20px', 
                    'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)', 'transition': '0.3s', 
                    'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
        ], style={'width': '100%', 'maxWidth': '600px', 'margin': '0 auto'})
    elif pathname == '/':
        # Assuming all files have "Time", "Speed", and "Acceleration" columns
        parameters = ['Speed', 'Acceleration']  # Focused parameters

        # Create a subplot layout with 1 row and 2 columns for side by side display
        fig = make_subplots(rows=1, cols=2, shared_yaxes=True)

        # Dictionary to store average speed and acceleration
        averages = {}

        for selected_file in selected_files:
            file_path = f'/Users/simon/Desktop/Builds/Dashy/{selected_file}'  # Adjust to your file path
            data = pd.read_csv(file_path)
            data['Time'] = pd.to_datetime(data['Time'], errors='coerce')  # Ensuring Time is datetime

            for i, parameter in enumerate(parameters, start=1):
                fig.add_trace(
                    go.Scatter(x=data['Time'], y=data[parameter], mode='lines+markers', name=f'{selected_file} - {parameter}'),
                    row=1, col=i
                )
                # Calculate and store averages
                if selected_file not in averages:
                    averages[selected_file] = {}
                averages[selected_file][parameter] = data[parameter].mean()

        # Calculate rankings based on average speed and acceleration
        rankings = sorted(averages.items(), key=lambda x: (x[1]['Speed'] + x[1]['Acceleration']), reverse=True)

        # Extract camel ID from file name and use it for ranking display
        ranking_cards = dbc.Row(
            [dbc.Col(dbc.Card([
                dbc.CardHeader(f"Rank {index + 1}:  {rank[0].replace('', '').replace('.csv', '')}"),  # Adjusted to display Camel ID
                dbc.CardBody([
                    html.H5(f"Speed: {rank[1]['Speed']:.2f}", className="card-title"),
                    html.H5(f"Acceleration: {rank[1]['Acceleration']:.2f}", className="card-title")
                ])
            ], color="light", outline=True), width=4) for index, rank in enumerate(rankings)],
            className="mb-4", justify="center"
        )

        # Update the figure layout
        fig.update_layout(
            height=800, 
            width=1600, 
            hovermode='x unified',
            margin=dict(l=0, r=0, t=0, b=0),  # Adjust margins to 0 to help centering
            xaxis=dict(
                title_text="Time",  # Apply title settings directly to xaxis and yaxis
                showline=True,  # Optional: if you want to show lines for the axis
                mirror=True  # Optional: if you want the axis lines to mirror
            ),
            yaxis=dict(
                title_text="Value",
                automargin=True,
                showline=True,  # Optional: if you want to show lines for the axis
                mirror=True  # Optional: if you want the axis lines to mirror
            )
        )

        # Return both the graph and the ranking cards, wrapped in a container for centering
        return html.Div(
            [
                dcc.Graph(figure=fig, style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}),
                dbc.Container(ranking_cards, fluid=True, style={'textAlign': 'center'})
            ],
            style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}
        )
    else:
        # Handle other paths as before or return a '404' message
        return '404'

@app.callback(
    Output('main-content', 'className'),
    [Input('dark-mode-toggle', 'value')]
)
def toggle_dark_mode(toggle_value):
    if toggle_value:
        return "dark-mode"
    else:
        return "light-mode"

if __name__ == '__main__':
    app.run_server(debug=True)
