# Python chat using sockets
## Run on linux
```bash
# server
sudo apt install python3-pip
sudo apt install python3-venv
git clone https://github.com/H4RP3R/GB_SocketChat.git
cd GB_SocketChat
python3 -m venv env
source env/bin/activate
ip install -r requirements.txt
python3 server.py --ip <host_ip> --port <port_num>

# clients
python3 client.py --ip <host_ip> --port <port_num>
```