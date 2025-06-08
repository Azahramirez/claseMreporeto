# claseMreporeto
repositorio del reto integrador

# Ligas de otros repositorios del proyecto
- Ligas de repositorios 
1. Repositorio de desarrollo de solución 
https://github.com/Azahramirez/claseMreporeto 
2. Repositorio de imagen de Dashboard(Streamlit) 
https://github.com/roch21V2/streamlit_reto_final 
3. Repositorio de imagen de api(Fastapi) 
https://github.com/roch21V2/api 
4. Repositorio de infraestructura como código en Azure 
https://github.com/sheldon7681/infrastructure 
5. Repositorio de recursos en Kubernetes (AKS) 
https://github.com/sheldon7681/infrastructure-manifests

(Públicos para la revisión, al momento de finalizar, se mantendrán privados) 

---

## Inicializar repo:


>`uv sync`
>
>Cargar archivo con secretos `.env`

#### Formato archivo .env (para mlflow)

>MLFLOW_TRACKING_USERNAME=
>
>MLFLOW_TRACKING_PASSWORD=
>
>MLFLOW_TRACKING_URI=
>
>AZURE_STORAGE_CONNECTION_STRING=
>
>AZURE_STORAGE_ACCESS_KEY=



## Folder notebooks

- Dentro de este apartado se encuentra la limpieza y transformaciones de los datos dentro de `Notebook2_DataPrep_Final.ipynb`

- También se ubica cómo se aplico la prueba (ANOVA), que al final se cambió por Kruskal-Wallis debido a los supuestos de normalidad `Notebook2_DataAnalysis...`

- A partir de `Notebook{n}...ipynb` donde **n>2** se explica el proceso de desarrollo de modelos de serie de tiempo para distintas métricas y tablas
usando primero un modelo SARIMA y luego Prophet.

- `Notebook_3_TS_oc..` son dos notebooks distintos que explican los modelos de serie de tiempo para el porcentaje de ocupación en la tabla 
reservaciones `Tres` y la tabla ocupaciones `Tocu`.

- `Notebook_3_TS_inghab..` es el notebook que explica el proceso para generar el modelo de TS para el ingreso total por día
de la tabla ocupaciones

- `Notebook_4_Multiple..` es el notebook que explica el proceso para generar las cinco series de tiempo de num_adu para cada uno de los 5
estados de origen de clientes más importantes en la tabla ocupaciones.

## Folder data

Es donde se integran los datos en local solo para *entrenamiento*

## Folder models

Se muestran los modelos en formato .pkl

## Folder src

- Aparece primero un prototipo de dashboard que fue modificado para integrarse a la nube `app.py`

### Folder loadmlflow

- Dentro de `test.py` se muestra como se suben los modelos al contenedor en la nube de mlflow

### webapp

- Versión anterior de dashboard *funcional*, la imagen utilizada en el proyecto aparece en [Dashboard](https://github.com/roch21V2/streamlit_reto_final)

### apis

- Versión anterior de api *funcional*, la imagen utilizada en el proyecto aparece en [api](https://github.com/roch21V2/api)










