FROM python:3.9.15-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update && apt install -y gcc curl libcurl4-openssl-dev libssl-dev libgmp-dev libmpfr-dev libmpc-dev && pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]