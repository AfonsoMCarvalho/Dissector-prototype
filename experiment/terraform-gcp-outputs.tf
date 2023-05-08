# Terraform GCP
# To output variables, follow pattern:
# value = TYPE.NAME.ATTR

# example for a set of identical instances created with "count"
output "os_nodes_IPs1"  {
  value = formatlist("%s = %s", google_compute_instance.os-nodes[*].name, google_compute_instance.os-nodes[*].network_interface.0.access_config.0.nat_ip)
}

output "os_nodes_internal_IPs1"  {
  value = formatlist("%s = %s", google_compute_instance.os-nodes[*].name, google_compute_instance.os-nodes[*].network_interface.0.network_ip)
}

output "client_nodes_IPs1"  {
  value = formatlist("%s = %s", google_compute_instance.client-nodes[*].name, google_compute_instance.client-nodes[*].network_interface.0.access_config.0.nat_ip)
}

output "client_nodes_internal_IPs1"  {
  value = formatlist("%s = %s", google_compute_instance.client-nodes[*].name, google_compute_instance.client-nodes[*].network_interface.0.network_ip)
}

output "job_coordinator_IP1"  {
  value = formatlist("%s = %s", google_compute_instance.job-coordinator.name, google_compute_instance.job-coordinator.network_interface.0.access_config.0.nat_ip)
}

output "probe_nodes_IP1"  {
  value = formatlist("%s = %s", google_compute_instance.probe-nodes[*].name, google_compute_instance.probe-nodes[*].network_interface.0.access_config.0.nat_ip)
}

# Automaticaly create an inventory file with the returned IPs
# instance.description contains onion_url
#resource "local_file" "ansible_inventory" {
#  filename = "inventory_model.cfg"
#  content = <<EOF
#[all_nodes]
#%{ for instance in google_compute_instance.os_nodes[*] }${instance.name}   ansible_host=${instance.network_interface.0.access_config.0.nat_ip}   internal_ens4=${instance.network_interface.0.network_ip}   ansible_user=${var.USER}  ansible_ssh_private_key_file=${var.SSH_KEY} node_name=${instance.name} ansible_python_interpreter=/usr/bin/python3 onion_address=${instance.description}
#%{ endfor }
  
#[coordinator]
#job-coordinator		ansible_host=${google_compute_instance.job-coordinator.network_interface.0.access_config.0.nat_ip} 	ansible_user=${var.USER}   ansible_python_interpreter=/usr/bin/python3   ansible_ssh_private_key_file=${var.SSH_KEY} node_name=job-coordinator onion_address=none

#EOF
#}


resource "local_file" "ansible_inventory" {
  filename = "inventory_model.cfg"
  content = <<EOF
[os_nodes]
%{ for instance in google_compute_instance.os-nodes[*] }${instance.name}   ansible_host=${instance.network_interface.0.access_config.0.nat_ip}   internal_ens4=${instance.network_interface.0.network_ip}   ansible_user=${var.USER}  ansible_ssh_private_key_file=${var.SSH_KEY} node_name=${instance.name} ansible_python_interpreter=/usr/bin/python3 onion_popularity=0.${instance.labels["onion_popularity"]} onion_page=${instance.labels["onion_page"]} onion_address=${instance.description}
%{ endfor }

[client_nodes]
%{ for instance in google_compute_instance.client-nodes[*] }${instance.name}   ansible_host=${instance.network_interface.0.access_config.0.nat_ip}   internal_ens4=${instance.network_interface.0.network_ip}   ansible_user=${var.USER}  ansible_ssh_private_key_file=${var.SSH_KEY} node_name=${instance.name} ansible_python_interpreter=/usr/bin/python3
%{ endfor }

[probe_nodes]
%{ for instance in google_compute_instance.probe-nodes[*] }${instance.name}   ansible_host=${instance.network_interface.0.access_config.0.nat_ip}   internal_ens4=${instance.network_interface.0.network_ip}   ansible_user=${var.USER}  ansible_ssh_private_key_file=${var.SSH_KEY} node_name=${instance.name} ansible_python_interpreter=/usr/bin/python3
%{ endfor }

[client_nodes:vars]
request_iterations=1
session_iterations=1
experiment_folder=''

[probe_nodes:vars]
request_iterations=1
session_iterations=1
experiment_folder=''

[os_nodes:vars]
experiment_folder=''

[coordinator:vars]
experiment_folder=''
  
[coordinator]
job-coordinator		ansible_host=${google_compute_instance.job-coordinator.network_interface.0.access_config.0.nat_ip} 	ansible_user=${var.USER}   ansible_python_interpreter=/usr/bin/python3   ansible_ssh_private_key_file=${var.SSH_KEY} node_name=job-coordinator onion_address=none

EOF
}
