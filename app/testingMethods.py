import os

menu = {}
menu['1']="GET /containers                     List all containers"
menu['2']="GET /containers?state=running      List running containers (only)"
menu['3']="GET /containers/<id>                Inspect a specific container"
menu['4']="GET /containers/<id>/logs           Dump specific container logs" 
menu['5']="GET /images                         List all images"
menu['6']="POST /images                        Create a new image"
menu['7']="POST /containers                    Create a new container"
menu['8']="PATCH /images/<id>                  Change a specific image's attributes"
menu['9']="DELETE /containers/<id>             Delete a specific container"
menu['10']="DELETE /containers                  Delete all containers"
menu['11']="DELETE /images/<id>                 Delete a specific image"
menu['12']="DELETE /images                      Delete all images"
menu['13']="Exit"

while True: 
  options=menu.keys() 
  options = sorted(options)
  print ("Available API endpoints:")
  for entry in options: 
    print (entry, menu[entry])
  selection=input("Please Select:") 
  if selection =='1': 
    os.system("curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool")
  elif selection == '2': 
    os.system("curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers?state=running | python -mjson.tool")
  elif selection == '3':
    id=input("Please Enter Container ID:") 
    os.system("curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers/%s" % id)
  elif selection == '4': 
    id=input("Please Enter Container ID:") 
    os.system("curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers/%s/logs" % id)
  elif selection == '5':
    os.system("curl -s -X GET -H 'Accept: application/json' http://localhost:8080/images | python -mjson.tool")
  elif selection == '6': 
    file = input("Please Enter File:") 
    os.system("curl -H 'Accept: application/json' -F file=@%s.Dockerfile http://localhost:8080/images" % file)
  elif selection == '7':
    id=input("Please Enter Image ID/Name:")
    os.system("curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{\"image\": \"%s\"}'" % id)
  elif selection == '8':
    id=input("Please Enter Image ID:")
    os.system("curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/bf7a249e576d -d  '{tag: %s}'" % id)
  elif selection == '9': 
    id=input("Please Enter Image ID:")
    os.system("curl -s -X DELETE -H 'Accept: application/json' http://localhost:8080/images/%s" % id)
  elif selection == '10':
    os.system("curl -s -X DELETE -H 'Accept: application/json' http://localhost:8080/containers")
  elif selection == '11': 
    id=input("Please Enter Image Tag:")
    os.system("curl -s -X DELETE -H 'Accept: application/json' http://localhost:8080/images/%s" % id)
  elif selection == '12':
    os.system("curl -s -X DELETE -H 'Accept: application/json' http://localhost:8080/images")
  elif selection == '13': 
    break
  else: 
    print ("Unknown Option Selected!")
