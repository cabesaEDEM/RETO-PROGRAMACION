import os, psycopg, requests


try:
    req= requests.get("https://rickandmortyapi.com/api/character")

    resultados=req.json()["results"]

    url = os.getenv("DATABASE_URL")
    connection = psycopg.connect(url)
    cur = connection.cursor()

    for personaje in resultados:
        id = personaje["id"]
        name = personaje["name"]
        status = personaje["status"]
        species = personaje["species"]
        type_character = personaje["type"]
        gender = personaje["gender"]
        origin_name = personaje["origin"]["name"]
        location_name = personaje["location"]["name"]
        image = personaje["image"]
        url = personaje["url"]  
        cur.execute(
            """INSERT INTO characters (name, status, species, type, gender, origin_name, location_name, image, url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
            (name, status, species, type_character, gender, origin_name, location_name, image, url))
        

    connection.commit()
    cur.close()
    connection.close()
    
    print("BD conectada con éxito")
except Exception as e:
    print( e.with_traceback())