FROM python:3.10-alpine

WORKDIR /app 

COPY requirements.txt .

#RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt 

COPY . .

CMD ["python", "bot/main.py"]

# uv pip freeze > requirements.txt
# docker build -t tgrandombot:latest .
# docker container prune (y)
# docker rmi -f tgrandombot
# 