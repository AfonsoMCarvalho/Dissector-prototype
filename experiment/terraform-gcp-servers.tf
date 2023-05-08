
# Elemets of the cloud such as virtual servers,
# networks, firewall rules are created as resources
# syntax is: resource RESOURCE_TYPE RESOURCE_NAME
# https://www.terraform.io/docs/configuration/resources.html



###########  Nodes serving onion urls   #############
# This method creates as many identical instances as the "count" index value
resource "google_compute_instance" "os-nodes" {
    count = 1
    name = var.NODES_ONION_NAMES[count.index]
    machine_type = var.GCP_MACHINE_TYPES[1]
    zone = var.NODES_ONION_REGIONS[count.index]

    #description = var.NODES_ONION_URLS[count.index] # description contains onion_url
    description = "${file("/PATH/hidden-service-docker-image/onion_addresses_v3/node${count.index + 1}/hostname")}" # description contains onion_url
    labels = {"onion_popularity": var.NODES_ONION_POPULARITY[count.index], 
              "onion_page": var.NODES_ONION_PAGES[count.index]}

    boot_disk {
        initialize_params {
        # image list can be found at:
        # https://cloud.google.com/compute/docs/images
        image = "ubuntu-1804-bionic-v20201116"
        #image = "debian-10-buster-v20211209"
        size = 50
        }
    }

    network_interface {
        network = "default"
        access_config {
        }
    }

    provisioner "remote-exec" {
      inline = ["echo 'Wait until SSH is ready'"]

      connection {
        type    = "ssh"
        user    = var.USER
        private_key = file("/home/afonso/.ssh/ansible")
        host = self.network_interface.0.access_config.0.nat_ip
      }
    }

    metadata = {
      ssh-keys = "${var.USER}:${file("~/.ssh/ansible.pub")}"
    }

    # Copies onion url files
    provisioner "file" {
      source      = "/PATH/hidden-service-docker-image/onion_addresses_v3/node${count.index + 1}/hostname"
      destination = "/home/${var.USER}/hostname"

      connection {
        type    = "ssh"
        user    = var.USER
        private_key = file("/home/afonso/.ssh/ansible")
        host = self.network_interface.0.access_config.0.nat_ip
      }
    }

    provisioner "file" {
      source      = "/PATH/hidden-service-docker-image/onion_addresses_v3/node${count.index + 1}/hs_ed25519_public_key"
      destination = "/home/${var.USER}/hs_ed25519_public_key"

      connection {
        type    = "ssh"
        user    = var.USER
        private_key = file("/home/afonso/.ssh/ansible")
        host = self.network_interface.0.access_config.0.nat_ip
      }
    }

    provisioner "file" {
      source      = "/PATH/hidden-service-docker-image/onion_addresses_v3/node${count.index + 1}/hs_ed25519_secret_key"
      destination = "/home/${var.USER}/hs_ed25519_secret_key"

      connection {
        type    = "ssh"
        user    = var.USER
        private_key = file("/home/afonso/.ssh/ansible")
        host = self.network_interface.0.access_config.0.nat_ip
      }
    }
    
  tags = ["node"]
}

###########  Nodes accessing onion urls   #############
# This method creates as many identical instances as the "count" index value
resource "google_compute_instance" "client-nodes" {
    count = 4
    name = var.NODES_CLIENT_NAMES[count.index]
    machine_type = var.GCP_MACHINE_TYPES[0]
    zone = var.NODES_CLIENT_REGIONS[count.index]

    boot_disk {
        initialize_params {
        # image list can be found at:
        # https://cloud.google.com/compute/docs/images
        image = "ubuntu-1804-bionic-v20201116"
        #image = "debian-10-buster-v20211209"
        size = 20
        }
    }

    network_interface {
        network = "default"
        access_config {
        }
    }

    provisioner "remote-exec" {
      inline = ["echo 'Wait until SSH is ready'"]

      connection {
        type    = "ssh"
        user    = var.USER
        private_key = file("/home/afonso/.ssh/ansible")
        host = self.network_interface.0.access_config.0.nat_ip
      }
    }

    metadata = {
      ssh-keys = "${var.USER}:${file("~/.ssh/ansible.pub")}"
    }
    
  tags = ["node"]
}



###########  Job coordinator node   #############
resource "google_compute_instance" "job-coordinator" {
    name = var.JOB_COORDINATOR_NAME
    machine_type = var.GCP_MACHINE_TYPES[0]
    zone = var.GCP_REGION1

    boot_disk {
        initialize_params {
        # image list can be found at:
        # https://cloud.google.com/compute/docs/images
        image = "ubuntu-1804-bionic-v20201116"
        size = 30
        }
    }

    network_interface {
        network = "default"
        access_config {
        }
    }

    provisioner "remote-exec" {
      inline = ["echo 'Wait until SSH is ready'"]

      connection {
        type    = "ssh"
        user    = var.USER
        private_key = file("~/.ssh/ansible")
        host = self.network_interface.0.access_config.0.nat_ip
      }
    }

    metadata = {
      ssh-keys = "${var.USER}:${file("~/.ssh/ansible.pub")}"
    }

  tags = ["node"]
}

###########  Probe nodes   #############
resource "google_compute_instance" "probe-nodes" {
    count = 12
    name = var.NODES_PROBES_NAME[count.index]
    machine_type = var.GCP_MACHINE_TYPES[1]
    zone = var.NODES_PROBES_REGION[count.index]

    boot_disk {
        initialize_params {
        # image list can be found at:
        # https://cloud.google.com/compute/docs/images
        image = "ubuntu-1804-bionic-v20201116"
        size = 30
        }
    }

    network_interface {
        network = "default"
        access_config {
        }
    }

    provisioner "remote-exec" {
      inline = ["echo 'Wait until SSH is ready'"]

      connection {
        type    = "ssh"
        user    = var.USER
        private_key = file("~/.ssh/ansible")
        host = self.network_interface.0.access_config.0.nat_ip
      }
    }

    metadata = {
      ssh-keys = "${var.USER}:${file("~/.ssh/ansible.pub")}"
    }

  tags = ["node"]
}