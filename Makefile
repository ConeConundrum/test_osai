up:

		docker-compose -f docker-compose.yaml --build up

stop:
		docker-compose -f docker-compose.yaml stop

down:
		docker-compose -f docker-compose.yaml down

test: down
		docker-compose -f docker-compose.yaml build
		docker-compose -f docker-compose.yaml run -e POSTGRES_DB=tests app pytest tests -v
		docker-compose -f docker-compose.yaml down

test_module: down
		docker-compose -f docker-compose.yaml build
		docker-compose -f docker-compose.yaml run -e POSTGRES_DB=tests app pytest $(MODULE) -vv
		docker-compose -f docker-compose.yaml down
