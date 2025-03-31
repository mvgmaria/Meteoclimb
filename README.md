Meteoclimb is a tool designed for climbers in Spain to help them find climbing spots (crags) for their upcoming trips while also providing weather forecasts for these areas.

Features

- Find crags by region – Choose one or multiple regions in Spain where you want to climb.
- Set travel preferences – Filter crags based on maximum driving time and/or distance in kilometers.
- Weather forecasts – Get detailed weather predictions for your selected crags in 3-hour increments.
- Plan ahead – View forecasts for up to 5 days (to ensure accuracy).

### Database Set Up

You can use the test_crags.sql provided by going into MySQL and running the query, so that you have a database names "meteoclimb" with a table named "test_crags"

### Environment Variables Setup

1. Copy the .demo_env file and rename it to .env.
2. Open the .env file and add your API keys (both of them have sufficient free tiers) and database password:
   API_KEY="your_openrouteservice_key"
   API_KEY_W="your_open_weather_key"
   DB_KEY="your_db_password"

---

MeteoClimb es una herramienta diseñada para escaladores en España que les ayuda a encontrar zonas de escalada (escuelas) para sus próximos viajes, proporcionando también previsiones meteorológicas para dichas áreas.

Características

- Encuentra escuelas por región – Elige una o varias regiones de España donde quieras escalar.
- Configura tus preferencias de viaje – Filtra las escuelas según un tiempo máximo de conducción y/o distancia en kilómetros.
- Previsión meteorológica – Obtén pronósticos detallados en intervalos de 3 horas para las escuelas seleccionadas.
- Planifica con antelación – Consulta el clima hasta 5 días (para garantizar la precisión del pronóstico).

### Configuración de la base de datos

Puedes usar la base de datos test_crags.sql ejecutando el query en MySQL, de tal manera que tengas una base de datos llamada "meteoclimb" con una tabla llamada "test_crags"

### Configuración de las variables de entorno

1. Copia el archivo .demo_env y renómbralo a .env.
2. Abre el archivo .env y añade tus API keys (las dos tienen planes gratuitos con margen suficiente) y clave de tu base de datos:
   API_KEY="tu_clave_de_openrouteservice"
   API_KEY_W="tu_clave_de_open_weather"
   DB_KEY="tu_contraseña_db"
