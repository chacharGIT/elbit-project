Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"

  config.vm.network "private_network", ip: "192.168.33.10"

  config.vm.hostname = "web.jewish.holidays.local"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "jewish_holidays"
    vb.memory = "2048"
    vb.cpus = "2"
  end

  config.vm.provision "shell", inline: <<-SHELL
    # Update system packages
    sudo yum update -y

    # Install Python 3, pip and nginx
    sudo yum install -y epel-release
    sudo yum install -y python3 python3-pip nginx

    # Install required Python packages
    sudo pip3 install flask requests python-dateutil

    # Create self-signed SSL cert and private key
    sudo openssl req -x509 -nodes -days 365 -subj "/C=IL" -newkey rsa:2048 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.crt

    # Copy the Python script and nginx configuration to the VM
    cp /vagrant/holidays.py /home/vagrant/holidays.py
    cp /vagrant/nginx.conf /etc/nginx/conf.d/default.conf

    # Restart Nginx
    sudo systemctl restart nginx

    # Change directory to the Python script location
    cd /home/vagrant

    # Create templates directory and place holidays.html
    mkdir templates
    cp /vagrant/holidays.html /home/vagrant/templates/holidays.html

    # Allow selinux httpd network connection
    sudo setsebool -P httpd_can_network_connect 1

    # Run the Flask server
    python3 holidays.py
  SHELL
end