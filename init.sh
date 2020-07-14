docker build . -t ml4t
docker run -p 9090:8888 -v $PWD:/home/jovyan/work --name "ml" ml4t
