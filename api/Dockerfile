FROM python:3.11.1-slim-buster

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt
COPY dist/invoicer_api-0.0.1-py3-none-any.whl /app/invoicer_api-0.0.1-py3-none-any.whl

RUN pip install -r requirements.txt --compile
RUN pip install invoicer_api-0.0.1-py3-none-any.whl --no-deps --compile

CMD ["python", "-m", "flask", "--app", "invoicer_api.app", "run", "--host", "0.0.0.0", "--port", "5001"]
