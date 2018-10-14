# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Load Vagrant configurations (versioned and unversioned)
if File.exist?("vagrant/config.yml")
  vm_config = YAML.load_file("vagrant/config.yml")
else
  vm_config = YAML.load_file("vagrant/config.default.yml")
end

Vagrant.configure("2") do |config|
  vagrant_home = "/home/vagrant"
  project_directory = "/vagrant"

  config.vm.define :dev do |machine|
    machine.vm.box = vm_config["box_name"]
    machine.vm.hostname = vm_config["dev_hostname"]
    machine.vm.network :public_network, ip: vm_config["dev_ip"]
    machine.ssh.username = vm_config["user"]

    machine.vm.provider :virtualbox do |v|
      v.name = vm_config["dev_hostname"]
      v.memory = vm_config["memory_size"]
      v.cpus = vm_config["cpus"]
    end

    if vm_config["copy_gitconfig"]
      machine.vm.provision :file, source: "~/.gitconfig", destination: ".gitconfig"
    end
    if vm_config["copy_vimrc"]
      machine.vm.provision :file, source: "~/.vimrc", destination: ".vimrc"
    end

    if vm_config["copy_profile"]
      machine.vm.provision :file, source: "~/.profile", destination: ".profile"
    end
    if vm_config["copy_bash_aliases"]
      machine.vm.provision :file, source: "~/.bash_aliases", destination: ".bash_aliases"
    end
    if vm_config["copy_bashrc"]
      machine.vm.provision :file, source: "~/.bashrc", destination: ".bashrc"
    end
    machine.vm.provision :shell do |s|
      s.name = "Bash startup additions (scripts/vagrant-bash)"
      s.inline = <<-SHELL
        if ! grep -q -F '#<<kubernetes>>' "${HOME}/.bashrc" 2>/dev/null
        then
          cat "${PROJECT_DIR}/scripts/vagrant-bash.sh" >> "${HOME}/.bashrc"
        fi
      SHELL
      s.env = { "HOME" => vagrant_home, "PROJECT_DIR" => project_directory }
    end

    machine.vm.provision :shell do |s|
      s.name = "Bootstrapping development server"
      s.path = "scripts/bootstrap.sh"
      s.args = [ project_directory ]
    end
  end

  (1..vm_config["masters"]).each do |index|
    config.vm.define "master_#{index}" do |machine|
      machine.vm.box = vm_config["box_name"]
      machine.vm.hostname = vm_config["master_#{index}_hostname"]
      machine.vm.network :public_network, ip: vm_config["master_#{index}_ip"]
      machine.ssh.username = vm_config["user"]

      machine.vm.provider :virtualbox do |v|
        v.name = vm_config["master_#{index}_hostname"]
        v.memory = vm_config["memory_size"]
        v.cpus = vm_config["cpus"]
      end
    end
  end

  (1..vm_config["nodes"]).each do |index|
    config.vm.define "node_#{index}" do |machine|
      machine.vm.box = vm_config["box_name"]
      machine.vm.hostname = vm_config["node_#{index}_hostname"]
      machine.vm.network :public_network, ip: vm_config["node_#{index}_ip"]
      machine.ssh.username = vm_config["user"]

      machine.vm.provider :virtualbox do |v|
        v.name = vm_config["node_#{index}_hostname"]
        v.memory = vm_config["memory_size"]
        v.cpus = vm_config["cpus"]
      end
    end
  end
end