migrate:
	alembic upgrade head

rollback:
	alembic downgrade -1

gen:
	alembic revision --autogenerate -m "$(message)"