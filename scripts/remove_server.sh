cd /home/ec2-user/deploy/
if [ -d "interactive-web-server" ]
then 
    cd ./interactive-web-server
    docker-compose down
    cd /home/ec2-user/deploy
    rm -rf ./interactive-web-server
fi