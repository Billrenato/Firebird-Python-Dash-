import fdb
from dash import Dash, html, dcc,Input,Output
import plotly.express as px
import pandas as pd
import sqlalchemy_firebird
import sqlalchemy
from sqlalchemy import create_engine
import firebird


app = Dash(__name__)

engine = create_engine(
    'firebird+fdb://sysdba:masterkey@localhost/C:/GRILITESTE.FDB'
)

conn = engine.connect()

sql = """
SELECT vw_pedidovendas.dt,vw_itenspedidovendas.descricao,vw_itenspedidovendas.qtd
FROM vw_itenspedidovendas
inner join vw_pedidovendas on vw_itenspedidovendas.nm = vw_pedidovendas.nm
where vw_pedidovendas.dt between '21.07.2024 00:00' and '30.07.2024 00:00'
group by vw_pedidovendas.dt ,vw_itenspedidovendas.descricao, vw_itenspedidovendas.qtd
"""


df = pd.read_sql_query (sql,conn)
df.groupby('descricao').mean()

fig = px.bar(df, x='descricao',y='qtd',color='dt')


app.layout = html.Div(children=[
    html.H1(children=''),

    html.Div(children='''
        
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])






if __name__ == '__main__':
    app.run(debug=True)






