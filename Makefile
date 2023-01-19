up:
		docker-compose -f docker-compose.yaml up --build

stop:
		docker-compose -f docker-compose.yaml stop

down:
		docker-compose -f docker-compose.yaml down

test: down
		docker-compose -f docker-compose.yaml build
		docker-compose -f docker-compose.yaml run -e POSTGRES_DB=tests app pytest tests
		docker-compose -f docker-compose.yaml down

test_module: down
		docker-compose -f docker-compose.yaml build
		docker-compose -f docker-compose.yaml run -e POSTGRES_DB=tests app pytest $(MODULE) -vv
		docker-compose -f docker-compose.yaml down

bandit:
	bandit -r ./app
