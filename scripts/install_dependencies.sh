cd /home/ec2-user/deploy
git clone https://github.com/wafflestudio/interactive-web-server.git
cd interactive-web-server
cp /home/ec2-user/deploy/secret.json ./web_editor/
sudo chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
docker-compose down