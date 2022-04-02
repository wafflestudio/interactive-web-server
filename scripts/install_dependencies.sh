cd /home/ec2-user/deploy
git clone https://github.com/wafflestudio/interactive-web-server.git
cd interactive-web-server
sudo chmod +x init-letsencrypt.sh
sudo ./init-letsencrypt.sh
docker-compose down