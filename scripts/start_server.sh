cd /home/ec2-user/deploy/interactive-web-server/web_editor
if [ ! -f "secret.json" ]
then
    cp /home/ec2-user/deploy/secret.json /home/ec2-user/deploy/interactive-web-server/web_editor/
fi

docker-compose build --no-cache
# docker-compose up -d
cd /home/ec2-user/deploy/interactive-web-server/
init-letsencrypt.sh