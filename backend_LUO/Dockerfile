FROM python:3.11.9

WORKDIR /app
ENV TORCH_HOME=/app


RUN apt-get update && apt-get install -y libgl1
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app
RUN mkdir -p /app/hub /app/tmp_img && chmod -R 777 /app/hub /app/tmp_img

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]