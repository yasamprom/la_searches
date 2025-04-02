FROM python:3.9
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y chromium
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:/app/la-searches"
ENV TELEGRAM_API_TOKEN ${TELEGRAM_API_TOKEN}
ENV TG_IDS ${TG_IDS}
CMD ["python3", "src/main.py"]