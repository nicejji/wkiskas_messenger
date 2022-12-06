# Wkiskas Messenger


> ### Simple chat service built with FastAPI and Svelte.

![Auth page](/docs/media/auth.png) ![Chat](docs/media/chat.png)

#### Installation

- Install python packages.   
```poetry install```.  
  
- Install node packages and build frontend.   
```cd frontend_web && npm install && npm run build && cd ..```.  
- Set following environment variables (.env file can be used):  
```ACCESS_TOKEN_EXPIRES_MINUTES``` - *Expiration time for generated jwt tokens*.   
```DB_URL``` - *DB URL for PostgreSQL db*.  
```ALGORITHM``` - *Algorithm used for jwt signing, recommended ```HS256```*.  
```SECRET_KEY``` - *Secret key used for jwt signing, can be generated with ```openssl rand -hex 32```*

- Create database tables.    
```psql -d <database_name> -f init_db.sql```

- Run server.  
```poetry shell``` - *activate virtual environment*.  
```uvicorn main:app``` - *run uvicorn server*.  


