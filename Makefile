fix-imports:
	autoflake --in-place --recursive --remove-unused-variables --remove-all-unused-imports .
	isort -rc .
	black .

release:
	python setup.py bdist bdist_wheel --universal bdist_egg upload

.PHONY:	fix-import release
