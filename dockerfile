FROM python:3.10-slim
ENV TOKEN="6897174789:AAH8EDJrQbgapAkdggamraRF8rGaCWAcbas"
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]