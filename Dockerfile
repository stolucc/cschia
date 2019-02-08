FROM python:3

RUN pip install pipenv

COPY . /chia
WORKDIR /chia

RUN pipenv install --system --deploy

EXPOSE 5000
CMD ["sh", "./docker-entrypoint.sh"]
