import dash
import plotly.express as px
from dash import dcc

from dash import html
from web.models import *
import pandas as pd
from django_plotly_dash import DjangoDash
from collections import Counter
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash
from django.db.models import Sum


external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css']

# Important: Define Id for Plotly Dash integration in Django
app = dash.Dash(__name__)
app = DjangoDash('dash_integration_id', external_stylesheets=[dbc.themes.BOOTSTRAP])

app.css.append_css({
    "external_url": external_stylesheets
})

def update_data():
    # aquí puedes obtener los datos del servidor de Django
    queryset = Servicio.objects.filter(cotizacion__activo=True).values("marca", "cantidad")

    # Agrupar los valores por la columna prueba y sumar los valores de la columna cantidad
    df = pd.DataFrame(queryset)
    df = df.groupby("marca")["cantidad"].sum().reset_index()

    MS = px.pie(df, values="cantidad", names="marca")
    MS.update_layout(
        {'plot_bgcolor': 'rgba(0,0,0,0)',
         'paper_bgcolor': 'rgba(0,0,0,0)'},
    )
    MS.update_traces(hole=.5)
    
    ##########################################################################

    queryset = Servicio.objects.filter(cotizacion__activo=True).values("prueba", "cantidad")

    # Agrupar los valores por la columna prueba y sumar los valores de la columna cantidad
    df = pd.DataFrame(queryset)
    df = df.groupby("prueba")["cantidad"].sum().reset_index()

    # Crear la gráfica de pastel con los datos agregados
    pie = px.pie(df, values="cantidad", names="prueba")
    pie.update_layout(
        {'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'},
    )

    ##########################################################################

    cotitype = Cotizacion.objects.filter(activo = True).values("estatus")

    df = pd.DataFrame(cotitype)
    df = df.groupby("estatus").size().reset_index(name="count")

    # Crear la gráfica de pastel con los datos agregados
    cotitypefig = px.pie(df, values="count", names="estatus")
    cotitypefig.update_layout(
        {'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'},
    )

    ##########################################################################

    ordentype = OrdenTrabajo.objects.filter(activo = True).values("estatus")

    df = pd.DataFrame(ordentype)
    df = df.groupby("estatus").size().reset_index(name="count")

    # Crear la gráfica de pastel con los datos agregados
    ordentypefig = px.pie(df, values="count", names="estatus")
    ordentypefig.update_layout(
        {'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'},
    )

    #########################################################################
    
      #Entradas de aire
    queryset = Servicio.objects.filter(cotizacion__activo=True).values("entrada_nominal", "cantidad")

    # Agrupar los valores por la columna prueba y sumar los valores de la columna cantidad
    df = pd.DataFrame(queryset)
    df = df.groupby("entrada_nominal")["cantidad"].sum().reset_index()

    paire = px.pie(df, values="cantidad", names="entrada_nominal")
    paire.update_layout(
    {'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'},
    )
    paire.update_traces(hole=.5)
    
    ##########################################################################
    
        #Ajuste de valvulas
    queryset = Servicio.objects.filter(cotizacion__activo=True).values("ajuste", "cantidad")

    # Agrupar los valores por la columna prueba y sumar los valores de la columna cantidad
    df = pd.DataFrame(queryset)
    df = df.groupby("ajuste")["cantidad"].sum().reset_index()
    

    paieajuste = px.pie(df, values="cantidad", names="ajuste")
    paieajuste.update_layout(
    {'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'}
    ,)
    paieajuste.update_traces(textposition='inside', textinfo='percent+label')
    
    ###########################################################################
    servicios = Servicio.objects.filter(cotizacion__activo=True).values('marca', 'modelo').annotate(cantidad=Sum('cantidad'))

    df = pd.DataFrame(servicios)
    
    modelos=px.bar(df, x='marca', y='cantidad', color='modelo')
    
    modelos.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    ###############################################################################################

    # Obtener los datos de las cotizaciones y los clientes correspondientes
    cotizaciones = Cotizacion.objects.filter(activo=True).select_related('cliente')
    clientes = [cotizacion.cliente for cotizacion in cotizaciones]

    # Obtener los nombres de los clientes y las cantidades de cotizaciones
    nombres_clientes = [cliente.razon_social for cliente in clientes]
    cantidades_cotizaciones = [clientes.count(cliente) for cliente in set(clientes)]

    clientes_ordenados = [cliente for _, cliente in sorted(zip(cantidades_cotizaciones, nombres_clientes), reverse=True)]
    cantidades_cotizaciones_ordenadas = sorted(cantidades_cotizaciones, reverse=False)

    # Crear la gráfica de barras
    grafica_barras = go.Bar(
        y=nombres_clientes,
        x=cantidades_cotizaciones_ordenadas,
        orientation='h',  # Establecer la orientación horizontal
        marker=dict(color='green')
    )

    # Crear el objeto Layout para la gráfica
    layout = go.Layout(
        xaxis=dict(title='Cotizaciones',tickmode='linear',tick0=1,dtick=1),
        yaxis=dict(title='Clientes',tickmode='linear',tick0=1,dtick=1),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    # Crear la figura con la gráfica y el diseño
    fig = go.Figure(data=[grafica_barras], layout=layout)

    #######################################################################
    
    # Obtener el número de cotizaciones realizadas
    num_cotizaciones = Cotizacion.objects.filter(activo=True).count()

    # Crear el indicador numérico
    cot = go.Figure(go.Indicator(
        mode = "number",
        value = num_cotizaciones,
        title = {'text': "Número de cotizaciones"},
    ))

    # Personalizar el layout del gráfico
    cot.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )
    
    #######################################################################

    suma = Servicio.objects.filter(cotizacion__activo=True).count()

    # Crear el indicador numérico
    sum = go.Figure(go.Indicator(
        mode = "number",
        value = suma,
        title = {'text': "Número de servicios"},
    ))

    # Personalizar el layout del gráfico
    sum.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener número de cotizaciones vigentes.
    cotivig = Cotizacion.objects.filter(estatus__iexact='vigente', activo=True).count()

    # Crear el indicador numérico
    cotivig_sum = go.Figure(go.Indicator(
        mode = "number",
        value = cotivig,
        title = {'text': "Cotizaciones Vigentes"},
    ))

     # Personalizar el layout del gráfico
    cotivig_sum.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener número de cotizaciones aceptadas.
    cotiacp = Cotizacion.objects.filter(estatus__iexact='aceptada', activo=True).count()

    # Crear el indicador numérico
    cotiacp_sum = go.Figure(go.Indicator(
        mode = "number",
        value = cotiacp,
        title = {'text': "Cotizaciones Aceptadas"},
    ))

     # Personalizar el layout del gráfico
    cotiacp_sum.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener número de cotizaciones rechazadas.
    cotirec = Cotizacion.objects.filter(estatus__iexact='rechazada', activo=True).count()

    # Crear el indicador numérico
    cotirec_sum = go.Figure(go.Indicator(
        mode = "number",
        value = cotirec,
        title = {'text': "Cotizaciones Rechazadas"},
    ))

     # Personalizar el layout del gráfico
    cotirec_sum.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener el número de órdenes de trabajo realizadas
    num_ordentrabajo = OrdenTrabajo.objects.filter(activo = True).count()

    # Crear el indicador numérico
    OT_sum = go.Figure(go.Indicator(
        mode = "number",
        value = num_ordentrabajo, 
        title = {'text': "Total de Órdenes"},
    ))
    
    OT_sum.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener número de órdenes de trabajo en espera.
    num_espera = OrdenTrabajo.objects.filter(estatus__iexact='espera', activo=True).count()

    # Crear el indicador numérico
    ordenEspera = go.Figure(go.Indicator(
        mode = "number",
        value = num_espera,
        title = {'text': "Órdenes en Espera"},
    ))

     # Personalizar el layout del gráfico
    ordenEspera.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener número de órdenes de trabajo en laboratorio.
    num_lab = OrdenTrabajo.objects.filter(estatus__iexact='laboratorio', activo=True).count()

    # Crear el indicador numérico
    ordenLab = go.Figure(go.Indicator(
        mode = "number",
        value = num_lab,
        title = {'text': "Órdenes en Laboratorio"},
    ))

     # Personalizar el layout del gráfico
    ordenLab.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener número de órdenes de trabajo en revision.
    num_rev = OrdenTrabajo.objects.filter(estatus__iexact='revision', activo=True).count()

    # Crear el indicador numérico
    ordenRev = go.Figure(go.Indicator(
        mode = "number",
        value = num_rev,
        title = {'text': "Órdenes en Revisión"},
    ))

     # Personalizar el layout del gráfico
    ordenRev.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener número de órdenes de trabajo terminadas.
    num_ter = OrdenTrabajo.objects.filter(estatus__iexact='terminado', activo=True).count()

    # Crear el indicador numérico
    ordenTer = go.Figure(go.Indicator(
        mode = "number",
        value = num_ter,
        title = {'text': "Órdenes Terminadas"},
    ))

     # Personalizar el layout del gráfico
    ordenTer.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    ########################################################################
    
    # Obtener número de órdenes de trabajo en Pausa.
    num_pau = OrdenTrabajo.objects.filter(estatus__iexact='terminado', activo=True).count()

    # Crear el indicador numérico
    ordenPau = go.Figure(go.Indicator(
        mode = "number",
        value = num_pau,
        title = {'text': "Órdenes en Pausa"},
    ))

     # Personalizar el layout del gráfico
    ordenPau.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )

    #######################################################################
    
    sumaval = Servicio.objects.filter(cotizacion__activo=True).aggregate(total_suma=models.Sum('cantidad'))['total_suma']

    # Crear el indicador numérico
    sumva = go.Figure(go.Indicator(
        mode = "number",
        value = sumaval,
        title = {'text': "Valvulas Totales:"},
    ))

    # Personalizar el layout del gráfico
    sumva.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )
    
    #########################################################################
    
    servicios_acreditados = Servicio.objects.filter(cotizacion__activo=True).filter(alcance_acreditado=True)
    total_objetos_acreditados = 0

    for servicio in servicios_acreditados:
        total_objetos_acreditados += servicio.cantidad
        
    # Crear el indicador numérico
    acre = go.Figure(go.Indicator(
        mode = "number",
        value = total_objetos_acreditados,
        title = {'text': "Número de acreditados"},
    ))

    # Personalizar el layout del gráfico
    acre.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )
    
    ##############################################################
    
    servicios_correctivos = Servicio.objects.filter(cotizacion__activo=True).filter(tipo_mantenimiento="Correctivo")
    total_objetos_correctivos = 0

    for servicio in servicios_correctivos:
        total_objetos_correctivos += servicio.cantidad
    
    correc = go.Figure(go.Indicator(
        mode = "number",
        value = total_objetos_correctivos,
        title = {'text': "Mantenimiento Correctivo"},
    ))

    # Personalizar el layout del gráfico
    correc.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )
    
    #############################################################
    
    servicios_preventivo = Servicio.objects.filter(cotizacion__activo=True).filter(tipo_mantenimiento="Preventivo")
    total_objetos_preventivo = 0

    for servicio in servicios_preventivo:
        total_objetos_preventivo += servicio.cantidad
    
    preven = go.Figure(go.Indicator(
        mode = "number",
        value = total_objetos_preventivo,
        title = {'text': "Mantenimiento Preventivo"},
    ))

    # Personalizar el layout del gráfico
    preven.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )
    
    ############################################################
    
    servicios_presion = Servicio.objects.filter(cotizacion__activo=True).filter(tipo_mantenimiento="Cambio de Presion de Ajuste")
    total_objetos_presion = 0

    for servicio in servicios_presion:
        total_objetos_presion += servicio.cantidad
    
    presion = go.Figure(go.Indicator(
        mode = "number",
        value = total_objetos_presion,
        title = {'text': "Presion de Ajuste"},
    ))

    # Personalizar el layout del gráfico
    presion.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )
    
    
    #############################################################
    
    num_clientes = Cliente.objects.filter(activo=True).count()

    clisum = go.Figure(go.Indicator(
        mode = "number",
        value = num_clientes,
        title = {'text': "Clientes totales:"},
    ))

    # Personalizar el layout del gráfico
    clisum.update_layout(
        width=300,
        height=150,
        margin={'t': 40, 'b': 0, 'l': 0, 'r': 0},
        paper_bgcolor="white",
    )
    
    ###############################################################
    
    # Obtener datos de clientes
    clientes_name = Cliente.objects.filter(activo=True).values_list("razon_social", flat=True)
    clientes_est = Cliente.objects.filter(activo=True).values_list("estado", flat=True)
    data = {'nombre': clientes_name, 'estado': clientes_est}
    clientes_data = pd.DataFrame(data)

    # Definir las coordenadas de cada estado
    coordenadas = {
        'Aguascalientes': (21.8818, -102.2916),
        'Baja California': (30.8406, -115.2838),
        'Baja California Sur': (26.0444, -111.6661),
        'Campeche': (18.476, -90.3189),
        'Chiapas': (16.7569, -93.1292),
        'Chihuahua': (28.6329, -106.0691),
        'Ciudad de México': (19.4326, -99.1332),
        'Coahuila': (27.0587, -101.7068),
        'Colima': (19.2465, -103.7236),
        'Durango': (24.0277, -104.6532),
        'Guanajuato': (21.019, -101.2574),
        'Guerrero': (17.5734, -99.5275),
        'Hidalgo': (20.1169, -98.7333),
        'Jalisco': (20.6597, -103.3496),
        'Estado de México': (19.4978, -99.1269),
        'Michoacán': (19.7069, -101.1903),
        'Morelos': (18.6813, -99.1013),
        'Nayarit': (21.7514, -104.8455),
        'Nuevo León': (25.5922, -99.9962),
        'Oaxaca': (17.0732, -96.7266),
        'Puebla': (19.0414, -98.2063),
        'Querétaro': (19.1817, -88.4791),
        'Quintana Roo': (19.1817, -88.4791),
        'San Luis Potosí': (22.1565, -100.9855),
        'Sinaloa': (25.1721, -107.4795),
        'Sonora': (29.0892, -110.9613),
        'Tabasco': (17.8409, -92.6189),
        'Tamaulipas': (23.7416, -99.1435),
        'Tlaxcala': (19.3122, -98.2394),
        'Veracruz': (19.1738, -96.1342),
        'Yucatán': (20.6843, -88.5678),
        'Zacatecas': (22.7709, -102.5832)
    }


    # Obtener las coordenadas de cada estado en el DataFrame de clientes
    locations = []
    for estado in clientes_data['estado']:
        lat, lon = coordenadas[estado]
        locations.append([lat, lon])

    # Agregar nombres al DataFrame de locations y cantidad de clientes por estado
    locations_df = pd.DataFrame(locations, columns=['latitud', 'longitud'])
    locations_df['estado'] = clientes_data['estado']
    clientes_por_estado = clientes_data.groupby('estado')['nombre'].count().reset_index(name='cantidad')
    locations_df = pd.merge(locations_df, clientes_por_estado, on='estado')

    # Crear figura de burbujas
    mapacli = go.Figure()
    mapacli.add_trace(
        go.Scattermapbox(
            lat=locations_df['latitud'],
            lon=locations_df['longitud'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=locations_df['cantidad']*5,
                sizemode='diameter',
                sizeref=0.3,
                color='blue',
                opacity=0.3,
            ),
            text=locations_df['estado'] + ': ' + locations_df['cantidad'].astype(str), # Cambiar para que muestre la información combinada
            hoverinfo='text'
        )
    )
    # Configurar layout del mapa
    mapacli.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoibGVvbmFyZG9yZyIsImEiOiJjbGgyOWF0NHMxYXNpM2VwN2xocGZvbXB4In0.mZHTAgo23Lb_VxylzehlUw',
            bearing=0,
            center=dict(
                lat=23.634501,
                lon=-102.552784
            ),
            pitch=0,
            zoom=3.5,
        ),
    )
    ##########################################################################
    
    return MS, pie, paire, paieajuste, modelos, fig, cot, sum, acre, mapacli, clisum, correc, sumva, preven, presion, OT_sum, cotivig_sum, cotiacp_sum, cotirec_sum, cotitypefig, ordenEspera, ordenLab, ordenRev, ordenTer, ordenPau, ordentypefig

