FROM python:3.11
WORKDIR /app
COPY client_requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "client_app.py"]
