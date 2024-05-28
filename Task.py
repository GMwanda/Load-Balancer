import os
import math
from flask import Flask, request, jsonify
from ConsistentHash import ConsistentHashMap
import random
import string
import subprocess
import docker

app = Flask(__name__)

# Constants for consistent hash map
N = 3   # Number of server containers
SLOTS = 512  # Total number of slots in the consistent hash map
K = int(math.log2(SLOTS))  # Number of virtual servers for each server container

# Initialize the consistent hash map
consistent_hash_map = ConsistentHashMap(num_servers=N, num_slots=SLOTS, num_virtual_servers=K)


@app.route('/home', methods=['GET'])
def home():
    server_id = os.environ.get('SERVER_ID', 'Unknown')
    return jsonify({"message": f"Hello from Server: {server_id}", "status": "successful"}), 200


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return 'Hello', 200


@app.route('/map_request', methods=['GET'])
def map_request():
    request_id = request.args.get('id', type=int)
    print(request_id)

    if request_id is None:
        return jsonify({"error": "Request ID is required"}), 400
    try:
        server_id = consistent_hash_map.map_request(request_id)
        return jsonify({"request_id": request_id, "mapped_server": server_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Assuming a simple in-memory structure to keep track of replica
replicas = []

def random_hostname(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "N": len(replicas),
        "replicas": replicas
    })

docker_client = docker.from_env()
@app.route('/add', methods=['POST'])
def add_replicas():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])

    if len(hostnames) > n:
        return jsonify({"error": "Number of hostnames exceeds number of instances to add"}), 400

    new_replicas = []
    for i in range(n):
        if i < len(hostnames):
            hostname = hostnames[i]
        else:
            hostname = random_hostname()

        try:
            # Remove the container if it already exists
            existing_container = docker_client.containers.get(hostname)
            existing_container.stop()
            existing_container.remove()
        except docker.errors.NotFound:
            pass  # Container does not exist, no need to remove it

            # Run a new container
        container = docker_client.containers.run("web_server_image", name=hostname,
                                                 detach=True)  # replace "web_server_image" with actual image name
        new_replicas.append(container.name)

        # new_replicas.append(hostname)
        # subprocess.run(["docker", "run", "-d", "--name", hostname,
        #                 "web_server_image"])  # replace "web_server_image" with actual image name
    replicas.extend(new_replicas)
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }), 200


@app.route('/rm', methods=['DELETE'])
def remove_replicas():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])

    if len(hostnames) > n:
        return jsonify({"error": "Number of hostnames exceeds number of instances to remove"}), 400

    to_remove = set()
    if hostnames:
        to_remove.update(hostnames)
    else:
        to_remove.update(random.sample(replicas, min(n, len(replicas))))

    for hostname in to_remove:
        if hostname in replicas:
            replicas.remove(hostname)
            subprocess.run(["docker", "stop", hostname], check=True)
            subprocess.run(["docker", "rm", hostname], check=True)

    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }), 200


@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    if not replicas:
        return jsonify({"error": "No replicas available"}), 503

    chosen_replica = replicas[hash(path) % len(replicas)]
    return jsonify({
        "path": path,
        "replica": chosen_replica
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
