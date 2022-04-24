cd /home/ec2-user/deploy/interactive-web-server
if [ -f "secret.json" ] 
then
    echo "secret.json exists." > debug.txt # debugging
fi

docker-compose build --no-cache
docker-compose up -d