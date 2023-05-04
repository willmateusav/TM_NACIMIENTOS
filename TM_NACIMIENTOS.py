import base64
import string
import os
import folium
import json
import requests
import dash
import dash_html_components as html
import dash_core_components as dcc
from branca.colormap import linear
from folium import FeatureGroup, LayerControl, Map, Marker

from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
import plotly.express as px # install plotly version 4.1.1
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Call the data to the map
Nacimientos = pd.read_csv('Nac_2016.csv')
Nacimientos2 = pd.read_csv('Nac_2017.csv')
Nacimientos1 = pd.read_csv('Nac_2018.csv')
PeSo = pd.read_csv('Peso_2016.csv')
PeSo1 = pd.read_csv('Peso_2017.csv')
PeSo2 = pd.read_csv('Peso_2018.csv')
RH = pd.read_csv('RH_2016.csv')
RH1 = pd.read_csv('RH_2017.csv')
RH2 = pd.read_csv('RH_2018.csv')
time = pd.read_csv('tiempo.csv')
time1 = pd.read_csv('tiempo1.csv')
TAS = pd.read_csv('Tasa.csv')


# create the figure SEXO
fig = go.Figure(data=[
    go.Bar(name='Masculino', x=[2016, 2017, 2018], y=[332824, 336576, 332740]),
    go.Bar(name='Femenino', x=[2016, 2017, 2018], y=[314617, 320035, 316303]),
    go.Bar(name='Indeterminado', x=[2016, 2017, 2018], y=[80, 93, 72])
])

# Change the bar mode
fig.update_layout(title_text='Género de los nacientes por año', titlefont = {'color': 'black'}, title_x=0.5, #barmode='group',
 paper_bgcolor='rgba(0, 0, 0, 0)',plot_bgcolor='rgba(0, 0, 0, 0)', template='plotly_white')

# create the PIE figure
fig2 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

