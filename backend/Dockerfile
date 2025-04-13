FROM python:3.10.9

COPY . /app
WORKDIR /app
ENV TORCH_HOME=/app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN mkdir -p /app/hub && chmod -R 777 /app/hub
RUN mkdir -p /app/tmp_img && chmod -R 777 /app/tmp_img

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]