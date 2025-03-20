import dash
from dash import dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

df = pd.read_csv('gyroscope_data.csv')
total_samples = len(df)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Gyroscope Data Visualization"),
    
    html.Div([
        html.Label("Select Graph Type:"),
        dcc.Dropdown(
            id='graph-type',
            options=[
                {'label': 'Scatter Plot', 'value': 'scatter'},
                {'label': 'Line Chart', 'value': 'line'},
                {'label': 'Histogram', 'value': 'histogram'},
            ],
            value='scatter'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    
    html.Div([
        html.Label("Select Data Variables:"),
        dcc.Dropdown(
            id='data-variables',
            options=[
                {'label': 'X', 'value': 'x'},
                {'label': 'Y', 'value': 'y'},
                {'label': 'Z', 'value': 'z'},
                {'label': 'All', 'value': 'all'}
            ],
            value=['all'],
            multi=True
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    
    html.Div([
        html.Label("Number of Samples to Display:"),
        dcc.Input(
            id='num-samples',
            type='number',
            value=100,  
            min=1,
            max=total_samples,
            step=1
        )
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    
    html.Div([
        html.Button("Previous", id='prev-button', n_clicks=0),
        html.Button("Next", id='next-button', n_clicks=0)
    ], style={'padding': '10px'}),
    
    dcc.Graph(id='gyroscope-graph'),
    
    html.H2("Summary Statistics"),
    dash_table.DataTable(
        id='data-summary',
        columns=[
            {"name": "Variable", "id": "Variable"},
            {"name": "Mean", "id": "Mean"},
            {"name": "Std", "id": "Std"},
            {"name": "Min", "id": "Min"},
            {"name": "Max", "id": "Max"}
        ],
        data=[],
        style_table={'width': '50%'}
    ),
    
    dcc.Store(id='start-index', data=0)
])

@app.callback(
    [Output('gyroscope-graph', 'figure'),
     Output('data-summary', 'data'),
     Output('start-index', 'data')],
    [Input('graph-type', 'value'),
     Input('data-variables', 'value'),
     Input('num-samples', 'value'),
     Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')],
    [State('start-index', 'data')]
)
def update_visualization(graph_type, data_vars, num_samples, prev_clicks, next_clicks, start_index):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    if triggered_id == 'prev-button':
        start_index = max(0, start_index - num_samples)
    elif triggered_id == 'next-button':
        start_index = min(total_samples - num_samples, start_index + num_samples)

    end_index = start_index + num_samples
    df_subset = df.iloc[start_index:end_index]

    if 'all' in data_vars or not data_vars:
        selected_cols = ['x', 'y', 'z']
    else:
        selected_cols = data_vars

    if graph_type == 'scatter':
        fig = px.scatter(df_subset, y=selected_cols, title="Scatter Plot")
    elif graph_type == 'line':
        fig = px.line(df_subset, y=selected_cols, title="Line Chart")
    elif graph_type == 'histogram':
        fig = px.histogram(df_subset, x=selected_cols[0], title="Histogram")
    else:
        fig = px.scatter(df_subset, y=selected_cols, title="Scatter Plot")

    summary_df = df_subset[selected_cols].describe().loc[['mean', 'std', 'min', 'max']].transpose().reset_index()
    summary_df.columns = ['Variable', 'Mean', 'Std', 'Min', 'Max']
    summary_data = summary_df.to_dict('records')

    return fig, summary_data, start_index

if __name__ == '__main__':
    app.run_server(debug=True)
