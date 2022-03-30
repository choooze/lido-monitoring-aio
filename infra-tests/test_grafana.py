import pytest
import requests
import json
from os import environ as env

grafana_host = "mon-server.illcheck.you"
grafana_scheme = "http://"
grafana_user = "admin"
grafana_pass = env['GRAFANA_PASS']
grafana_port = "3000"
grafana_api = grafana_scheme + grafana_user + ":" + grafana_pass + "@" + grafana_host + ":" + grafana_port

# Are we logged in?
def test_successful_login():
    path = "/api/login/ping"
    response = requests.get(url=grafana_api+path)
    assert response.status_code == 200

# Do we have datasources?
@pytest.mark.parametrize("datasource_name", [
    "Prometheus",
    "Loki",
])
def test_available_datasource(datasource_name):
    path = "/api/datasources"
    response = requests.get(url=grafana_api+path)
    j_response = json.loads(response.text)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert any(i['name'] == datasource_name for i in j_response)

# Do we have dashobaords?
@pytest.mark.parametrize("dashboard_name", [
    "Cadvisor Dashboard",
    "Loki | Errors in Logs",
    "Node Exporter USE Method",
])
def test_available_dashboards(dashboard_name):
    path = "/api/search"
    response = requests.get(url=grafana_api+path)
    j_response = json.loads(response.text)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert any(i['title'] == dashboard_name for i in j_response)
