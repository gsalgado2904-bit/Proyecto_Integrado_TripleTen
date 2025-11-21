# -*- coding: utf-8 -*-

"""#Paso 1 - importar librerias y cargar datos."""

#Cargado de Librerias
import pandas as pd
import numpy as np
import math
from math import factorial
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats as st

#Carga del dataset
games_df = pd.read_csv("/datasets/games.csv")

"""#Paso 2 - Preparacion de datos"""

#Reemplazar los nombres de las columnas (Minusculas)

new_col_names = []
for columns in games_df:
    col_lowered = columns.lower()
    new_col_names.append(col_lowered)
games_df.columns = new_col_names

print(games_df.columns)

games_df.duplicated().sum()

#Convierte los datos en los tipos necesarios
#Describir columnas y los cambios de tipo de datos
#Trata los valores ausentes

#Para user score, primero se remplazo tbd con Nan, de ahi se convirtieron los valores a numericos para obtener un promedio y se sustituyeron los NaNs con el promedio de user_score
games_df["user_score"] = games_df["user_score"].replace("tbd",np.nan)
games_df["user_score"] = pd.to_numeric(games_df["user_score"])
user_score_mean = games_df["user_score"].mean()
games_df["user_score"] = games_df["user_score"].replace(np.nan,user_score_mean)

#Para year_of_release, hay varias juegos que tienen NaN por lo cual como se desconoce el año entonces no nos sirven estos datos para nuestro analisas ya que queremos ver tendencias por año y estos datos no las incluyen
games_df["year_of_release"] = games_df["year_of_release"].replace("NaN",np.nan)
games_df["year_of_release"] = pd.to_numeric(games_df["year_of_release"])
games_df = games_df.dropna(subset=["year_of_release"])

print(games_df["year_of_release"].unique())

#Debido a la naturaleza de los datos se agrega el promedio en los valores faltantes ya que estos no afectan el resultado promedio de ninguna de los dos DF elminar esas filas de nuestros DF significara una perdida de datos en otros valores como las ventas por region
#Se ponen como Nan los Year_of_release de esta forma, al graficar no tendremos una columna adicional y no tendremos que agregar filtros para excluir el año 0 es mejor dejarlo como null

#Calcula las ventas totales (la suma de las ventas en todas las regiones) para cada juego y coloca estos valores en una columna separada.
games_df["total_sales"] = games_df["na_sales"] + games_df["eu_sales"] + games_df["jp_sales"]

"""#Paso 3 - Analiza los datos"""

#Mira cuántos juegos fueron lanzados en diferentes años. ¿Son significativos los datos de cada período?
year_count = games_df.groupby("year_of_release")["name"].count().reset_index()
year_count_columns_new = {"year_of_release" : "year_of_release", "name" : "release_count"}
year_count.rename(columns = year_count_columns_new, inplace = True)
year_count["year_of_release"] = year_count["year_of_release"].astype(int)
year_count.plot(x="year_of_release",y="release_count", kind="bar",xlabel="Release Year", ylabel="Games Released",title="Game count by year",legend=False)

#Los datos si son significativos, ya que hay una tendencia de incremento a partir de los 90s la cual repunta la grafica y a partir del 2008 empieaza a tener una tendencia negativa

"""#Ventas de una plataforma a otra:
* Plataformas con mayores ventas totales
* Distribucion por año
* Plataformas que solian ser populares, pero ahora no tienen ventas
* Cuanto tarda una plataforma nueva en aparecer.
* Cuanto tarda una plataforma antigua en desaparecer.
"""

games_df.head()

#Prueba 1 plataforma con mayores ventas
total_platform_sales = games_df.groupby("platform")["total_sales"].sum().reset_index()
total_platform_sales = total_platform_sales.sort_values("total_sales", ascending=False)
total_platform_sales.plot(x="platform",y="total_sales",kind="bar")

print(total_platform_sales.head(5
                            ))

"""#Prueba 2 - distribucion por año

"""

highest_console_rows = ["DS","PS2", "PS3", "Wii", "X360"]
top_consoles_yearly = games_df[games_df['platform'].isin(highest_console_rows)]
top_consoles_yearly = top_consoles_yearly[top_consoles_yearly["year_of_release"] >= 2000.0]
total_sales_by_year = top_consoles_yearly.groupby(["platform","year_of_release"])["total_sales"].sum().unstack()
total_sales_by_year.plot(figsize=(20,15))
print(total_sales_by_year)






