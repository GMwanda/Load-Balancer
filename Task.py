import os
import math
from flask import Flask, request, jsonify
from ConsistentHash import ConsistentHashMap
import random
import string
import subprocess
import docker
import logging

app = Flask(__name__)

N = 3
SLOTS = 512  # Total number of slots in the consistent hash map
K = int(math.log2(SLOTS))  # Number of virtual servers for each server container

# Logs
logs = []

# Initialize Docker client
docker_client = docker.from_env()

# Initialize the consistent hash map
consistent_hash_map = ConsistentHashMap(num_servers=N, num_slots=SLOTS, num_virtual_servers=K)

# Assuming a simple in-memory structure to keep track of replicas
replicas = []

# Configure logging
logging.basicConfig(level=logging.INFO)


def random_hostname(length=10):
    """Generate a random hostname."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


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
        log_to_browser(f"Request {request_id} mapped to server {server_id}")
        return jsonify({"request_id": request_id, "mapped_server": server_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "N": len(replicas),
        "replicas": replicas
    })


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
                container = docker_client.containers.run(
                    "web_server_image",
                    name=hostname,
                    detach=True,
                    restart_policy={"Name": "always"},
                    command=["gunicorn", "-b", "0.0.0.0:5000", "Task:app"],
                    volumes={'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'}}
                )

                new_replicas.append(container.name)
                logging.info(f"Started new container: {container.name}")
            except Exception as e:
                # Log and return an error if container creation fails
                logging.error(f"Failed to start new container: {str(e)}")
                return jsonify({"error": f"Failed to start new container: {str(e)}"}), 500

        # Update the global replicas list
        replicas.extend(new_replicas)
        logging.info(f"Total replicas: {len(replicas)}")

        # Reinitialize ConsistentHashMap with the updated number of servers
        try:
            num_servers = len(replicas)
            consistent_hash_map = ConsistentHashMap(num_servers=num_servers, num_slots=SLOTS, num_virtual_servers=K)
        except Exception as e:
            # Log and return an error if ConsistentHashMap initialization fails
            logging.error(f"Failed to initialize ConsistentHashMap: {str(e)}")
            return jsonify({"error": f"Failed to initialize ConsistentHashMap: {str(e)}"}), 500

        # Convert replicas list to JSON serializable format
        replicas_json = list(replicas)

        return jsonify({
            "message": {
                "N": len(replicas_json),
                "replicas": replicas_json
            },
            "status": "successful"
        }), 200

    except Exception as e:
        # General exception handler for any other errors
        logging.error(f"Internal Server Error: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@app.route('/rm/<int:n>', methods=['DELETE'])
def remove_replicas(n):
    global replicas

    logging.info(f"Received request to remove {n} replicas")

    # Validate input
    if n <= 0:
        logging.error("The number of replicas to remove must be greater than zero")
        return jsonify({"error": "The number of replicas to remove must be greater than zero"}), 400

    if n > len(replicas):
        logging.error("The number of replicas to remove exceeds the number of available replicas")
        return jsonify({"error": "The number of replicas to remove exceeds the number of available replicas"}), 400

    # Select replicas to remove
    to_remove = random.sample(replicas, n)
    logging.info(f"Selected replicas to remove: {to_remove}")

    successfully_removed = []

    for hostname in to_remove:
        try:
            logging.info(f"Stopping container {hostname}")
            stop_result = subprocess.run(["docker", "stop", hostname], check=True, capture_output=True, text=True)
            logging.info(f"Stop result: {stop_result.stdout.strip()} {stop_result.stderr.strip()}")

            logging.info(f"Removing container {hostname}")
            remove_result = subprocess.run(["docker", "rm", hostname], check=True, capture_output=True, text=True)
            logging.info(f"Remove result: {remove_result.stdout.strip()} {remove_result.stderr.strip()}")

            replicas.remove(hostname)
            successfully_removed.append(hostname)
        except subprocess.CalledProcessError as e:
            error_message = f"Failed to remove container {hostname}: {str(e)}. Output: {e.output.strip()}"
            logging.error(error_message)
            return jsonify({"error": error_message}), 500

    if not successfully_removed:
        return jsonify({"error": "No replicas were removed"}), 400

    logging.info("Replicas removed successfully")

    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas,
            "removed": successfully_removed
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
