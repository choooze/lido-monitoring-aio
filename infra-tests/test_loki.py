import pytest
import requests
import json

loki_host = "mon-server.illcheck.you"
loki_scheme = "http://"
loki_port = "3100"
loki_api = loki_scheme + loki_host + ":" + loki_port


# Are we alive?
def test_aliveness():
    path = "/loki/api/v1/status/buildinfo"
    response = requests.get(url=loki_api+path)
    assert response.status_code == 200

# Here we will start a little docker container
# with all labels and generate log-string
def test_docker_log_line_to_loki(host):
    docker_run = host.run("docker run --rm --name my-service "
                           "--log-driver=loki --log-opt loki-url=\"http://localhost:3100/loki/api/v1/push\" "
                           "-l com.docker.compose.service=myapp alpine sh -c \"echo sEcReT_LiNe\"")
    assert docker_run.rc == 0

# Checking loki API to find a string
def test_log_line_in_loki():
    path = "/loki/api/v1/query"
    query = { 
        'query': '{compose_service="myapp"}',
    }
    response = requests.get(url=loki_api+path, params=query)
    j_response = json.loads(response.text)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
    log_line = j_response['data']['result'][0]['values'][0][1]
    assert log_line == "sEcReT_LiNe"
