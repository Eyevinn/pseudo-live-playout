
docker build -t maitv .

docker run -a stderr -a stdin -a stdout -i --rm -p 8080:8080 maitv 
