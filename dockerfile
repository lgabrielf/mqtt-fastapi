FROM eclipse-mosquitto

EXPOSE 1883

CMD ["mosquitto"]

RUN pip install -r requirements.txt