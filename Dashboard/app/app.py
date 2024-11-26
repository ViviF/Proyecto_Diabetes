import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
import requests
import json
from loguru import logger
import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# PREDICTION API URL 
api_url = os.getenv('API_URL')
api_url = "http://{}:8001/api/v1/predict".format(api_url)

# Definir mínimos y máximos
edad_min = 18
edad_max = 120
estatura_min = 1
estatura_max = 2.5
peso_min = 10
peso_max = 300

# Layout in HTML
app.layout = html.Div([
    html.H1('Detección Riesgo de Diabetes', style={'textAlign': 'center', 'color': 'blue', 'fontSize': '36px',  'fontWeight': 'bold'}),
    html.H2('''Esta herramienta es una guía para indicar si el usuario está en riesgo de padecer o no diabetes 
    y en ningún caso reemplaza el diagnóstico médico.'''),
    
    html.Div([
        
        # Dropdown Estado General de Salud
        html.Label('En general, su estado de salud es:', style={'fontSize': 18, 'marginBottom': '20px', 'marginTop': '20px'}),  # Título
        dcc.Dropdown(
            id='GenHlth',
            options = [
                {'label':'Excelente', 'value':1}, {'label':'Muy bueno', 'value':2}, {'label':'Bueno', 'value':3},
                {'label':'Regular', 'value':4}, {'label':'Mala', 'value':5}
            ],
        style={'width': '300px', 'marginBottom': '20px', 'flex': 1} ), # Ancho del Dropdown 

        # Edad
        html.Label('Edad (18 a 120 años):', style={'fontSize': 18, 'marginBottom': '20px'}),
        dcc.Input(id='edad', type='number', step='any', placeholder='Ej: 37', min=edad_min, max=edad_max,
                  style={'width': '300px', 'marginBottom': '20px', 'marginRight': '20px', 'flex': 1}) 

        ]),

    html.Div([
        # Estatura
        html.Label('Estatura (en metros):', style={'fontSize': 18, 'marginBottom': '20px'}),
        dcc.Input(id='height', type='number', step='any', placeholder='Ej: 1.75', min=estatura_min, max=estatura_max, 
                  style={'width': '300px', 'marginBottom': '20px', 'marginRight': '20px'}),

        # Peso
        html.Label('Peso (en kg):', style={'fontSize': 18, 'marginBottom': '10px'}),
        dcc.Input(id='weight', type='number', step='any', placeholder='Ej: 70', min=peso_min, max=peso_max,   
                  style={'width': '300px', 'marginBottom': '20px'}),
    
        # Mostrar el resultado del IMC
        html.Div(id='BMI', style={'fontSize': 25, 'marginBottom': '20px'}),
        ]),
    
    html.Div([
        # Presión Arterial Alta
        html.Label('¿Tiene presión arterial alta?:', style={'fontSize': 18, 'marginBottom': '10px'}),
        dcc.RadioItems(
        id='HighBP',  
        options=[
            {'label': 'Si', 'value': 1},  
            {'label': 'No', 'value': 0}  
        ],
        labelStyle={'display': 'block', 'marginBottom': '10px'} ),

        # Colesterol Alto
        html.Label('¿Tiene colesterol alto?:', style={'fontSize': 18, 'marginBottom': '10px'}),
        dcc.RadioItems(
        id='HighChol',  
        options=[
            {'label': 'Si', 'value': 1},  
            {'label': 'No', 'value': 0}  
        ],
        labelStyle={'display': 'block', 'marginBottom': '10px'} ),

        # Ataque Cardíaco
        html.Label('Enfermedad coronaria o ataque cardíaco :', style={'fontSize': 18, 'marginBottom': '10px'}),
        dcc.RadioItems(
        id='HeartDiseaseorAttack',  
        options=[
            {'label': 'Si', 'value': 1},  
            {'label': 'No', 'value': 0}  
        ],
        labelStyle={'display': 'block', 'marginBottom': '10px'} ),

         ]),

         # Contenedor para la predicción, centrado al final
        html.Div(id='prediccion_diabetes', style={'fontSize': 35, 'marginTop': '40px', 'textAlign': 'center', 'fontWeight': 'bold'}),

    # dcc.Store para almacenar variables:
    dcc.Store(id='store_age'), # rango de edad
    dcc.Store(id='store_imc') # IMC
])


