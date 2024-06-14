import os
import math
from flask import Flask, request, jsonify
from ConsistentHash import ConsistentHashMap
import random
import string
import subprocess
import docker
from flask_socketio import SocketIO
import logging

app = Flask(__name__)

N = 0
SLOTS = 512  # Total number of slots in the consistent hash map
K = int(math.log2(SLOTS))  # Number of virtual servers for each server container

# Logs
logs = []

# Initialize the consistent hash map
consistent_hash_map = ConsistentHashMap(num_servers=N, num_slots=SLOTS, num_virtual_servers=K)


@app.route('/home', methods=['GET'])
def home():
    server_id = os.environ.get('SERVER_ID', 'Unknown')
    return jsonify({"message": f"Hello from Server: {server_id}", "status": "successful"}), 200


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return "Hello 200"


@app.route('/map_request', methods=['GET'])
def map_request():
    request_id = request.args.get('id', type=int)
    print(request_id)

    if request_id is None:
        return jsonify({"error": "Request ID is required"}), 400
    try:
        server_id = consistent_hash_map.map_request()
        log_to_browser(jsonify({"request_id": request_id, "mapped_server": server_id}))
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

# Configure logging
logging.basicConfig(level=logging.INFO)


def random_hostname(length=10):
    """Generate a random hostname."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


@app.route('/add_servers/<int:n>', methods=['POST'])
def add_replicas(n):
    try:
        # Generate hostnames
        hostnames = [random_hostname() for _ in range(n)]
        logging.info(f"Generated hostnames: {hostnames}")

        new_replicas = []

        # Iterate to create the requested number of replicas
        for hostname in hostnames:
            logging.info(f"Using hostname: {hostname}")

            try:
                # Run a new container
                container = docker_client.containers.run("web_server_image", name=hostname, detach=True)
                new_replicas.append(container.name)
                logging.info(f"Started new container: {container.name}")
            except Exception as e:
                logging.error(f"Failed to start new container: {str(e)}")
                return jsonify({"error": f"Failed to start new container: {str(e)}"}), 500

        # Update the global replicas list
        replicas.extend(new_replicas)
        logging.info(f"Total replicas: {len(replicas)}")

        N = len(replicas)

        return jsonify({
            "message": {
                "N": len(replicas),
                "replicas": replicas
            },
            "status": "successful"
        }), 200

    except Exception as e:
        logging.error(f"Internal Server Error: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@app.route('/rm/<int:n>', methods=['DELETE'])
def remove_replicas(n):
    data = request.get_json()
    hostnames = data.get("hostnames", [])

    # Validate input
    if n <= 0 and not hostnames:
        return jsonify({"error": "Either 'n' or 'hostnames' must be specified"}), 400

    if len(hostnames) > n:
        return jsonify({"error": "Number of hostnames exceeds number of instances to remove"}), 400

    to_remove = set(hostnames)

    # If more instances need to be removed, add random instances
    if n > len(hostnames):
        remaining_count = n - len(hostnames)
        additional_replicas = random.sample(replicas, min(remaining_count, len(replicas) - len(hostnames)))
        to_remove.update(additional_replicas)

    for hostname in to_remove:
        if hostname in replicas:
            replicas.remove(hostname)
            try:
                subprocess.run(["docker", "stop", hostname], check=True)
                subprocess.run(["docker", "rm", hostname], check=True)
            except subprocess.CalledProcessError as e:
                log_to_browser(f"Failed to remove container {hostname}: {str(e)}")
                return jsonify({"error": f"Failed to remove container {hostname}: {str(e)}"}), 500

    log_to_browser("Replicas removed")
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }), 200



@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(logs)


def log_to_browser(message):
    logs.append(message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
