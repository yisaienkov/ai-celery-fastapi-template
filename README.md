# Celery & Flask Experiments

Work in progress...

### Run redis
> docker run -d -p 6379:6379 redis

### Run celery
> celery -A tasks worker --loglevel=INFO --pool=solo

### Run flask
> flask run