"""The Basic Dashboard that Imitates what was written at Green Key Resources."""
from dash import Dash, html, dcc, dash_table, Input, Output, callback
import plotly.express as px
import pandas as pd
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv("ObesityDataSet_raw_and_data_sinthetic.csv")
df = df.sample(n=100, random_state=42)
df['count'] = 1


def label_company_size(row):
    """Label the company based on the number of employees."""
    if row['Company Size'] <= 100:
        return 'small business'
    elif 100 < row['Company Size'] <= 1_500:
        return 'medium business'
    elif 1_500 < row['Company Size'] <= 2_000:
        return 'mid-market enterprise'
    elif row['Company Size'] > 2_000:
        return 'large enterprise'

colors = ['orange', 'red', 'green', 'purple']
def color_calc(row):
    """Create color label for calc column."""
    if row['CALC'] == 'no':
        return 'orange'
    elif row['CALC'] == 'Sometimes':
        return 'red'
    elif row['CALC'] == 'Frequently':
        return 'green'
    elif row['CALC'] == 'Always':
        return 'purple'

style = {
        'display': 'inline-block'
        }
df['colors'] = df.apply(color_calc, axis=1)
gender_pie = px.pie(df, names='Gender', title='Gender')
gender_pie.update_layout(title_x=0.5, clickmode='event+select')

fig = px.histogram(df, x='NObeyesdad', y='count', title='Alcohol Frequency', labels={'NObeyesdad': 'Level of Obesity', 'count':'People'}, color='NObeyesdad')
fig.update_layout(title_x=0.5)

fig2 = px.histogram(df, x='NObeyesdad', y='FAF', color='NObeyesdad', labels={'NObeyesdad': 'Level of Obesity', 'FAF':'Physical Activity'})

fig3 = px.density_heatmap(df,x='MTRANS', y='TUE')
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='Sample Dashboard From Green Key Resources', style={'textAlign': 'center', 'font':40}),
        html.Div([
        dcc.Graph(id='filter',figure=gender_pie, style=style),    
        dcc.Graph(id='click-filter', figure=fig, style=style),
        #html.Pre(id='click-filter')
        ]),
        html.Div([
            dcc.Graph(id='click-filter2', figure=fig2, style=style),
            dcc.Graph(figure=fig3, style=style),
        ]),
        html.Div([
            html.H4(children='Detail', style={'textAlign': 'center'})
        ]),
        dash_table.DataTable(df.to_dict('records'), page_size=10, style_cell={'textAlign': 'center'})
    ], style=style)

@callback(
    Output('click-filter', 'figure'),
    Output('click-filter2', 'figure'),
    #Output('click-filter3', 'figure'),
    Input('filter', 'clickData')
)
def filter(clickData):
    #return clickData
    cdata = json.dumps(clickData, indent=2)
    if cdata == 'null':
        fig = px.histogram(df, x='NObeyesdad', y='count', title='Alcohol Frequency', labels={'NObeyesdad': 'Level of Obesity', 'count':'People'}, color='NObeyesdad')
        fig2 = px.histogram(df, x='NObeyesdad', y='FAF', color='NObeyesdad', labels={'NObeyesdad': 'Level of Obesity', 'FAF':'Physical Activity'})
    else:
        cdata = json.loads(cdata)
        value = cdata['points'][0]['label']
        filtered_df = df[df['Gender'] == value]
        fig = px.histogram(filtered_df, x='NObeyesdad', y='count', title='Alcohol Frequency', labels={'NObeyesdad': 'Level of Obesity', 'count':'People'}, color='NObeyesdad')
        fig2 = px.histogram(filtered_df, x='NObeyesdad', y='FAF', color='NObeyesdad', labels={'NObeyesdad': 'Level of Obesity', 'FAF':'Physical Activity'})
    fig.update_layout(title_x=0.5)
    return fig, fig2



if __name__ == "__main__":
    app.run(debug=True)
