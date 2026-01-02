FROM python:3.14.2-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

RUN echo "0 * * * * cd /app && export PYTHONPATH=/app && python3 cleanup.py >> /var/log/cron.log 2>&1" > /etc/cron.d/webapp-cleanup
RUN chmod 0644 /etc/cron.d/webapp-cleanup
RUN crontab /etc/cron.d/webapp-cleanup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x entrypoint.sh
CMD [ "./entrypoint.sh" ]