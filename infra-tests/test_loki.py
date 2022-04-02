import pytest
import requests
import json
import time
import uuid

loki_host = "mon-server.illcheck.you"
loki_scheme = "http://"
loki_port = "3100"
loki_api = loki_scheme + loki_host + ":" + loki_port


# Are we alive?
def test_aliveness():
    path = "/loki/api/v1/status/buildinfo"
    response = requests.get(url=loki_api+path)
    assert response.status_code == 200


# Here we will start a tiny docker container
# with all needed labels and will generate log-string
#
# Will use random string for log line
loki_log_line = str(uuid.uuid4())

def test_docker_log_line_to_loki(host):
    docker_run = host.run("docker run --rm --name my-service "
                           "--log-driver=loki --log-opt loki-url=\"http://localhost:3100/loki/api/v1/push\" "
                           "-l com.docker.compose.service=myapp alpine sh -c \"echo "
                            + loki_log_line 
                            + "\"")
    assert docker_run.rc == 0

# Checking loki API to find a log-string
#
# We should use host's time
def test_get_host_epoch(host):
    global epoch
    epoch = int(time.time())

def test_log_line_in_loki():
    # Searching only in range of 8 seconds
    start_epoch = epoch - 4
    end_epoch = epoch + 4
    path = "/loki/api/v1/query_range"
    query = { 
        'start': start_epoch,
        'end': end_epoch,
        'query': '{compose_service="myapp"}',
    }
    response = requests.get(url=loki_api+path, params=query)
    j_response = json.loads(response.text)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    log_line = j_response['data']['result'][0]['values'][0][1]
    assert log_line == loki_log_line