# Define el layout de la aplicación
app.layout = dbc.Container(
    [
        dbc.CardBody(
            [
        dbc.Row([
                dbc.Col(html.H1("Datos generados en plataforma web Metrotecnia S.A de C.V", style={'text-align': 'center', 'margin-bottom': '5%'}), width={'size': 12})
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                            [
                                dbc.CardHeader(),
                                dbc.CardBody(
                                    dcc.Graph(id='indicadorclisum', figure=go.Figure()),
                                    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                                ),
                                dbc.CardFooter()
                            ]
                        ),
                        width={'size': 3}),
                dbc.Col(
                    dbc.Card(
                            [
                                dbc.CardHeader(),
                                dbc.CardBody(
                                    dcc.Graph(id='indicadorser', figure=go.Figure()),
                                    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}

                                ),
                                dbc.CardFooter()
                            ]
                        ),
                        width={'size': 3}),
                dbc.Col(
                    dbc.Card(
                            [
                                dbc.CardHeader(),
                                dbc.CardBody(
                                    dcc.Graph(id='indicadoracre', figure=go.Figure()),
                                    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                                ),
                                dbc.CardFooter()
                            ]
                        ),
                        width={'size': 3})
            ]),
            dbc.Row(dbc.Col(html.H1("Información de clientes", style={'text-align': 'center', 'margin-bottom': '3%', 'margin-top': '5%'}), width={'size': 12}),),
            dbc.Row([
                dbc.Col(                        
                    dbc.Card(
                        [
                            dbc.CardHeader("Cotizaciones generadas por los clientes"),
                            dbc.CardBody(
                                dcc.Graph(id='fig', figure=go.Figure())
                            ),
                            dbc.CardFooter()
                        ]
                    ),width={'size': 12}),
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Mapa de ubicaciones de los clientes"),
                            dbc.CardBody(
                                dcc.Graph(id='mapacli', figure=go.Figure()),
                            ),
                            dbc.CardFooter()
                        ]
                    ),style={'margin-top': '2%'}, width={'size': 12})
            ]),
            ###################### COTIZACIONES ######################
            dbc.Row(dbc.Col(html.H1("Cotizaciones", style={'text-align': 'center', 'margin-bottom': '3%', 'margin-top': '5%'}), width={'size': 12}),),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(),
                        dbc.CardBody(
                            dcc.Graph(id='indicadorcot', figure=go.Figure()),
                            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                            ),
                        dbc.CardFooter()
                    ]),
                    width={'size': 3}
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(),
                        dbc.CardBody(
                            dcc.Graph(id='indicadorcotvig', figure=go.Figure()),
                            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                            ),
                        dbc.CardFooter()
                    ]),
                    width={'size': 3}
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(),
                        dbc.CardBody(
                            dcc.Graph(id='indicadorcotacp', figure=go.Figure()),
                            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                            ),
                        dbc.CardFooter()
                    ]),
                    width={'size': 3}
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(),
                        dbc.CardBody(
                            dcc.Graph(id='indicadorcotrec', figure=go.Figure()),
                            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                            ),
                        dbc.CardFooter()
                    ]),
                    width={'size': 3}
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Cotizaciones por estatus"),
                        dbc.CardBody(
                            dcc.Graph(id='cotitypefig', figure=go.Figure())
                        ),
                        dbc.CardFooter()
                    ]),
                    style={'margin-top': '2%'}, width={'size': 12}
                ),
            ]),
            ######################VALVULAS Y MANTENIMIENTOS######################
            dbc.Row(dbc.Col(html.H1("Información de Servicios", style={'text-align': 'center', 'margin-bottom': '3%', 'margin-top': '5%'}), width={'size': 12}),),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(),
                            dbc.CardBody(
                                dcc.Graph(id='indicadorvalvula', figure=go.Figure()),
                                style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                            ),
                            dbc.CardFooter()
                        ]
                    ),
                    width={'size': 3}),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(),
                            dbc.CardBody(
                                dcc.Graph(id='indicadorcorrec', figure=go.Figure()),
                                style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                            ),
                            dbc.CardFooter()
                        ]
                    ),
                    width={'size': 3}),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(),
                            dbc.CardBody(
                                dcc.Graph(id='indicadorpreven', figure=go.Figure()),
                                style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                            ),
                            dbc.CardFooter()
                        ]
                    ),
                    width={'size': 3}),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(),
                            dbc.CardBody(
                                dcc.Graph(id='indicadorpresion', figure=go.Figure()),
                                style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                            ),
                            dbc.CardFooter()
                        ]
                    ),
                    width={'size': 3}),
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Marcas de válvulas en servicios"),
                            dbc.CardBody(
                                dcc.Graph(id='marca', figure=go.Figure())
                            ),
                            dbc.CardFooter()
                        ]
                    ), style={'margin-top': '2%'}, width={'size': 6}),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Tipo de prueba de válvula"),
                            dbc.CardBody(
                                dcc.Graph(id='prueba', figure=go.Figure())
                            ),
                            dbc.CardFooter()
                        ]
                    ), style={'margin-top': '2%'}, width={'size': 6})
            ]),
            dbc.Row([
                dbc.Col(                        
                    dbc.Card(
                        [
                            dbc.CardHeader("Tipo de ajuste de presión"),
                            dbc.CardBody(
                                dcc.Graph(id='ajuste', figure=go.Figure())
                            ),
                            dbc.CardFooter()
                        ]
                    ), style={'margin-top': '2%'}, width={'size': 6}
                ),
                dbc.Col(                        
                    dbc.Card(
                        [
                            dbc.CardHeader("Tipo de entrada nominal"),
                            dbc.CardBody(
                                dcc.Graph(id='aire', figure=go.Figure())
                            ),
                            dbc.CardFooter()
                        ]
                    ),style={'margin-top': '2%'}, width={'size': 6})
            ]),
            dbc.Row([
                dbc.Col(                        
                    dbc.Card(
                        [
                            dbc.CardHeader("Modelo de válvulas"),
                            dbc.CardBody(
                                dcc.Graph(id='modelo', figure=go.Figure()),
                            ),
                            dbc.CardFooter()
                        ]
                    ), style={'margin-top': '2%'}, width={'size': 12})
            ])
            ]
        ),
        ###################### ORDENES DE TRABAJO ######################
        dbc.Row(dbc.Col(html.H1("Órdenes de Trabajo", style={'text-align': 'center', 'margin-bottom': '3%', 'margin-top': '5%'}), width={'size': 12}),),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(),
                    dbc.CardBody(
                        dcc.Graph(id='indicadororden', figure=go.Figure()),
                        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                        ),
                    dbc.CardFooter()
                ]),
                width={'size': 3}
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(),
                    dbc.CardBody(
                        dcc.Graph(id='indicadorordenEspera', figure=go.Figure()),
                        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                        ),
                    dbc.CardFooter()
                ]),
                width={'size': 3}
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(),
                    dbc.CardBody(
                        dcc.Graph(id='indicadorordenLab', figure=go.Figure()),
                        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                        ),
                    dbc.CardFooter()
                ]),
                width={'size': 3}
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(),
                    dbc.CardBody(
                        dcc.Graph(id='indicadorordenRev', figure=go.Figure()),
                        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                        ),
                    dbc.CardFooter()
                ]),
                width={'size': 3}
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(),
                    dbc.CardBody(
                        dcc.Graph(id='indicadorordenTer', figure=go.Figure()),
                        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                        ),
                    dbc.CardFooter()
                ]),
                style={'margin-top': '2%'}, width={'size': 3}
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(),
                    dbc.CardBody(
                        dcc.Graph(id='indicadorordenPau', figure=go.Figure()),
                        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
                        ),
                    dbc.CardFooter()
                ]),
                style={'margin-top': '2%'}, width={'size': 3}
            ),
        ]),
        dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader("Órdenes de trabajo por estatus"),
                        dbc.CardBody(
                            dcc.Graph(id='ordentypefig', figure=go.Figure())
                        ),
                        dbc.CardFooter()
                    ]),
                    style={'margin-top': '2%'}, width={'size': 12}
                ),
            ]),
        
        dbc.CardFooter(),
        dcc.Interval(
            id='interval-component',
            interval=5*1000,  # en milisegundos
            n_intervals=0
        )
    ]
)

