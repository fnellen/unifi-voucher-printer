FROM python:3.13.0a6-slim

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN apt-get update && apt-get install -y libusb-1.0-0 libusb-1.0-0-dev

COPY backend/requirements.txt /app
RUN pip install -r requirements.txt

COPY backend /app

EXPOSE 5000

CMD ["python3", "server.py" ]