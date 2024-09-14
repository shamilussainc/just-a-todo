FROM python:3.10

WORKDIR /code

# copy and run requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy migration related files
COPY ./alembic.ini /code/alembic.ini
COPY ./alembic/ /code/alembic/

COPY ./app/ /code/app/

# CMD [ "fastapi", "run", "app/main.py", "--port", "80" ]