#bucle for que sobre highest console rows, para cada consola filtrar el dataframe. group by por año para calcular ventas totales.

#Caja de diagrama
#Diferencias significativas en las ventas
#ventas promedio en varias plataformas
total_sales_platform = games_df.groupby("platform")["total_sales"].sum().reset_index().sort_values(by="total_sales",ascending=False)
print(total_sales_platform)
sns.boxplot(total_sales_platform["total_sales"])

#Las ventas si tienen diferencias muy significantes basadas en el diagrama de caja, ya que hay muchos elementos los cuales se encuentran fuera del diagrama de caja y no son representativos de los demas.

#Como las reseñas afectan a las ventas
games_df.plot(kind="scatter",x="critic_score",y="total_sales")

print(games_df['critic_score'].corr(games_df['total_sales']))

#La relacion entre las reseñas de la critica y las ventas no estan relacionadas, ya que el resultado es muy poco casi todos los juegos se encuentran en un rango entre 15 o menos independientemente de la calificacion que le sea otorgada asi que mayor puntuacion no significa mayores ventas.

"""#Prueba 3 - Plataformas que solian ser populares, pero ahora no tienen ventas


"""

platform_last_release = games_df.groupby('platform')['year_of_release'].agg(lambda x: x.max()).reset_index()
platform_last_release["year_of_release"].rename("release_year")
platform_last_release = platform_last_release.sort_values(by="year_of_release")
unpopular_consoles = platform_last_release[platform_last_release['year_of_release'] < 2013]
print(unpopular_consoles)


#En esta tabla se representan todas las consales que a partir del 2013 han dejado de tener ventas de juegos, estas consolas tienen ya mas de 3 años que no son representativas en el mercado, por lo cual se pueden omitir

"""#Prueba 4 - Cuanto tarda una plataforma nueva en aparecer."""



platform_year_release["year_of_release"].shift(1)
platform_year_release["years_difference"] = platform_year_release["year_of_release"] - platform_year_release["year_of_release"].shift(1)
mean_release_window = platform_year_release["years_difference"].mean()
print(f"El tiempo promedio en que aparezca una consola nueva en el mercado es de: {mean_release_window} años")

"""#Prueba 5 - Cuanto tarda una plataforma antigua en desaparecer."""

platform_year_range = games_df.groupby('platform')['year_of_release'].agg(lambda x: x.max() - x.min()).reset_index()
mean_console_duration = platform_year_range["year_of_release"].mean()
print(f"El tiempo promedio de vida de una consola es de: {mean_console_duration} años")

"""#Paso 4 - perfil de usuario para cada region

Por region las 5 consolas principales y sus ventas
"""

#Top consoles NA
top_consoles_yearly_na = games_df.groupby("platform")["na_sales"].sum().reset_index()
top_consoles_yearly_na = top_consoles_yearly_na.sort_values(by="na_sales",ascending=False)
top_consoles_yearly_na = top_consoles_yearly_na.head(5)
mean_sales_na = top_consoles_yearly_na["na_sales"].mean()

#Top consoles EU
top_consoles_yearly_eu = games_df.groupby("platform")["eu_sales"].sum().reset_index()
top_consoles_yearly_eu = top_consoles_yearly_eu.sort_values(by="eu_sales",ascending=False)
top_consoles_yearly_eu = top_consoles_yearly_eu.head(5)
mean_sales_eu = top_consoles_yearly_eu["eu_sales"].mean()

#Top consoles JP
top_consoles_yearly_jp = games_df.groupby("platform")["jp_sales"].sum().reset_index()
top_consoles_yearly_jp = top_consoles_yearly_jp.sort_values(by="jp_sales",ascending=False)
top_consoles_yearly_jp = top_consoles_yearly_jp.head(5)
mean_sales_jp = top_consoles_yearly_jp["jp_sales"].mean()

#Una de las principales diferencias entre estos datos son sus promedios en general, de ahi podemos partir de las diferencias en ventas en cada una de las regiones
print(f"El promedio de ventas en NA es de: {mean_sales_na}")
print(f"El promedio de ventas en EU es de: {mean_sales_eu}")
print(f"El promedio de ventas en JP es de: {mean_sales_jp}")

#Aqui podemos obeservar que las ventas promedio de cada region es muy diferente y se distancian en algunos casos hasta en un doble o aproximados al doble.

"""Cinco generos principales por region"""

genres_top5 = games_df["genre"].value_counts()
print(genres_top5.head(5))

