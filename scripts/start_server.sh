cd /home/ec2-user/deploy/interactive-web-server
if [ -f "secret.json" ] 
then
    echo "secret.json exists." > debug.txt # debugging
fi

cp /home/ec2-user/deploy/secret.json /home/ec2-user/deploy/interactive-web-server/web_editor/

docker-compose build
docker-compose up -d