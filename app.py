import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64

# Initialize the Dash application
app = dash.Dash(__name__)

# Define external CSS and JavaScript URLs
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
    'styles.css'
]

external_scripts = [
    'https://cdn.jsdelivr.net/npm/chart.js'
]

# Set external CSS and JavaScript
for stylesheet in external_stylesheets:
    app.css.append_css({'external_url': stylesheet})

for script in external_scripts:
    app.scripts.append_script({'external_url': script})

# Define the layout of your Dash app
app.layout = html.Div([
    html.Div(className='container', children=[
        html.Div(className='sidebar neumorphic', children=[
            html.Div(className='logo', children=[
                html.Img(src='logo1.png', alt='Company Logo', width=400, height=300),
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
                html.Table(className='table table-striped', children=[
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
                    html.Tbody(children=[
                        html.Tr([
                            html.Td('1'),
                            html.Td('USA'),
                            html.Td('Canada'),
                            html.Td('10 January, 2024'),
                            html.Td('900'),
                            html.Td('2')
                        ]),
                        html.Tr([
                            html.Td('2'),
                            html.Td('India'),
                            html.Td('Pakistan'),
                            html.Td('15 February, 2024'),
                            html.Td('2000'),
                            html.Td('20')
                        ]),
                        html.Tr([
                            html.Td('3'),
                            html.Td('Brazil'),
                            html.Td('Argentina'),
                            html.Td('25 March, 2024'),
                            html.Td('1600'),
                            html.Td('6')
                        ]),
                        html.Tr([
                            html.Td('4'),
                            html.Td('Japan'),
                            html.Td('China'),
                            html.Td('05 April, 2024'),
                            html.Td('1400'),
                            html.Td('12')
                        ]),
                        html.Tr([
                            html.Td('5'),
                            html.Td('UK'),
                            html.Td('Australia'),
                            html.Td('30 June, 2024'),
                            html.Td('1700'),
                            html.Td('9')
                        ]),
                    ])
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


# Callback to download CSV
@app.callback(
    Output('download-btn', 'n_clicks'),
    Input('download-btn', 'n_clicks')
)
def download_csv(n_clicks):
    if n_clicks:
        csv_string = "S.No,Source,Destination,Week Date,Quantity,SKUs_Count\n" \
                     "1,USA,Canada,10 January, 2024,900,2\n" \
                     "2,India,Pakistan,15 February, 2024,2000,20\n" \
                     "3,Brazil,Argentina,25 March, 2024,1600,6\n" \
                     "4,Japan,China,05 April, 2024,1400,12\n" \
                     "5,UK,Australia,30 June, 2024,1700,9\n"

        csv_data = "data:text/csv;charset=utf-8," + csv_string
        return dcc.send_file(
            csv_data.encode(),
            filename="table_data.csv",
            mimetype='text/csv'
        )


if __name__ == '__main__':
    app.run_server(debug=True)
