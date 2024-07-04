import dash
from dash import dcc, html, Input, Output
import pandas as pd
import base64

# Initialize the Dash application
app = dash.Dash(__name__)

# Define external CSS and JavaScript URLs
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
    '/static/style.css'  # Adjust the path to where your style.css is hosted
]

# Set external CSS
for sheet in external_stylesheets:
    app.css.append_css({'external_url': sheet})

# Load CSV data
df = pd.read_csv('data.csv')  # Update with your CSV file path

# Define pagination parameters
PAGE_SIZE = 5

# Define the layout of your Dash app
app.layout = html.Div([
    html.Div(className='container', children=[
        html.Div(className='sidebar neumorphic', children=[
            html.Div(className='logo', children=[
                html.Img(src='/assets/logo1.png', alt='Company Logo', width=400, height=300),
                html.H2('NPS')
            ]),
            html.Ul(children=[
                html.Li(html.A(html.I(className='fas fa-network-wired'), ' Network Plan')),
                html.Li(html.A(html.I(className='fas fa-project-diagram'), ' Demand Flow')),
                html.Li(html.A(html.I(className='fas fa-chart-line'), ' Performance Report')),
            ])
        ]),
        html.Div(className='content', children=[
            html.Div(className='heading', children='Network Planning System'),
            html.Div(className='dropdowns', children=[
                dcc.Dropdown(id='selected-option-1', className='dropdown', options=[
                    {'label': 'Select a vendor', 'value': ''},
                    {'label': 'Vendor 1', 'value': 'Vendor 1'},
                    {'label': 'Vendor 2', 'value': 'Vendor 2'},
                    {'label': 'Vendor 3', 'value': 'Vendor 3'},
                ], value=''),
                dcc.Dropdown(id='selected-option-2', className='dropdown', options=[
                    {'label': 'Select a family code', 'value': ''},
                    {'label': 'Code 1', 'value': 'Code 1'},
                    {'label': 'Code 2', 'value': 'Code 2'},
                    {'label': 'Code 3', 'value': 'Code 3'},
                ], value=''),
                dcc.Dropdown(id='selected-option-3', className='dropdown', options=[
                    {'label': 'Select a site', 'value': ''},
                    {'label': 'Site 1', 'value': 'Site 1'},
                    {'label': 'Site 2', 'value': 'Site 2'},
                    {'label': 'Site 3', 'value': 'Site 3'},
                ], value='')
            ]),
            html.Div(className='tabs', children=[
                html.Div(className='tab', children='Summary'),
                html.Div(className='tab', children='Transfers')
            ]),
            html.Div(className='table-container neumorphic', children=[
                html.Table(className='table table-striped', id='datatable', children=[
                    html.Thead(children=[
                        html.Tr([
                            html.Th('S.No'),
                            html.Th('Source'),
                            html.Th('Destination'),
                            html.Th('Week Date'),
                            html.Th('Quantity'),
                            html.Th('SKUs_Count')
                        ])
                    ]),
                    html.Tbody(id='table-body')
                ]),
                html.Div(id='datatable-container', children=[
                    dcc.Input(id='datatable-filter', type='text', placeholder='Filter table data...'),
                    dcc.RadioItems(
                        id='datatable-pagination-mode',
                        options=[
                            {'label': 'Display all rows', 'value': 'all'},
                            {'label': 'Paginate rows', 'value': 'paginate'}
                        ],
                        value='paginate',
                        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                    ),
                    dcc.Dropdown(
                        id='datatable-pagination-dropdown',
                        options=[
                            {'label': str(i), 'value': str(i)}
                            for i in [5, 10, 15, 20]
                        ],
                        value='5',
                        clearable=False,
                        style={'width': '90px'}
                    ),
                    html.Div(id='datatable-pagination')
                ]),
                html.Button('Download', className='download-btn', id='download-btn')
            ]),
            html.Div(className='chart-container neumorphic', children=[
                dcc.Graph(id='myLineChart')
            ]),
            html.Div(className='date-bar', children=[
                dcc.Input(type='text', placeholder='Date (MM/DD/YY)', className='date-input'),
                html.Button('Generate', className='generate-button', id='generate-button')
            ])
        ])
    ])
])


# Callback to update the table based on filter and pagination
@app.callback(
    Output('table-body', 'children'),
    Output('datatable-pagination', 'children'),
    Input('datatable-filter', 'value'),
    Input('datatable-pagination-mode', 'value'),
    Input('datatable-pagination-dropdown', 'value')
)
def update_table(filter_value, mode, page_size):
    if filter_value is None:
        filtered_df = df
    else:
        filtered_df = df[df.apply(lambda row: filter_value in row.values, axis=1)]

    if mode == 'paginate':
        pagination = html.Div([
            html.P(f'Displaying {min(len(filtered_df), int(page_size))} of {len(filtered_df)} entries')
        ])
        return filtered_df.iloc[0:int(page_size)].apply(
            lambda row: html.Tr([html.Td(cell) for cell in row]), axis=1
        ), pagination
    else:
        return filtered_df.apply(
            lambda row: html.Tr([html.Td(cell) for cell in row]), axis=1
        ), None


# Callback to update the chart based on dropdown selection
@app.callback(
    Output('myLineChart', 'figure'),
    Input('selected-option-1', 'value'),
    Input('selected-option-2', 'value'),
    Input('selected-option-3', 'value')
)
def update_chart(selected_vendor, selected_code, selected_site):
    # Dummy data for demonstration
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October']
    data = [65, 59, 80, 81, 56, 55, 40, 75, 60, 70]

    return {
        'data': [{
            'x': labels,
            'y': data,
            'type': 'line',
            'marker': {'color': 'blue'},
        }],
        'layout': {
            'title': 'Dash Data Visualization',
            'xaxis': {'title': 'Month'},
            'yaxis': {'title': 'Value'},
            'plot_bgcolor': '#f5f5f5',
            'paper_bgcolor': '#f5f5f5',
            'font': {'color': 'black'}
        }
    }


# Run the Dash Application
if __name__ == '__main__':
    app.run_server(debug=True)
