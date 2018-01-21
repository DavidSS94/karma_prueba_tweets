Instrucciones de uso del REST API:

# Pasos:
- Corra el archivo .py con python: **python rest-tecnica.py**

*NOTA: si por alguna cuestión llega a marcar error por la falta de las librerías usadas (dateutil.parser, flask_pymongo, flask_cors), tendrá que instalarlas con los siguientes comando:*

- pip install -U python-dateutil
- pip install -U flask-cors
- pip install -U Flask-PyMongo

- Para realizar el consumo de los endpoints puede hacerlo mediante el CLI por medio del comando **curl**.

**Endpoint 1:** Devolver el número de tweets, número total de usuarios únicos, menciones únicas y hashtags únicos de toda la búsqueda.

# Consumo:
curl -d '{ "searchId" : "559d590abc0926835ba0bf41", "initialDate" : "2015-07-08", "finalDate" : "2015-07-10" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/endpoint_1

# Respuesta:
{
  "result": [
    {
      "totaltweets": 44
    },
    {
      "totalusers": 41
    },
    {
      "totalhastags": 25
    },
    {
      "totalmencionesunicas": 37
    }
  ]
}

**Endpoint 2:** Usuario con mayor número de tweets en la búsqueda.

# Consumo:
curl -d '{ "searchId" : "559d590abc0926835ba0bf41", "initialDate" : "2015-07-08", "finalDate" : "2015-07-10" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/endpoint_2

# Respuesta:
{
  "result": [
    {
      "conteo": 2,
      "usuario": "UVMovilidad"
    }
  ]
}


**Endpoint 3:** Top 10 de los hashtags con mayores apariciones en la búsqueda.

# Consumo:
curl -d '{ "searchId" : "559d590abc0926835ba0bf41", "initialDate" : "2015-07-08", "finalDate" : "2015-07-10" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/endpoint_3

# Respuesta:
{
  "result": [
    {
      "conteo": 39,
      "hashtag": "OrgulloMexicano"
    },
    {
      "conteo": 5,
      "hashtag": "orgullomexicano"
    },
    {
      "conteo": 3,
      "hashtag": "1MillonDeRaza"
    },
    {
      "conteo": 2,
      "hashtag": "ConoceM\u00e9xico"
    },
    {
      "conteo": 2,
      "hashtag": "ContigoSiempre"
    },
    {
      "conteo": 2,
      "hashtag": "PremiosCanacine"
    },
    {
      "conteo": 2,
      "hashtag": "sifueramillonario"
    },
    {
      "conteo": 2,
      "hashtag": "Agua"
    },
    {
      "conteo": 1,
      "hashtag": "Lloronas"
    },
    {
      "conteo": 1,
      "hashtag": "Cavall7"
    }
  ]
}

**Endpoint 4:** Porcentaje de retweets y tweets originales.

# Consumo:
curl -d '{ "searchId" : "559d590abc0926835ba0bf41", "initialDate" : "2015-07-08", "finalDate" : "2015-07-10" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/endpoint_4

# Respuesta:
{
  "result": [
    {
      "conteo": 17,
      "percentage": 38.63636363636363,
      "type": "retweet"
    },
    {
      "conteo": 27,
      "percentage": 61.36363636363637,
      "type": "original"
    }
  ]
}

# Validaciones

- Cada endpoint debe de validar que la búsqueda solicitada exista.

**Consumo**
curl -d '{ "searchId" : "000000000000000000000000", "initialDate" : "2015-07-08", "finalDate" : "2015-07-10" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/endpoint_4

**Respuesta**
{
  "Error": "La busqueda solicitada, no existe"
}

- Validar que los 3 campos requeridos vengan en la petición.

**Consumo**
curl -d '{ "searchId" : "", "initialDate" : "2015-07-08", "finalDate" : "2015-07-10" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/endpoint_4

**Respuesta**
{
  "Error": "Ingrese todos los datos"
}


- Validar que la fecha inicial sea menor que la final.

**Consumo**
curl -d '{ "searchId" : "559d590abc0926835ba0bf41", "initialDate" : "2015-07-08", "finalDate" : "2015-07-08" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/endpoint_4

**Respuesta**
{
  "Error": "La fecha inicial debe ser menor que la final"
}
