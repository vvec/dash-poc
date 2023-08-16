# Import packages
from dash import Dash, html, callback, Output, Input, ALL, ctx
from dash import dcc as dCore
import dash_ag_grid as dAGrid
import dash_bootstrap_components as dBoot
import pandas as pd
import plotly.express as px
from jinja2 import Environment, FileSystemLoader
import os

# Incorporate data
print(os.getcwd())
df = pd.read_csv(r'..\test-data\test_data.csv')
column_names = [{"field": i} for i in df.columns]
control_options = [i for i in df.columns]
control_options.pop(0)

# Get email template
environment = Environment(loader=FileSystemLoader(r'..\test-data\\'))
environment.trim_blocks = True
environment.lstrip_blocks = True
htmlTemplate = environment.get_template('vvec-recall-2023-q1.html')
recall = { 'greeting': 'recall.name', 'prior_visit':'recall.last_visit_date'}

# Initialize the app
app = Dash(__name__,external_stylesheets=[dBoot.themes.SLATE])

the_list = dBoot.ListGroup(
    [
        dBoot.ListGroupItem(
            item,
            id={"type":"list-group-item", "index":index},
            action=True
        )
        for index,item in enumerate(control_options)
    ],
    id='list_group'
)
the_table = dAGrid.AgGrid(id="get-started-example-basic", rowData=df.to_dict("records"), columnDefs= column_names) 
the_controls = dCore.RadioItems(options=control_options, value=control_options[0], id='controls-and-radio-item')

the_detail = dCore.Graph(figure={}, id='detail_chart')
the_summary = dCore.Graph(figure=px.bar(df, x='date', y=control_options, barmode='group'), id='side-by-side-bar-graph')


# App layout
app.layout = html.Div(
    id="container", 
    className="text-center bg-body p-2", 
    children=[ 
        dBoot.Row(html.H1('Title String')),
        dBoot.Row(
            [
                dBoot.Col(
                    html.Div(
                        id="summary_area", 
                        className="text-center bg-body-secondary m-2", 
                        children=[the_summary]
                    ), 
                    width=12  
                )
            ]
        ),
        dBoot.Row(
            [
                dBoot.Col(
                    html.Div(
                        id="main_control_area", 
                        className="text-center bg-body-warning p-0", 
                        children=[the_list]
                    ), 
                    width=2  
                ),
                dBoot.Col(
                    html.Div(
                        id="work_area", 
                        className="text-center bg-body-danger p-0", 
                        children=[ 
                            dBoot.Row(
                                [
                                    dBoot.Col(
                                        html.Div(
                                            id="detail_control_area", 
                                            className="text-center bg-body-warning m-4", 
                                            children=[the_controls]
                                        ), 
                                        width=3
                                    ),
                                    dBoot.Col(html.Iframe(
                                            id='recall_preview',
                                            srcDoc=htmlTemplate.render(greeting='recall.greeting', priorVisit='recall.prior_visit'),
                                            style={"overflow":"hidden", "height":"320px", "width":"100%"}
                                        ),
                                        width=9
                                    )
                                ]
                            ),
                            dBoot.Row(
                                dBoot.Col(
                                    html.Div(
                                        id="table_area", 
                                        className="text-center bg-body-tertiary p-2", 
                                        children=[the_table]
                                    )
                                )
                            )
                        ]       
                    ),
                    width=10
                )
            ]
        ),
        # dCore.Graph(figure={}, id='controls-and-graph')
    ]
)

# Add controls to build the interaction
@callback(
    Output(component_id='recall_preview', component_property='srcDoc'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    frame = htmlTemplate.render(greeting=col_chosen, priorVisit='recall.prior_visit')
    return frame

@callback(
    Output("main_control_area", "children"),
    Input({'type': 'list-group-item', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def update(_):    
    return f"Clicked on Item {ctx.triggered_id.index}"
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