# Calcular el rango de edad 
@app.callback(
    Output('store_age', 'data'),
    Input('edad', 'value')
)
def rango_edad(edad):
    if edad:
        if 18 <= edad <= 24:
            Age = 1 
        elif edad <= 29:
            Age = 2 
        elif edad <= 34:
            Age = 3  
        elif edad <= 39:
            Age = 4  
        elif edad <= 44:
            Age = 5   
        elif edad <= 49:
            Age = 6  
        elif edad <= 54:
            Age = 7  
        elif edad <= 59:
            Age = 8  
        elif edad <= 64:
            Age = 9  
        elif edad <= 69:
            Age = 10  
        elif edad <= 74:
            Age = 11  
        elif edad <= 79:
            Age = 12  
        else:
            Age = 13 

        return {'age': Age}
    
    return {'age': None}


# Callback para calcular el IMC/BMI
@app.callback(
    Output('store_imc', 'data'),
    Output('BMI', 'children'),
    Input('height', 'value'),
    Input('weight', 'value')
)
def calcular_imc(height, weight):
    if (height and weight):
        # Calcular el IMC
        BMI = float(weight) / (float(height) ** 2)
        
        if BMI < 18.5:
            bmi_message = f"Su IMC es {BMI:.0f}: Bajo peso"
            color = '#20c1c9'
        elif BMI <= 24.9:
            bmi_message = f"Su IMC es {BMI:.0f}: Peso normal"
            color = '#20c975'
        elif BMI <= 29.9:
            bmi_message = f"Su IMC es {BMI:.0f}: Sobrepeso"
            color = '#decf28'
        elif BMI <= 34.9:
            bmi_message = f"Su IMC es {BMI:.0f}: Obesidad"
            color = '#f5bf2c'
        else:
            bmi_message = f"Su IMC es {BMI:.0f}: Obesidad mórbida"
            color = '#bf2626'
    
        return {'imc': BMI}, html.Div(bmi_message, style={'color': color, 'fontSize': '24px'})
        
    bmi_message = "Ingrese su estatura y peso para calcular el IMC."
    return {'imc': None}, html.Div(bmi_message, style={'color': 'red', 'fontSize': '24px'})


@app.callback(
    Output('prediccion_diabetes', 'children'),
    Input('HighBP', 'value'),
    Input('HighChol', 'value'),
    Input('HeartDiseaseorAttack', 'value'),
    Input('GenHlth', 'value'),
    Input('store_age', 'data'),
    Input('store_imc', 'data')
)
def calcular_imc_and_predict(HighBP, HighChol, HeartDiseaseorAttack, GenHlth, store_age, store_imc):
    Age = store_age.get('age', None)
    BMI = store_imc.get('imc', None)
    
    if HighBP is not None and HighChol is not None and HeartDiseaseorAttack is not None and GenHlth is not None and Age is not None and BMI is not None:

        
        # Preparar los datos para la predicción
        myreq = {
            "inputs": [
                {
                "HighBP": int(HighBP),
                "HighChol": int(HighChol),
                "BMI": int(BMI),
                "HeartDiseaseorAttack": int(HeartDiseaseorAttack),
                "GenHlth": int(GenHlth),
                "Age": int(Age),
                }
            ]
        }

        headers =  {"Content-Type":"application/json", "accept": "application/json"}

        # POST call to the API
        response = requests.post(api_url, data=json.dumps(myreq), headers=headers)
        data = response.json()
        logger.info("Response: {}".format(data))

        if round(data["predictions"][0])==1:
            prediccion_message = "Alto riesgo de diabetes."
            color1 = 'red'
        else:
            prediccion_message = "Bajo riesgo de diabetes."
            color1 = 'green'
                
        return html.Div(prediccion_message, style={'color': color1, 'fontSize': '35px'})

    return "Por favor, ingrese todos los datos solicitados"

if __name__ == '__main__':
    logger.info("Running dash")
    app.run_server(debug=True)
