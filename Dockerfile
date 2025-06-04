FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    build-essential libffi-dev curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"
RUN uv venv /app/.venv

WORKDIR /app 

COPY requirements.txt .

#RUN pip freeze > requirements.txt
RUN uv pip install -r requirements.txt 
COPY . .

CMD ["uv", "run", "python",  "bot/main.py"]

#docker image prune -y
#docker container prune -y
#docker compose up -d --build
