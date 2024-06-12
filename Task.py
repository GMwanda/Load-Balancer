import os
import math
from flask import Flask, request, jsonify
import random
import string
import subprocess
import docker
import logging

app = Flask(__name__)

# Constants for consistent hash map
N = 3  # Number of server containers
SLOTS = 512  # Total number of slots in the consistent hash map
K = int(math.log2(SLOTS))  # Number of virtual servers for each server container


class ConsistentHashMap:
    def __init__(self, num_servers, num_slots, num_virtual_servers):
        self.num_servers = num_servers
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.hash_map = [None] * num_slots
        self.servers = {i: [] for i in range(num_servers)}  # dictionary to hold server and their virtual servers

        self._initialize_virtual_servers()

    def _hash_request(self, i):
        return (i + 2 ** i + 17) % self.num_slots

    def _hash_virtual_server(self, server_id, virtual_id):
        return (server_id + virtual_id + 2 ** virtual_id + 25) % self.num_slots

    def _initialize_virtual_servers(self):
        for server_id in range(self.num_servers):
            for virtual_id in range(self.num_virtual_servers):
                slot = self._hash_virtual_server(server_id, virtual_id)
                original_slot = slot
                while self.hash_map[slot] is not None:
                    slot = (slot + 1) % self.num_slots
                    if slot == original_slot:
                        raise Exception("Hash map is full, cannot find emptyslot")
                self.hash_map[slot] = (server_id, virtual_id)
                self.servers[server_id].append(slot)

    def map_request(self, request_id):
        slot = self._hash_request(request_id)
        original_slot = slot
        while self.hash_map[slot] is None:
            slot = (slot + 1) % self.num_slots
            if slot == original_slot:
                raise Exception("No server available to handle the request")
        server_id, _ = self.hash_map[slot]
        return server_id


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

# Configure logging
logging.basicConfig(level=logging.INFO)


def random_hostname(length=10):
    """Generate a random hostname."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


@app.route('/add_servers/<int:n>', methods=['POST'])
def add_replicas(n):
    try:
        # Generate hostnames
        n = 1
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
