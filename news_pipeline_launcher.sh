#!/bin/bash
brew services start redis
brew services start mongo

#pip3 install -r requirements.txt

cd web-server
cd client
#npm install
npm run build
cd ../server
# npm install
npm start &

# Launch backend server
cd ../../backend_server
python3 service.py &

# Launch recommendation server
cd ../news_recommendation_service
python3 recommendation_service.py &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
