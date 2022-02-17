FROM python:3.10.2-slim-buster

# Prevents Python from writing pyc files to disc. Equivalent to python -B
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr. Equivalent to python -u
ENV PYTHONUNBUFFERED 1
EXPOSE 40008

WORKDIR /usr/src

COPY requirements.txt /usr/src/requirements.txt



RUN pip3 install --upgrade pip \
    &&  pip install --no-cache --ignore-installed -r /usr/src/requirements.txt

### enable this production & remove the bind-mount ./src:/usr/src from docker-compose
# COPY ./src /usr/src 

CMD ["uvicorn", "main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "40008" ]