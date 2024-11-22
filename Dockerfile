# backend/Dockerfile
FROM python:3.9

WORKDIR /app


COPY requirements.txt .

#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


#port that FASTAPI will run on 
EXPOSE 8000

#command to run the application

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]