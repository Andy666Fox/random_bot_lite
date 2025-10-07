FROM python:3.10-slim
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    build-essential libffi-dev curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"
RUN uv venv /app/.venv

RUN groupadd -r tgrbgroup && \
    useradd -r -g tgrbgroup -d /app -s /bin/bash tgrbservice

WORKDIR /app 

COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt 

COPY . .

RUN chown -R tgrbservice:tgrbgroup /app

RUN chmod -R 755 /app

USER tgrbservice

CMD ["uv", "run", "python",  "bot/main.py"]



