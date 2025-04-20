FROM python:3.8.10

WORKDIR /app
ENV TORCH_HOME=/app

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1

# Pre-copy only requirements to leverage cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Now copy the rest of the app
COPY . /app

# Make folders and set permissions
RUN mkdir -p /app/hub /app/tmp_img && chmod -R 777 /app/hub /app/tmp_img

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]