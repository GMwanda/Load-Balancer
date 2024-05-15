from flask import Flask, jsonify, request
import os
import math

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
                        raise Exception("Hash map is full, cannot find empty slot")
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)