#print(top_consoles_yearly_na)

"""Conclusion: El genero accion, es un genero que se basa en muchos tipos de accion se puede interpretar desde peleas hasta disparos pero son categorizados como accion debido al alto contenido de secuencias o enfrentamientos freneticos

Sports se carazteriza por cualquier tipo de deporte, desde el Futbol hasta el Hockey entre muchos otros.

Misc estos son generos que no tienen una clasificacion como tal es decir pueden hacer multiples cosas, podrian tener accion, terror o multiples generos dentro del mismo

Role-Playing aqui se toma el papel de un personaje especifico y se le da al jugador una vasta habilidad de eleccion se caracterizan por estadisticas ya que el jugador puede tener muchos atributos diferentes y especializrse como0 por ejemplo en fuerza, destreza o en inteligencia

Shooter son juegos que se enfocan en disparos no necesariamente con armas, pero puede ser por ejemplo un juego de superheroes en el que todos tienen un tipo de arma que arrojan a los enemigos para cumplir con un objetivo

Clasificacion de ESRB
"""

#Primero obtenemos las ventas de cada rating de la ESRB por cada region
esrb_sales_na = games_df.groupby("rating")["na_sales"].sum().reset_index()
esrb_sales_eu = games_df.groupby("rating")["eu_sales"].sum().reset_index()
esrb_sales_jp = games_df.groupby("rating")["jp_sales"].sum().reset_index()

#Despues haremos merge de los 3 dataframes para poder compararlos.
esrb_sales_regions = esrb_sales_na.merge(esrb_sales_eu,on="rating",how="left")
esrb_sales_regions = esrb_sales_regions.merge(esrb_sales_jp,on="rating",how="left")

esrb_sales_regions.plot(x="rating",kind="bar")

#Con esto podemos demostrar que los juegos con mayor ingreso son los que estan clasificados con E, ya que significan Everyone que es para todos asi que no hay una limitante de edad.

"""Conclusion: Con esto podemos demostrar que los juegos con mayor ingreso son los que estan clasificados con E, ya que significan Everyone que es para todos asi que no hay una limitante de edad, esto tambien lo hace independientemente de la region ya que en en todas las clasificaciones con mayores ventas el patron es el mismo NA lidera, EU le sigue en segundo y JP siempre queda como el menor.

#Paso 5 - prueba de hipotesis

Las calificaciones promedio para Xbox One y PC son las mismas

Hipotesis nula: el promedio de las clasificaciones no es diferente para Xbox One y PC
"""

games_df.sample(5)

from scipy import stats as st

user_scores = games_df[['platform', 'user_score']]
xbox_one_user_scores = user_scores[user_scores['platform'] == "XOne"]
pc_user_scores = user_scores[user_scores['platform'] == "PC"]

alpha = 0.5

results = st.ttest_ind(xbox_one_user_scores["user_score"],pc_user_scores["user_score"])

print("valor p:", results.pvalue)

if results.pvalue < alpha:
    print("Rechazamos la hipotesis nula")
else:
    print("No podemos rechazar la hipotesis nula")

"""Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.

Hipotesis nula: el promedio de las clasificaciones no es diferente para los generos de Action y Sports
"""

from scipy import stats as st

genre_scores = games_df[['genre', 'user_score']]
action_scores = genre_scores[genre_scores['genre'] == "Action"]
sports_scores = genre_scores[genre_scores['genre'] == "Sports"]

alpha = 0.5

results = st.ttest_ind(action_scores["user_score"],sports_scores["user_score"])

print("valor p:", results.pvalue)

if results.pvalue < alpha:
    print("Rechazamos la hipotesis nula")
else:
    print("No podemos rechazar la hipotesis nula")



"""#Paso 6 - conclusion general

En conclusion si hay multiples varianzas en los datos dependiendo de como categoricemos o comparemos algunos datos, no parece ser una similitud muy grande entre datos pero si se notan las diferencias en cada region no solo por la cantidad de ventas, pero si lo analizamos mas a profundidas tambien seria importante contabilizar la cantidad de consolas vendidas en cada area y no solo el juego, esto para darle mas profundidad a nuestro analisis pero son datos adicionales que no son necesarios para nuestro proyecto.


Es importante destacar que los datos pueden ser mejor aprovechados para analizar temas de calificacion y generos de los videojuegos en si, pero para los temas principales como son las plataformas los datos no son los correctos para analizarlos.
"""
