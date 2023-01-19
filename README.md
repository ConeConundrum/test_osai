# test_osai
All endpoints are in root `localhost/`

Docs available are in root `localhost/docs`

Environment variables already presented in repo with `.env` file


## Run with docker compose

`docker-compose -f docker-compose.yaml up --build`

## Run with make

Run app: `make up`

Stop all: `make stop`

Delete all: `make down`

Run tests: `make test`

Run static analyze: `make bandit`
