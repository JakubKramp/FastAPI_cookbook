FROM python:3.10
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN pip3 install -U pip poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
COPY . /code
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]