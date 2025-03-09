FROM flyway/flyway:latest AS flyway-stage

FROM python:3.12.2-slim

# Install Java runtime so Flyway can run
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

COPY --from=flyway-stage /flyway /flyway

ENV PATH="/flyway:${PATH}"

COPY flyway.conf /flyway/conf/flyway.conf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x ./prestart.sh

EXPOSE 8000

CMD ["./prestart.sh"]