# Celery & Flask Experiments

Work in progress...

### Run redis
> docker run -p 6379:6379 redis

### Run worker
> docker build -t ai-brocker-worker:latest -f Dockerfile_worker .
> docker run -e REDISSERVER=redis://<ip>:6379 ai-brocker-worker:latest

### FastAPI
> docker build -t ai-brocker-api:latest -f Dockerfile_api .
> docker run -p 5000:5000 -e REDISSERVER=redis://<ip>:6379 ai-brocker-api:latest

### Flower
> docker run -p 5001:5555 mher/flower --broker=redis://<ip>:6379