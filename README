# Monitoring platform AIO PoC  

It's a bunch of roles for installing server/client side monitoring with a tools such as Prometheus/Grafana/Loki/AlertManager + Cadvisor/NodeExporter.

Every service installing as a Docker-container within Docker-compose assistance

## How To Use

Just add your hosts to inventory/hosts.yml to according groups (server might be also a client) and run it as

```bash
# Server part
ansible-playbook server.yaml
# Client part
ansible-playbook client.yaml
```

## Configuration

### Global
There are some switches in group_vars/all for enabling/disabling services  
```bash
# Switches
install_prometheus: true
install_grafana: true
install_loki: true
install_alertmanager: true

```

### Monitoring Server 
Every service has a default configuration living in the roles/monitoring-server/defaults/main/$SERVICENAME.yml

For example, **grafana**:
```bash
...

grafana_admin_user: "admin"
grafana_admin_password: "YOUR_SECRET_PASS" # Use Vault for keeping secrets!

grafana_cfg_dir: "/opt/grafana"
grafana_data_dir: "/data/grafana"
grafana_data_user: "grafana"
grafana_data_group: "grafana"

grafana_version: "latest"
grafana_publish_port: "3000"

grafana_cpu_limit: "1"
grafana_cpu_reserv: "0.25"

grafana_mem_limit: "512M"
grafana_mem_reserv: "128M"

```
