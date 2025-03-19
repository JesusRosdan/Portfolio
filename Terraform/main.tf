terraform {
  required_providers {
    proxmox = {
      source = "Telmate/proxmox"
      version = "3.0.1-rc6"
    }
  }
}
    #export PM_API_TOKEN_ID=""
    #export PM_API_TOKEN_SECRET=""

provider "proxmox" {
    pm_tls_insecure = true
    pm_api_url = "https://192.168.1.11:8006/api2/json"
    pm_otp = ""
}

locals {
  vms = [
    {
      name   = "DEVCI"
      memory = 4096
      cores  = 4
      ip = "192.168.1.90"
    },
    {
      name   = "Monitoring"
      memory = 8192
      cores  = 8
      ip = "192.168.1.91"
    },
    {
      name   = "Logging"
      memory = 8192
      cores  = 8
      ip = "192.168.1.92"
    }
  ]
}

resource "proxmox_vm_qemu" "VMs" {
    count = length(local.vms)
    
    name   = local.vms[count.index].name
    desc = "Machine ${count.index} of experiments"
    
    # Node name has to be the same name as within the cluster
    # this might not include the FQDN
    target_node = "pve" 
    clone       = "ubuntu-noble-cloudinit-template"
    # Activate QEMU agent for this VM
    agent = 1

    os_type = "Linux 6.x - 2.6 Kernel"

    cores  = local.vms[count.index].cores

    sockets = 1
    vcpus = 0
    cpu_type = "host"

    memory = local.vms[count.index].memory

    scsihw = "virtio-scsi-single"

    # Setup the disk
    disks {
        scsi {
            scsi0 {
                disk {
                    size            = 64
                    cache           = "none"
                    storage         = "local-lvm"
                    iothread        = true
                    discard         = true
                }
            }
        }
      ide {
              ide2 {
                  cloudinit {
                      storage = "local-lvm"
                  }
              }
        }  
    }
  
    # Setup the network interface and assign a vlan tag: 256
    network {
        id = 0
        model = "virtio"
        bridge = "vmbr0"
        firewall  = false
        link_down = false
    }
    
    #preprovision    = true
    # Setup the ip address using cloud-init.
    #boot = "order=scsi0"
    # Keep in mind to use the CIDR notation for the ip.
    ipconfig0 = "ip=${local.vms[count.index].ip}/24,gw=192.168.1.1"

    #ipconfig0  = "ip=${var.master_ips[count.index]}/${var.networkrange},gw=${var.gateway}"
    #ipconfig1  = "ip=${var.secondary_master_ips[count.index]}/${var.networkrange}"

    sshkeys    = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDdPvEBDoF1ns1dhvIqGUefw9Aqukp8Sdu+DVtkYdpqm jesusrosdan@hotmail.com"   
    ciuser     = var.linuxuser
    cipassword = var.linuxpassword
    nameserver = "1.1.1.1"
    boot       = "order=scsi0;ide2"
}