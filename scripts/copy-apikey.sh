#!/bin/bash
echo "Copying IBM Cloud apikey into development environment..."
docker cp ~/.bluemix/apikey.json promotions:/home/vscode 
docker exec promotions sudo chown vscode:vscode /home/vscode/apikey.json
echo "Complete"