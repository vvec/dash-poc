# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import dash_ag_grid as dag

import pandas as pd
import plotly.express as px
import os

# Incorporate data
print(os.getcwd())
df = pd.read_csv(r'test-data\test_data.csv')
column_names = [{"field": i} for i in df.columns]
control_options = [i for i in df.columns]
control_options.pop(0)

# Initialize the app
app = Dash(__name__)


# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data and a Graph'),
    dag.AgGrid(id="get-started-example-basic", rowData=df.to_dict("records"), columnDefs= column_names),
    html.Hr(),
    dcc.RadioItems(options=control_options, value=control_options[0], id='controls-and-radio-item'),
    dcc.Graph(figure={}, id='controls-and-graph'),
    dcc.Graph(figure=px.bar(df, x='date', y=control_options, barmode='group'))
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.bar(df, x='date', y=col_chosen)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
