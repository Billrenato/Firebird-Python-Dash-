import fdb
from dash import Dash, html, dcc,Input,Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlalchemy_firebird
import sqlalchemy
from sqlalchemy import create_engine
import firebird
import dash_bootstrap_components as dbc





app = Dash(__name__)

engine = create_engine(
    'firebird+fdb://sysdba:masterkey@localhost/C:/GRILITESTE.FDB'
)

conn = engine.connect()


sql1="""select
 case
   when extract(month from vp.dt) in (1) then '01-Janeiro'
   when extract(month from vp.dt) in (2) then '02-Fevereiro'
   when extract(month from vp.dt) in (3) then '03-Março'
   when extract(month from vp.dt) in (4) then '04-Abril'
   when extract(month from vp.dt) in (5) then '05-Maio'
   when extract(month from vp.dt) in (6) then '06-Junho'
   when extract(month from vp.dt) in (7) then '07-Julho'
   when extract(month from vp.dt) in (8) then '08-Agosto'
   when extract(month from vp.dt) in (9) then '09-Setembro'
   when extract(month from vp.dt) in (10) then '10-Outubro'
   when extract(month from vp.dt) in (11) then '11-Novembro'
   when extract(month from vp.dt) in (12) then '12-Dezembro'
 end || '' mes,
 sum(vp.total) TotalPedidos

from vw_pedidovendas vp
where vp.dt between '01.01.2024' and '31.12.2024'  and vp.pedido_orcamento = 'P'
group by  1"""

sql3="""
select
 case
   when extract(month from vp.dt) in (1) then '01-Janeiro'
   when extract(month from vp.dt) in (2) then '02-Fevereiro'
   when extract(month from vp.dt) in (3) then '03-Março'
   when extract(month from vp.dt) in (4) then '04-Abril'
   when extract(month from vp.dt) in (5) then '05-Maio'
   when extract(month from vp.dt) in (6) then '06-Junho'
   when extract(month from vp.dt) in (7) then '07-Julho'
   when extract(month from vp.dt) in (8) then '08-Agosto'
   when extract(month from vp.dt) in (9) then '09-Setembro'
   when extract(month from vp.dt) in (10) then '10-Outubro'
   when extract(month from vp.dt) in (11) then '11-Novembro'
   when extract(month from vp.dt) in (12) then '12-Dezembro'
 end || '' Mes,
 count(vp.pedido_orcamento) vendastotal


from vw_pedidovendas vp
where vp.dt between '01.01.2024' and '31.12.2024' and vp.pedido_orcamento = 'P'
group by 1

"""


sql4 = """select  count(vw_pedidovendas.pedido_orcamento)
from  vw_pedidovendas
where vw_pedidovendas.pedido_orcamento = 'P' and  vw_pedidovendas.dt between '01.01.2024 00:00' and  '31.12.2024 00:00'"""




sql5 = """select sum (vw_pedidovendas.total)
from  vw_pedidovendas
where   vw_pedidovendas.dt between '01.01.2024 00:00' and  '31.12.2024 00:00'"""




sql6 = """select vw_itenspedidovendas.descricao, count(vw_itenspedidovendas.qtd) from vw_itenspedidovendas
inner join vw_pedidovendas on vw_itenspedidovendas.nm = vw_pedidovendas.nm
where vw_pedidovendas.dt between '01.01.2024' and '31.12.2024'
group by vw_itenspedidovendas.descricao, vw_itenspedidovendas.qtd"""



sql7 = """select
 case
     when extract(month from vp.dt) in (1) then '01-Janeiro'
   when extract(month from vp.dt) in (2) then '02-Fevereiro'
   when extract(month from vp.dt) in (3) then '03-Março'
   when extract(month from vp.dt) in (4) then '04-Abril'
   when extract(month from vp.dt) in (5) then '05-Maio'
   when extract(month from vp.dt) in (6) then '06-Junho'
   when extract(month from vp.dt) in (7) then '07-Julho'
   when extract(month from vp.dt) in (8) then '08-Agosto'
   when extract(month from vp.dt) in (9) then '09-Setembro'
   when extract(month from vp.dt) in (10) then '10-Outubro'
   when extract(month from vp.dt) in (11) then '11-Novembro'
   when extract(month from vp.dt) in (12) then '12-Dezembro'
 end || '' MES,
 sum(vp.total) TotalPedidos,
 vp.vendedor_nome

from vw_pedidovendas vp
where vp.dt between '01.01.2024' and '31.12.2024' and vp.pedido_orcamento = 'P'
group by 1,vp.vendedor_nome"""



sql9 = """select sum (vw_pedidovendas.total),vw_pedidovendas.vendedor_nome
from vw_pedidovendas
where   vw_pedidovendas.dt between '01.01.2024 00:00' and  '31.12.2024 00:00'
group by vw_pedidovendas.vendedor_nome
"""





df1 = pd.read_sql_query (sql1,conn)
df3 = pd.read_sql_query (sql3,conn)
df4 = pd.read_sql_query (sql4,conn)
df5 = pd.read_sql_query (sql5,conn)
df6 = pd.read_sql_query (sql6,conn)
df7 = pd.read_sql_query (sql7,conn)
df9 = pd.read_sql_query (sql9,conn)


df4 = df4["COUNT"] = df4["COUNT"].astype(float)
df5 = df5["SUM"] = df5["SUM"].astype(float)
df6=df6.nlargest(n=10, columns=['COUNT'])
df9=df9.nlargest( n=20, columns=['SUM'])
for template in ["plotly_dark"]:
    fig1 = px.line(df1, x='mes',y='totalpedidos',template=template, title="Valor Total dos pedidos por mes:")
    fig3 = px.bar(df3, x='mes',y='vendastotal',template=template, title="Quantidade de pedidos por mes:")
    
    
    fig4 = go.Figure(
         go.Indicator(
        title="Quantidade de vendas em 2024",
        name="$",
        number = {"font":{"size":80},'font_color':'royalblue'},
        mode="number",
        value=float(df4.iloc[0]),
        delta={'position': "top", 'valueformat':'f'}
        
        
     )
    )
    
    fig4.update_layout(


        paper_bgcolor ='black',
        grid={
            'rows': 1,
            'columns': 1,
            'pattern': 'independent'
            }
        )
    

    

    
    fig5 = go.Figure(

    go.Indicator(
        title="Total de vendas em reais 2024",
        name="$",
        number = {"font":{"size":80},'prefix': "$",'font_color':'royalblue'},
        mode="number",
        value=float(df5.iloc[0]),
        delta={'position': "top", 'valueformat':'f'}
        
        
     ))
    fig5.update_layout(


        paper_bgcolor ='black',
        grid={
            'rows': 1,
            'columns': 1,
            'pattern': 'independent'
            }
        )
    
    fig6 = px.bar(df6, x='COUNT',y='descricao',template=template, title="Ranking de produto mais vendido:")
    fig7 = px.bar(df7, x='mes',y='totalpedidos',color='vendedor_nome',template=template, title="Ranking de vendores por mes:")
    fig9 = px.bar(df9, x='vendedor_nome',y='SUM',template=template, title="ranking de vendores por ano:")

    







app.layout = dbc.Container(children=[



    dbc.Row([
        dbc.Col([
            dcc.Graph(figure = fig1)
            
        ])
   
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure = fig4)
            
        ])
   
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure = fig3)
            
        ])
   
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure = fig5)
            
        ])
   
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure = fig6)
            
        ])
   
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure = fig7)
            
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure = fig9)
            
        ])    
        
    ])

])







if __name__ == '__main__':
    app.run(debug=True)
