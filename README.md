# dockerCMS
Fell behind due to timing. Command file works fine but the method file not so much. This means you can run all the commands but some have
to be from console. Youtube video feels too rushed and would have liked to try again, to show how much actually did work and that it had
most if not all of the functionality working.
External-IP: 35.195.48.255

list of functioning bash commands:
#list containers
curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool
curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers?state=running | python -mjson.tool

#list images
curl -s -X GET -H 'Accept: application/json' http://localhost:8080/images

#get specific container
curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers/fa55c6153102

#get specific container logs
curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers/fa55c6153102/logs
curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers/3802475d7a7a/logs

#create image
curl -H 'Accept: application/json' -F file=@whale-say.DockerFile  http://localhost:8080/images
curl -H 'Accept: application/json' -F file=@sshd.DockerFile  http://localhost:8080/images

#create container
curl -X POST -H 'Accept: application/json' http://localhost:8080/containers -d '{"image":"2e6c175114b3"}'
curl -X POST -H 'Accept: application/json' http://localhost:8080/containers -d '{"image":""}'
#delete specific image
curl -s -X DELETE -H 'Accept : application/json' http://localhost:8080/images/

#delete specific container
curl -s -X DELETE -H 'Accept : application/json' http://localhost:8080/containers/e9cae2fd6671

#update image 
curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/2e6c175114b3 -d  '{"tag": "newtag"}'
curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/bf7a249e576d -d  '{"tag": "plswork"}'

#remove all containers
curl -s -X DELETE -H 'Accept: application/json' http://localhost:8080/containers

#remove all images
curl -s -X DELETE -H 'Accept: application/json' http://localhost:8080/images

#stop container
sudo docker stop ""
