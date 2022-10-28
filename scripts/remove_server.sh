cd /home/ec2-user/deploy/
if [ -d "interactive-web-server" ]
then 
    cd ./interactive-web-server
    docker-compose down
    docker system prune
    docker builder prune
    cd /home/ec2-user/deploy
    rm -rf ./interactive-web-server
fi