fig2.add_trace(go.Pie(labels=PeSo['NOM'], values=PeSo['COUNT_PESO'], name="Año 2016"), 1, 1)
fig2.add_trace(go.Pie(labels=PeSo1['NOM'], values=PeSo1['COUNT_PESO'], name="Año 2017"), 1, 2)
fig2.add_trace(go.Pie(labels=PeSo2['NOM'], values=PeSo2['COUNT_PESO'], name="Año 2018"), 1, 3)
fig2.update_layout(title_text="Distribución porcentual del peso de los nacientes por año",  titlefont = {'color': 'black'},
                   paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', template='plotly_white', title_x=0.5 )

# create the PIE figure

fig3 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

fig3.add_trace(go.Pie(labels=RH['RH'], values=RH['Conteo_RH'], name="Año 2016"), 1, 1)
fig3.add_trace(go.Pie(labels=RH1['RH'], values=RH1['Conteo_RH'], name="Año 2017"), 1, 2)
fig3.add_trace(go.Pie(labels=RH2['RH'], values=RH2['Conteo_RH'], name="Año 2018"), 1, 3)
fig3.update_layout(title_text="Distribución de los grupos sanguíneos de los nacientes por año",  titlefont = {'color': 'black'},
                   paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', template='plotly_white', title_x=0.5,
                   annotations=[dict(text='Grupo sanguíneo', x=0.095, y=0.5, font_size=12, showarrow=False),
                   dict(text='Grupo sanguíneo', x=0.499, y=0.5, font_size=12, showarrow=False),
                   dict(text='Grupo sanguíneo', x=0.905, y=0.5, font_size=12, showarrow=False)])

fig3.update_traces(hole=.4, hoverinfo="label+value+name")

# create the TIME figure
fig4 = go.Figure([go.Scatter(x=time['Tiempo'], y=time['Cantidad'], line = dict(width=3))])
fig4.update_layout(title_text="Serie de tiempo del número de nacimientos por mes", xaxis = {'showgrid': True}, yaxis = {'showgrid': False}, titlefont = {'color': 'black'}, paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', template='plotly_white', title_x=0.5)

## Add shape regions ##
fig4.update_layout(
    shapes=[
        # 1st highlight during Jun-2016 and Sep-2016
        dict(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            # y-reference is assigned to the plot paper [0,1]
            yref="paper",
            x0="Jun-2016",
            y0=0,
            x1="Sep-2016",
            y1=1,
            fillcolor="LightSalmon", # "PaleTurquoise"
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
        # 2nd highlight during Jun-2017 and Sep-2017
        dict(
            type="rect",
            xref="x",
            yref="paper",
            x0="Jun-2017",
            y0=0,
            x1="Sep-2017",
            y1=1,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
        # 3dr highlight during Jun-2018 and Sep-2018
        dict(
            type="rect",
            xref="x",
            yref="paper",
            x0="Jun-2018",
            y0=0,
            x1="Sep-2018",
            y1=1,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
        # 1st highlight during Feb-2016 and Jun-2016
        dict(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            # y-reference is assigned to the plot paper [0,1]
            yref="paper",
            x0="Feb-2016",
            y0=0,
            x1="Jun-2016",
            y1=1,
            fillcolor="LightSeaGreen",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
        # 2nd highlight during Feb-2017 and Jun-2017
        dict(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            # y-reference is assigned to the plot paper [0,1]
            yref="paper",
            x0="Feb-2017",
            y0=0,
            x1="Jun-2017",
            y1=1,
            fillcolor="LightSeaGreen",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
        # 3dr highlight during Feb-2018 and Jun-2018
        dict(
            type="rect",
            xref="x",
            yref="paper",
            x0="Feb-2018",
            y0=0,
            x1="Jun-2018",
            y1=1,
            fillcolor="LightSeaGreen",
            opacity=0.5,
            layer="below",
            line_width=0,
        )
    ]
)
## create the TIME figure ##

## Create the forecast time figure ##

fig6 = go.Figure()
# Create and style traces
fig6.add_trace(go.Scatter(x=time['Tiempo'], y=time['Cantidad'], line=dict(width=3), name='Nacimientos 2016-2019'))
fig6.add_trace(go.Scatter(x=time1['Tiempo'], y=time1['Cantidad'],line=dict(color='firebrick', width=3, dash='dash'), name='Pronóstico 2019'))

fig6.update_layout(title_text="Serie de tiempo de nacimientos y su pronóstico para el 2019",  titlefont = {'color': 'black'}, paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', template='plotly_white', title_x=0.5)

## Create the forecast time figure ##

# create the rate figure
fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=TAS['MES'], y=TAS['Tasa1'],
                    mode='lines',
                    name='Tasa de crecimiento 2016 a 2017'))
fig5.add_trace(go.Scatter(x=TAS['MES'], y=TAS['Tasa2'],
                    mode='lines',
                    name='Tasa de crecimiento 2017 a 2018'))
fig5.update_layout(title_text="Tasa de variación por mes",  titlefont = {'color': 'black'}, paper_bgcolor='rgba(0, 0, 0, 0)', plot_bgcolor='rgba(0, 0, 0, 0)', template='plotly_white', title_x=0.5)
# create the rate figure

# create empty map zoomed in on Colombia ######################################################################################################
# Call the data to the map
NacimientoS = pd.read_csv('year.csv')

A16 = NacimientoS[NacimientoS["year"]==2016]
A17 = NacimientoS[NacimientoS["year"]==2017]
A18 = NacimientoS[NacimientoS["year"]==2018]

# create empty map zoomed in on Colombia
COL_COORDINATES = (4.570868, -74.2973328)
map = folium.Map(location=COL_COORDINATES, zoom_start=6, tiles=None, overlay=False)

# add label over the json data
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.10, 
                                'weight': 0.3}

#folium.TileLayer('cartodbpositron', name='my tilelayer').add_to(map)
# feature groups
feature_group0 = folium.FeatureGroup(name='Año 2016',overlay=False).add_to(map)
feature_group1 = folium.FeatureGroup(name='Año 2017',overlay=False).add_to(map)
feature_group2 = folium.FeatureGroup(name='Año 2018',overlay=False).add_to(map)

fs = [feature_group0, feature_group1, feature_group2]
commodities = [A16, A17, A18]

for i in range(len(commodities)): 
    if i == 0:
       choropleth1 = folium.Choropleth('colombiageo.json',
                                     name='choropleth',
                                     data=commodities[i],
                                     columns=['NOMBRE_DPT', 'Conteo_Nacimientos'],
                                     key_on='feature.properties.NOMBRE_DPT',
                                     fill_color='OrRd',#'BuPu',#'YlGn',
                                     fill_opacity=0.9,
                                     line_opacity=0.3,
                                     legend_name='Cantidad de nacimientos',
                                     highlight=True,
                                     line_color='black').geojson.add_to(fs[i])
       NIL = folium.features.GeoJson(
                                     'colombiageo.json',
                                     style_function=style_function, 
                                     control=False,
                                     highlight_function=highlight_function, 
                                     tooltip=folium.features.GeoJsonTooltip(
                                     fields=['NOMBRE_DPT', 'Conteo_Nacimientos'],
                                     aliases=['Departamento: ', 'Número de nacimientos:'],
                                     style=('background-color: grey; color: white;')
                                                                           )
                                    ).add_to(choropleth1)
    elif i == 1:
         choropleth2 = folium.Choropleth('colombiageo.json',
                                     name='choropleth',
                                     data=commodities[i],
                                     columns=['NOMBRE_DPT', 'Conteo_Nacimientos'],
                                     key_on='feature.properties.NOMBRE_DPT',
                                     fill_color='OrRd',#'BuPu',#'YlGn',
                                     fill_opacity=0.9,
                                     line_opacity=0.3,
                                     legend_name='Cantidad de nacimientos',
                                     highlight=True,
                                     line_color='black').geojson.add_to(fs[i])
         NIL1 = folium.features.GeoJson(
                                     'colombiageo.json',
                                     style_function=style_function, 
                                     control=False,
                                     highlight_function=highlight_function, 
                                     tooltip=folium.features.GeoJsonTooltip(
                                     fields=['NOMBRE_DPT', 'Conteo_Nacimientos1'],
                                     aliases=['Departamento: ', 'Número de nacimientos:'],
                                     style=('background-color: grey; color: white;')
                                                                           )
                                    ).add_to(choropleth2)
    elif i == 2:
         choropleth3 = folium.Choropleth('colombiageo.json',
                                     name='choropleth',
                                     data=commodities[i],
                                     columns=['NOMBRE_DPT', 'Conteo_Nacimientos'],
                                     key_on='feature.properties.NOMBRE_DPT',
                                     fill_color='OrRd',#'BuPu',#'YlGn',
                                     fill_opacity=0.9,
                                     line_opacity=0.3,
                                     legend_name='Cantidad de nacimientos',
                                     highlight=True,
                                     line_color='black').geojson.add_to(fs[i])
         NIL1 = folium.features.GeoJson(
                                     'colombiageo.json',
                                     style_function=style_function, 
                                     control=False,
                                     highlight_function=highlight_function, 
                                     tooltip=folium.features.GeoJsonTooltip(
                                     fields=['NOMBRE_DPT', 'Conteo_Nacimientos2'],
                                     aliases=['Departamento: ', 'Número de nacimientos:'],
                                     style=('background-color: grey; color: white;')
                                                                           )
                                    ).add_to(choropleth3) 

         
colormap = linear.OrRd_09.scale(NacimientoS.Conteo_Nacimientos.min(),
                                NacimientoS.Conteo_Nacimientos.max()).to_step(6)
colormap.caption = 'Cantidad de nacimientos'
colormap.add_to(map)


folium.TileLayer('cartodbpositron',overlay=True,name="Modo Mapamundi").add_to(map)

LayerControl(position='topright', collapsed=False).add_to(map)
map.save('colombia.html')
# create empty map zoomed in on Colombia ######################################################################################################

# Image
test_png = 'formula.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

# Initialise the app
app = dash.Dash(__name__)

server = app.server

# Color for the second tab
colors = {
    'background': 'grey',#'#6495ED',
    'text': '#FFFAF0'
}

# tab style and font
tabs_styles = {
    'height': '48px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6', # color #d6d6d6
    'padding': '6px',
    'color': 'white',
    'backgroundColor': '#119DFF'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'blue',
    'color': 'white',
    'fontWeight': 'bold',
    'padding': '6px'
}

# Define the app
app.layout = html.Div([
    html.Div(
        html.H1('Nacimientos en Colombia', style={'backgroundColor': '#F0F8FF', 'textAlign': 'center', 'color': 'black'})#'fontWeight': 'bold',
    ),
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Nivel departamental', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Análisis descriptivo', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Tendencia, patrones y pronósticos', value='tab-3', style=tab_style, selected_style=tab_selected_style)#,
        #dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles, className='custom-tabs-container', parent_className='custom-tabs'),
    html.Div(id='tabs-content-inline', style={'backgroundColor': '#F0F8FF'})
], style={'backgroundColor': '#F0F8FF'}) # Color background in all dash

# the callbacks
@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Iframe(id='map', srcDoc=open('colombia.html', 'r').read(), width='100%', height='760')
        ])
    if tab == 'tab-2':
        return html.Div([
            #html.H2("Principales características de los nacimientos",
            #                                                   style={'textAlign': 'left',
            #                                                          'color': 'black',
            #                                                          'font-style': 'normal',
            #                                                          'width' : '100%',
            #                                                          'margin-top':'3%',
            #                                                          'margin-left':'2%',
            #                                                          #'margin-right':'5%'
            #                                                         }
            #       ),
           html.P(['''Una de las características de la analítica de datos es la analítica descriptiva, la cual utiliza los datos históricos para dar respuesta a la pregunta “¿qué sucedió?”. A continuación, evidenciaremos la situación de Colombia a través de una serie de gráficos que ilustrarán la cantidad y sus características, tales como el género, peso y grupo sanguíneo de los años 2016, 2017 y 2018 (puedes consultar y descargar la base de datos en el siguiente link: ''', html.A("Estadísticas Vitales del DANE", href='http://microdatos.dane.gov.co/index.php/catalog/MICRODATOS/about_collection/22/5', target="_blank",
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'italic'
                                                                      #'width' : '100%',
                                                                      #'margin-top':'5%',
                                                                      #'margin-left':'5%',
                                                                      #'margin-right':'5%'
                                                                     }), '''). ''', html.Br(), html.Br(), '''Enseguida se muestran el total de nacimiento por año.'''],
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      'margin-top':'3%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
# the boxtext  
         html.Div(className='row',
         style = {'display' : 'flex'},
             children=[
        html.P('Número de nacimientos en el 2016 %s' % Nacimientos['Conteo_Nacimientos'].sum(),style={'textAlign': 'center','color': 'black','font-style': 'normal','height' : '50px','width' : '25%','margin-left':'7%','fontWeight': 'bold','border': '2px solid #90EE90 '},className='divBorder' #'backgroundColor': '#90EE90 '}, 
               ),
        html.P('Número de nacimientos en el 2017 %s' % Nacimientos2['Conteo_Nacimientos'].sum(),style={'textAlign': 'center','color': 'black','font-style': 'normal','height' : '50px','width' : '25%','margin-left':'7%','fontWeight': 'bold','border': '2px solid #90EE90 '},className='divBorder' #'backgroundColor': '#90EE90 '}, 
               ),
        html.P('Número de nacimientos en el 2018 %s' % Nacimientos1['Conteo_Nacimientos'].sum(),style={'textAlign': 'center','color': 'black','font-style': 'normal','height' : '50px','width' : '25%','margin-left':'7%','fontWeight': 'bold','border': '2px solid #90EE90 '},className='divBorder' #'backgroundColor': '#90EE90 '}, 
               )
        ]),
### the boxtext ### 
    html.P(['''Para dar un contexto y una posible interpretación del incremento de nacimientos en el 2017 se cita un fragmento de un artículo de la revisa Semana - "La Quinta oleada, Inició en 2016 con la reapertura de la frontera. El éxodo de venezolanos aumentó de manera exponencial con respecto a años anteriores. Mientras que en 2015 entraron de manera legal al país alrededor de 330.000 personas, la cifra ascendió a 796.000 en 2017" - para leer el artículo completo haz click ''', html.A("Aquí", href='https://www.semana.com/nacion/articulo/crisis-en-venezuela-migracion-historica-de-venezolanos-a-#colombia/556758', target="_blank",
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'italic',
                                                                      'width' : '95%',
                                                                      'fontWeight': 'bold'
                                                                     })], style={'textAlign': 'justify','color': 'black','font-style': 'normal','width' : '95%','margin-left':'2%'
                                                                     }),
html.P('''Lo anterior permite vislumbrar la importancia de un contexto, es decir, el dato en sí no proporciona "nada", pero cuando se realizan cruces con otras fuentes (base de datos, documentos, personas, etc), el dato brindará información que posteriormente se puede transformar en conocimiento. Todo esto conduce a lo que se conoce como Sistema de Información S.I. A continuación, se ilustra un gráfico de barras que permite observar la distribución de nacimientos por género para cada año.''', style={'textAlign': 'justify','color': 'black','font-style': 'normal','width' : '95%','margin-left':'2%'
                                                                     }),

    dcc.Graph(id='funnel-graph', figure=fig),
html.P('''Para un análisis de este gráfico y los siguientes, se debe tener en cuenta alguna característica significativa, representada e identificada en éste. Por ejemplo: al observar el 2017 se identifica que la mayoría de nacimientos correspondió al género masculino, además esta particularidad también está presente en el 2016 y 2018, lo que se puede inferir, es que a mediano plazo Colombia tendrá una niñez mayoritariamente masculina. Ahora, se ilustra un gráfico de tortas correspondiente a la distribución porcentual de los peso de los nacientes de 2016, 2017 y 2018.''', style={'textAlign': 'justify','color': 'black','font-style': 'normal','width' : '95%','margin-left':'2%'
                                                                     }), 
    dcc.Graph(id='Porcentaje_Peso', figure=fig2),
    html.P('''Sin ninguna dificultad (gracias a la gráfica) se puede observar y concluir que la distribución porcentual de los pesos se comporta de forma similar en cada uno de los años y, sin realizar análisis rigurosos ni estudio de casos, se puede deducir que el peso probable si alguien fuese a tener un niño, éste se encontraría entre los 2,5 kg y los 3,49 kg.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
    dcc.Graph(id='Porcentaje_RH', figure=fig3),
html.P('''Nuevamente se logra identificar que la distribución porcentual de los grupos sanguíneos tiene un comportamiento similar en cada uno de los años. Recordando el "contexto" discutido anteriormente y relacionado al cruce con otras fuentes, el grupo sanguíneo se convierte en un determinante fundamental al momento de salvar vidas durante algunas cirugías con situaciones inesperadas. En prospectiva, conocer la cantidad de nuevos posibles donantes permite realizar proyecciones en las reservar de sangre para los grupos sanguíneos con poca población, como lo son el B- y O- que oscilan entre el 2.6% y 0.39% respectivamente.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),

        ])# end of the elif IMPORTANT
    elif tab == 'tab-3':
        return html.Div([
            html.P('''Otra característica de la analítica de datos es la analítica predictiva, como su nombre lo indica, se concentra en responder a las preguntas asociadas a ¿qué podría pasar?. En este campo es indispensable la observación de tendencias y patrones que aporten a la creación de modelos que permiten vaticinar lo que va a ocurrir con antelación. Antes de continuar se definirá de forma intuitiva que es la tendencia y el patrón.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      'margin-top':'3%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
html.Ul([html.Li('''TENDENCIA: es la dirección general de una variable durante un período de tiempo.'''), html.Br(), html.Li('''PATRÓN: es un conjunto de datos que sigue una forma reconocible y recurrente.''')], style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      'margin-left':'2%'
                                                                     }),
html.P('''A continuación, se ilustra la serie de tiempo correspondiente al número de nacimiento por mes desde el 2016 hasta el 2018 de todo Colombia, en la cual se resaltan a modo de ejercicio ilustrativo dos patrones.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'3%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
    dcc.Graph(id='time', figure=fig4), 
html.P('''Al observar la gráfica se puede reconocer que cada año tiene dos sectores representados por colores diferentes, los cuales indican un patrón, el primero de color azul aguamarina corresponde a un patrón con comportamiento en forma de M (iniciando en febrero y terminando en junio) y el segundo un patrón con forma de línea recta (o con una tendencia lineal positiva, es decir creciente) desde junio hasta septiembre.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
html.P('''Lo anterior permite identificar el comportamiento del número de nacimientos a través de los años, lo que proporciona un conocimiento al momento de realizar un modelo de predicción. Enseguida se realiza un modelo usando redes neuronales, el cual dará un pronóstico para el año 2019, cabe resaltar que no solo se tuvo en cuenta los patrones que mencioné sino muchos otros. A continuación, se da una breve explicación del modelo de aprendizaje de maquinas que se usó, conocido como LSTM de sus siglas en inglés Long short-term memory.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
html.P('''Las LSTM son un tipo especial de redes recurrentes (son una clase de redes para analizar datos de series temporales). La característica principal de las redes recurrentes es que la información puede persistir introduciendo bucles en el diagrama de la red, por lo que, básicamente, pueden «recordar» estados previos y utilizar esta información para decidir cuál será el siguiente. Esta característica las hace muy adecuadas para manejar series cronológicas. Mientras las redes recurrentes estándar pueden modelar dependencias a corto plazo (es decir, relaciones cercanas en la serie cronológica), las LSTM pueden aprender dependencias largas, por lo que se podría decir que tienen una «memoria» a más largo plazo. El funcionamiento exacto de las redes LSTM es bastante complejo y se sale del propósito de este ejemplo ilustrativo.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'border': '2px solid #90EE90' ## Add border ##
                                                                      #'margin-right':'3%'
                                                                     }, className='divBorder'), ## Class border ##
    dcc.Graph(id='born-forecast', figure=fig6),
html.P('''Al observar la gráfica se reconoce que el pronóstico sigue el "mismo" comportamiento que en los años anteriores, pero, en algunos meses se sale de los rangos persistentes en los años previos, tal es el caso del mes de junio, el pronóstico observado es mucho más pequeño que el de los años anteriores, en los cuales se evidencia un comportamiento similar. Debido a que el modelo se realizó con solo tres años, puede que su precisión no sea la más adecuada, por consiguiente, los resultados del modelo servirán como una guía para una posible toma de decisiones.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
html.P(['''La analítica predictiva es un área que demanda tiempo, datos e información, por consiguiente, ésta debe estar muy bien enfocada debido al tiempo y al personal que se usará en su posible solución. Otra forma de identificar tendencias o patrones sin el uso de modelos complejos son las tasas de crecimientos (u otros tipos de indicadores) los cuales ayudan en la toma de decisiones, de manera oportunas, sencilla y algunas veces con resultados precisos.''', html.Br(), html.Br(), '''En seguida se ilustra la formula de la tasa de crecimiento (T).'''],
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
html.P([html.Img(src='data:image/png;base64,{}'.format(test_base64), style = {'height':'20%'})], style={'textAlign': 'center'}),
html.P('''T también conocida como tasa de variación, determina el cambio en porcentaje de una variable entre dos momentos distintos del tiempo. La siguiente figura muestra la tasa de variación de la cantidad de nacimientos entre los meses de dos años diferentes (2016, 2017) y (2017, 2018).''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),
    dcc.Graph(id='rate-figure', figure=fig5),
    html.P('''Observando la gráfica desde marzo hasta julio hubo un crecimiento en los nacimientos del 2016 al 2017 (línea azul), pero, durante ese mismo período hubo un decrecimiento en los nacimientos del 2017 al 2018 (línea roja). Adicionalmente se observa que para los meses de septiembre hasta diciembre la tasa de variación del 2017 al 2018 (línea roja) se mantuvo cercana a cero, lo que indica una cantidad de nacimiento similar durante esos meses del 2017 y 2018.''',
                                                              style={'textAlign': 'justify',
                                                                      'color': 'black',
                                                                      'font-style': 'normal',
                                                                      'width' : '95%',
                                                                      #'margin-top':'5%',
                                                                      'margin-left':'2%',
                                                                      #'margin-right':'3%'
                                                                     }),

        ])# end of the elif IMPORTANT

if __name__ == '__main__':
    app.run_server(debug=True)
