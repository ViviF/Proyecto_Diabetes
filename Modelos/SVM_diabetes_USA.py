# Incluir las bibliotecas requeridas para el modelo y su métrica
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score
from sklearn.svm import SVC

#Cargar el archivo desde el repositorio
# URL del archivo CSV público en S3
url = 'https://diabetes-dvcstore.s3.us-east-1.amazonaws.com/files/md5/10/1cada3906fab160ea188043d7f9a1b'
# Carga el archivo directamente en un DataFrame de pandas
df = pd.read_csv(url)

# Separar las características (X) y la variable objetivo (y)

X = df.drop(columns=['Diabetes_012'])
y = df['Diabetes_012']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

#Importe MLFlow para registrar los experimentos, el regresor de Support Vector Machine y las métricas
import mlflow
import mlflow.sklearn

# defina el servidor para llevar el registro de modelos y artefactos
#mlflow.set_tracking_uri('http://localhost:5000')
# registre el experimento
experiment = mlflow.set_experiment("Diabetes_USA")

# Aquí se ejecuta MLflow sin especificar un nombre o id del experimento. MLflow los crea un experimento para este cuaderno por defecto y guarda las características del experimento y las métricas definidas.
# Para ver el resultado de las corridas haga click en Experimentos en el menú izquierdo.
with mlflow.start_run(experiment_id=experiment.experiment_id):
    # defina los parámetros del modelo
    C=1.0               #Tolerancia al error. Valores más altos -> Menor tolerancia
    kernel='linear'     #'rbf'
    random_state=42
    # Cree el modelo con los parámetros definidos y entrénelo
    SVM_model = SVC(C=C, kernel=kernel, random_state=random_state)
    SVM_model.fit(X_train, y_train)

    # Realice predicciones de prueba
    predictions = SVM_model.predict(X_test)

    # Registre los parámetros
    mlflow.log_param("C", C)
    mlflow.log_param("kernel", kernel)
    mlflow.log_param("random_state", random_state)

    # Registre el modelo
    mlflow.sklearn.log_model(SVM_model, "SVM-model")

    # Cree y registre la métrica de interés
    #mse = mean_squared_error(y_test, predictions)
    accuracy = accuracy_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    mlflow.log_metric("Precision", accuracy)
    mlflow.log_metric("Sensibilidad", recall)
    print(accuracy)
    print(recall)