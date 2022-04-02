import pytest
import requests
import json

am_host = "mon-server.illcheck.you"
am_scheme = "http://"
am_port = "9093"
am_api = am_scheme + am_host + ":" + am_port


# Sending alert and checking response
def test_alert_sending():
    path = "/api/v1/alerts"
    params = [{
              'labels': {'alertname': 'HostOutOfDiskSpace',
                          'instance': 'mon-client.check.me',
                          'job': 'node',
                          'severity': 'warning'},
              'generatorURL': 'http://localhost:9090/graph'
              }
             ]
    json_params = json.dumps(params) 
    request = requests.post(url=am_api+path, data=json_params)
    assert request.text == '{"status":"success"}'
    assert request.status_code == 200

