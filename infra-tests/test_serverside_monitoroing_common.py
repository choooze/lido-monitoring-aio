import pytest

# Checking that our services are running
@pytest.mark.parametrize("service_name", [
    "docker",
    "monitoring-server",
])

def test_docker_running_and_enabled(host, service_name):
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled

# Check that we have docker-compose binary on the host
def test_docker_compose_installed(host):
    docker_compose = host.file("/usr/local/bin/docker-compose")
    assert docker_compose.exists
    assert docker_compose.mode == 0o755
    assert docker_compose.user == "root"
    assert docker_compose.group == "root"

# Check that every server-side container is in a running state
# TODO: make names persistent or loop through wildcard 
# list of services like *prometheus* 
@pytest.mark.parametrize("container_name", [
    "monitoring_prometheus_1",
    "monitoring_loki_1",
    "monitoring_grafana_1",
    "monitoring_alertmanager_1",
])

def test_container_state(host, container_name):
    service = host.docker(container_name)
    assert service.is_running

# Check that ports are listening and 
# accessible from localhost
@pytest.mark.parametrize("service_port", [
    "9090",
    "3100",
    "3000",
    "9093",
])

def test_service_port_open(host, service_port):
    service = host.addr("localhost")
    assert service.port(service_port).is_reachable
