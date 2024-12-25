#Python image
FROM python:3.10-slim

#working directory
WORKDIR /app

# Copy requirements file into container
COPY requirements.txt /app/

# Install Dependecies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app cod eto container
COPY . .

# EXPOSE port FastAPI runs on
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
