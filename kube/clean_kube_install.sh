sudo rm -rf  /etc/kubernetes
sudo rm -rf  /etc/cni/net.d
sudo rm -rf ~/.kube
sudo rm -rf /var/lib/cni/networks/cni0/*
sudo rm -rf /var/lib/cni/flannel/* && sudo rm -rf /var/lib/cni/networks/cbr0/* && sudo ip link delete cni0

