#! /bin/sh

echo "Creating FPC_ENGINE API Docker Image...";
cd API && docker build . -t fpc_api:latest && cd ..;

echo "\n++++++++++++++++++++++++++++\n";


echo "Creating Visualizer Docker Image...";
cd UI && docker build . -t fpc_ui:latest && cd ..;

echo "\n++++++++++++++++++++++++++++\n";

echo "Starting the Project...";
docker-compose up -d;
echo "Both Containers Started and Can be Accessed by their link  \"http://localhost:<port>\"";