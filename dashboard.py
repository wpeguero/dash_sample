"""The Basic Dashboard that Imitates what was written at Green Key Resources."""
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv("ObesityDataSet_raw_and_data_sinthetic.csv")
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
fig1 = px.pie(df, names='Gender', title='Gender')
fig1.update_layout(title_x=0.5)
fig2 = px.histogram(df, x='CALC', y='count', title='Alcohol Frequency', labels={'CALC': 'Alcohol Consumption Frequency', 'count':'People'}, color='CALC')
fig2.update_layout(title_x=0.5)
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='Sample Dashboard From Green Key Resources', style={'textAlign': 'center', 'font':40}),
        html.Div([
        dcc.Graph(figure=fig2, style=style),
        dcc.Graph(figure=fig1, style=style),    
        ]),
        html.Div([
            html.H4(children='Detail', style={'textAlign': 'center'})
        ]),
        dash_table.DataTable(df.to_dict('records'), page_size=10, style_cell={'textAlign': 'center'})
    ], style=style)



if __name__ == "__main__":
    app.run(debug=True)