# Define el callback para actualizar los gráficos
@app.callback(
   [Output(component_id='marca', component_property='figure'),
    Output(component_id='prueba', component_property='figure'),
    Output(component_id='aire', component_property='figure'),
    Output(component_id='ajuste', component_property='figure'),
    Output(component_id='modelo', component_property='figure'),
    Output(component_id='fig', component_property='figure'),
    Output(component_id='indicadorcot', component_property='figure'),
    Output(component_id='indicadorser', component_property='figure'),
    Output(component_id='indicadoracre', component_property='figure'),
    Output('mapacli', 'figure'),
    Output(component_id='indicadorclisum', component_property='figure'),
    Output(component_id='indicadorcorrec', component_property='figure'),
    Output(component_id='indicadorvalvula', component_property='figure'),
    Output(component_id='indicadorpreven', component_property='figure'),
    Output(component_id='indicadorpresion', component_property='figure'),
    Output(component_id='indicadororden', component_property='figure'),
    Output(component_id='indicadorcotvig', component_property='figure'),
    Output(component_id='indicadorcotacp', component_property='figure'),
    Output(component_id='indicadorcotrec', component_property='figure'),
    Output(component_id='cotitypefig', component_property='figure'),
    Output(component_id='indicadorordenEspera', component_property='figure'),
    Output(component_id='indicadorordenLab', component_property='figure'),
    Output(component_id='indicadorordenRev', component_property='figure'),
    Output(component_id='indicadorordenTer', component_property='figure'),
    Output(component_id='indicadorordenPau', component_property='figure'),
    Output(component_id='ordentypefig', component_property='figure')],
    [Input(component_id='interval-component', component_property='n_intervals')]
)
def update_graphs(n):
    MS, pie, paire, paieajuste, modelos, fig, indicadorcot, indicadorser, indicadoracre, mapacli, indicadorclisum, indicadorcorrec, indicadorvalvula, indicadorpreven, indicadorpresion, indicadororden, indicadorcotvig, indicadorcotacp, indicadorcotrec, cotitypefig, indicadorordenEspera, indicadorordenLab, indicadorordenRev, indicadorordenTer, indicadorordenPau, ordentypefig= update_data()
    return MS, pie, paire, paieajuste, modelos, fig, indicadorcot, indicadorser, indicadoracre, mapacli, indicadorclisum, indicadorcorrec, indicadorvalvula, indicadorpreven, indicadorpresion, indicadororden, indicadorcotvig, indicadorcotacp, indicadorcotrec, cotitypefig, indicadorordenEspera, indicadorordenLab, indicadorordenRev, indicadorordenTer, indicadorordenPau, ordentypefig

if __name__ == '__main__':
    app.run_server(debug=True)