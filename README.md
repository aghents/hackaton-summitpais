# hackaton-summitpais

Explicación sencilla de solución:

Convertimos el video a texto usando el modelo whisper y lo almacenamos en una base de datos. Cuando el usuario hace una consulta a ese video, se copia ese valor de la transcipcion del video a una base de datos temporal que se llama Chroma. Cuando el usuario hace una consulta, el texto q el usuario ingreso se transforma a un vector o matriz y se "busca" donde hay menor diferencia con respecto al embedding del transcript del video. El embedding del transcript del video por su parte se genera cuando el usuario se conecta al websocket usando el modelo ada y el endpoint de la api q nos pasaron

Una vez se detecta la seccion de la transcripcion que mejor se parece al input del usuario, el modelo redacta una respuesta acorde al contexto y pregunta q usuario podria haber hecho.
