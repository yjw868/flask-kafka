# Kafka-SocketIO version

The docker image consist 3 services:

 1. Kafka producer
 2. Kafka consumer
 3. Flask ScoketIO

How to use it:

- ```git clone https://github.com/yjw868/flask-kafka.git```
- ```cd flask-kafka```
- ```docker compose -f docker-compose.yml -up``` make sure the docker is running
- Go to http:localhost:8000
- Enter (1.115,2.119), (1.108,2.220), (1.101,2.209), (1.110,2.209), (1.112,2.212) into the input box
- Press submit
- The input will appear in the producer session
- The covariance matrix will appear in the consumer secession
