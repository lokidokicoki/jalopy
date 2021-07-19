PY_FILES := ${wildcard **/*.py}

lint:
	-isort ${PY_FILES}
	-flake8 ${PY_FILES}
	-pylint ${PY_FILES}
	-mypy ${PY_FILES}
