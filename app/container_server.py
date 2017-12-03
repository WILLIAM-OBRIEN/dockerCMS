from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return """
Available API endpoints:
GET /containers                     List all containers
GET /containers?state=running      List running containers (only)
GET /containers/<id>                Inspect a specific container
GET /containers/<id>/logs           Dump specific container logs
GET /images                         List all images
POST /images                        Create a new image
POST /containers                    Create a new container
PATCH /containers/<id>              Change a container's state
PATCH /images/<id>                  Change a specific image's attributes
DELETE /containers/<id>             Delete a specific container
DELETE /containers                  Delete all containers (including running)
DELETE /images/<id>                 Delete a specific image
DELETE /images                      Delete all images
"""

@app.route('/containers', methods=['GET'])
def containers_index():
    """
    Lists all of the containers
    """
    if request.args.get('state') == 'running': 
        output = docker('ps')
        resp = json.dumps(docker_ps_to_array(output))
         
    else:
        output = docker('ps', '-a')
        resp = json.dumps(docker_ps_to_array(output))

    return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['GET'])
def images_index():
    """
    Lists all images 
    """
    imgVar='images'
	output = docker(imgVar)
    resp = json.dumps(docker_images_to_array(output))
    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
    """
    Inspect specific container
    """
	containerID = id
	output = docker('inspect',containerID)
    resp = output

    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>/logs', methods=['GET'])
def containers_log(id):
    """
    Dump specific container logs
    """
	containerID = id
	output = docker("logs",str(containerID))
    resp = str(docker_logs_to_object(str(containerID,output)))
    return Response(response=resp, mimetype="application/json")


@app.route('/images/<id>', methods=['DELETE'])
def images_remove(id):
    """
    Delete a specific image
    """
	imageID = id
    docker ('rmi', imageID)
    resp = '{"id": "%s"}' % imageID
    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['DELETE'])
def containers_remove(id):
    """
    Delete a specific container - must be already stopped/killed
    """
	containerID = id
    docker ('rm', containerID)
    resp = '{"id": "%s"}' % containerID
    return Response(response=resp, mimetype="application/json")

@app.route('/containers', methods=['DELETE'])
def containers_remove_all():
    """
    Force remove all containers - dangrous!
    """
	output = docker('ps','-a')
	containerDeletionList = docker_ps_to_array(output)
	for cont in containerDeletionList
		docker("stop",cont["id"])
		docker("rm",cont["id"])
    resp = '{response:"Deleted all containers!"}'
    return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['DELETE'])
def images_remove_all():
    """
    Force remove all images - dangrous!
    """
	output = docker('images')
	imageDeletionList = docker_images_to_array(output)
	for img in imageDeletionList
		docker("rmi",img["id"])
    resp = '{response:"Deleted all images!"}'
    return Response(response=resp, mimetype="application/json")


@app.route('/containers', methods=['POST'])
def containers_create():
    """
    Create container (from existing image using id or name)
    """
    body = request.get_json(force=True)
    image = body['image']
    args = ('run', '-d')
    id = docker(*(args + (image,)))[0:12]
    return Response(response='{"id": "%s"}' % id, mimetype="application/json")


@app.route('/images', methods=['POST'])
def images_create():
    """
    Create image (from uploaded Dockerfile)
    """
    dockerfile = request.files['file']
	dockerfile.save('NewDockerFile')
    docker('build', '-t', 'custom', '.')
	ListOfImages = docker('images')
    resp = json.dumps(docker_images_to_array(ListOfImages))
    return Response(response=resp, mimetype="application/json")




@app.route('/containers/<id>', methods=['PATCH'])
def containers_update(id):
    """
    Update container attributes (support: state=running|stopped)
    """
	containerID = id
    body = request.get_json(force=True)
    try:
        state = body['state']
        if state == 'running':
            docker('restart', containerID)
    except:
        pass

    resp = '{"id": "%s"}' % containerID
    return Response(response=resp, mimetype="application/json")

@app.route('/images/<id>', methods=['PATCH'])
def images_update(id):
    """
    Update image attributes (support: name[:tag])  tag name should be lowercase only
    """
	imageID = id
	imageVar = request.get_json(force=True)
	try:
		imageTag = imageVar['tag']
		docker('tag', imageID, imageTag)
		
	except:
		pass
		
    resp = '{"id","%s"}' % imageID
    return Response(response=resp, mimetype="application/json")


def docker(*args):
    cmd = ['docker']
    for sub in args:
        cmd.append(sub)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stderr.startswith('Error'):
        print 'Error: {0} -> {1}'.format(' '.join(cmd), stderr)
    return stderr + stdout

# 
# Docker output parsing helpers
#

#
# Parses the output of a Docker PS command to a python List
# 
def docker_ps_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['image'] = c[1]
        each['name'] = c[-1]
        each['ports'] = c[-2]
        all.append(each)
    return all

#
# Parses the output of a Docker logs command to a python Dictionary
# (Key Value Pair object)
def docker_logs_to_object(id, output):
    logs = {}
    logs['id'] = id
    all = []
    for line in output.splitlines():
        all.append(line)
    logs['logs'] = all
    return logs

#
# Parses the output of a Docker image command to a python List
# 
def docker_images_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[2]
        each['tag'] = c[1]
        each['name'] = c[0]
        all.append(each)
    return all

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)