######################################################################
# Set up
######################################################################
build_run:
	docker compose -f ../docker-compose.yml build
	docker compose -f ../docker-compose.yml up -d
	docker compose exec backend python manage.py migrate
	docker compose exec backend python manage.py createsuperuser

######################################################################
# Run in development mode
######################################################################
run_dev:
	docker compose -f ../docker-compose.yml up -d

run_and_rebuild_dev:
	docker compose -f ../docker-compose.yml up -d --build

######################################################################
# Run in production mode
######################################################################
run_prod:
	docker compose -f ../docker-compose.prod.yml up -d

stop:
	docker compose down
######################################################################
# development tools
######################################################################
standardize-diff:
	isort keys/*.py accounts/*.py
	black keys/*.py accounts/*.py

standardize:
	autoflake --in-place --remove-all-unused-imports  --ignore-init-module-imports -r equipment/*.py accounts/*.py
	isort equipment/*.py accounts/*.py
	black equipment/*.py accounts/*.py

flake:
	flake8 equipment/*.py accounts/*.py
