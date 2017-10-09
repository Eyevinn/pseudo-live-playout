docker build -t tut .
docker run -a stderr -a stdin -a stdout -i --rm -p 4000:80 tut 
