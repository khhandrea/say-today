FROM python:3.9.16

WORKDIR /usr/src/app
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install

CMD ["pipenv", "run" ,"python3", "app.py"]