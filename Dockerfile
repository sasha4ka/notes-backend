FROM python:3.12-slim-bookworm
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app/
EXPOSE 8000
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]