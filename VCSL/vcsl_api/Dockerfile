FROM --platform=linux/amd64 python:3.11

COPY . /app
WORKDIR /app
EXPOSE 4242
RUN ["python", "-m", "pip" , "install", "-r", "requirements.txt"]

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4242", "--reload"]
