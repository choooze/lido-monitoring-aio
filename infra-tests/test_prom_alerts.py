import pytest
import requests
import json

prom_host = "mon-server.illcheck.you"
prom_scheme = "http://"
prom_port = "9090"
prom_api = prom_scheme + prom_host + ":" + prom_port


# Are we alive?
def test_aliveness():
    path = "/api/v1/query"
    query = {
        'query': 'up',
    }
    response = requests.get(url=prom_api+path, params=query)
    assert response.status_code == 200

# Checking cadvisor
def test_cadvisror():
    path = "/api/v1/query"
    query = {
        'query': 'cadvisor_version_info',
    }
    response = requests.get(url=prom_api+path, params=query)
    assert response.status_code == 200

# Checking node exporter
def test_nodeexporter():
    path = "/api/v1/query"
    query = {
        'query': 'node_os_version',
    }
    response = requests.get(url=prom_api+path, params=query)
    assert response.status_code == 200

# Check that our rule list is correct
#
# TODO: 
# 1. get container name from list of containers by pytest.docker
# 2. get rule list from somewhere (maybe put in rules dir?)
def test_check_rules_syntax(host):
    docker_run = host.run("docker exec monitoring_prometheus_1 "
                           "sh -c \"promtool check rules /etc/prometheus/alerts.yml \"")
    assert docker_run.rc == 0

def test_unittest_rules(host):
    docker_run = host.run("docker exec monitoring_prometheus_1 "
                           "sh -c \"promtool test rules /etc/prometheus/unittest.yml \"")
    assert docker_run.rc == 0

