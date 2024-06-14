class ConsistentHashMap:
    def __init__(self, num_servers, num_slots, num_virtual_servers):
        self.num_servers = num_servers
        self.num_slots = num_slots
        self.num_virtual_servers = num_virtual_servers
        self.hash_map = [None] * num_slots
        self.servers = {i: [] for i in range(num_servers)}  # dictionary to hold server and their virtual servers
        self.current_server_index = 0  # Keep track of the current server index

        self._initialize_virtual_servers()

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

    def map_request(self):
        # Map the request to the current server ID
        server_id = self.current_server_index

        # Update the current server index in a circular fashion
        self.current_server_index = (self.current_server_index + 1) % self.num_servers

        return server_id
