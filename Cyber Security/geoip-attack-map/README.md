This geoip attack map visualizer was developed to display network attacks on your organization in real time. 
The data server follows a syslog file, and parses out source IP, destination IP, source port, and destination port. 

Protocols are determined via common ports, and the visualizations vary in color based on protocol type

Important
This program relies entirely on syslog, and because all appliances format logs differently, you will need to customize the log parsing function(s). If your organization uses a security information and event management system (SIEM), it can probably normalize logs to save you a ton of time writing regex.

Send all syslog to SIEM.
Use SIEM to normalize logs.
Send normalized logs to the box (any Linux machine running syslog-ng will work) running this software so the data server can parse them.
Configs
Make sure in /etc/redis/redis.conf to change bind 127.0.0.1 to bind 0.0.0.0 if you plan on running the DataServer on a different machine than the AttackMapServer.
Make sure that the WebSocket address in /AttackMapServer/index.html points back to the IP address of the AttackMapServer so the browser knows the address of the WebSocket.
Download the MaxMind GeoLite2 database, and change the db_path variable in DataServer.py to the wherever you store the database.
./db-dl.sh
Add headquarters latitude/longitude to hqLatLng variable in index.html
Use syslog-gen.py, or syslog-gen.sh to simulate dummy traffic "out of the box."
IMPORTANT: Remember, this code will only run correctly in a production environment after personalizing the parsing functions. The default parsing function is only written to parse ./syslog-gen.sh traffic.
Bugs, Feedback, and Questions
If you find any errors or bugs, please let me know. Questions and feedback are also welcome, and can be sent to mcmay.web@gmail.com, or open an issue in this repository.

Deploy example
Tested on Ubuntu 16.04 LTS.

Clone the application:

git clone https://github.com/matthewclarkmay/geoip-attack-map.git
Install system dependencies:

sudo apt install python3-pip redis-server
Install python requirements:

cd geoip-attack-map
sudo pip3 install -U -r requirements.txt
Start Redis Server:

redis-server
Configure the Data Server DB:

cd DataServerDB
./db-dl.sh
cd ..
Start the Data Server:

cd DataServer
sudo python3 DataServer.py
Start the Syslog Gen Script, inside DataServer directory:

Open a new terminal tab (Ctrl+Shift+T, on Ubuntu).

./syslog-gen.py
./syslog-gen.sh
Configure the Attack Map Server, extract the flags to the right place:

Open a new terminal tab (Ctrl+Shift+T, on Ubuntu).

cd AttackMapServer/
unzip static/flags.zip
Start the Attack Map Server:

sudo python3 AttackMapServer.py
Access the Attack Map Server from browser:

http://localhost:8888/ or http://127.0.0.1:8888/

To access via browser on another computer, use the external IP of the machine running the AttackMapServer.

Edit the IP Address in the file "/static/map.js" at "AttackMapServer" directory. From:

var webSock = new WebSocket("ws:/127.0.0.1:8888/websocket");
To, for example:

var webSock = new WebSocket("ws:/192.168.1.100:8888/websocket");
Restart the Attack Map Server:

sudo python3 AttackMapServer.py
On the other computer, points the browser to:

http://192.168.1.100:8888/

This is an integration in active development by Justin Mitchell for the "NEW" Cyber Security branch repository 
