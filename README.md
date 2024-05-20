# Flask Load Balancer with Consistent Hashing

This project implements a simple load balancer using Flask and Consistent Hashing. It supports dynamically adding and removing replicas (server containers) and provides endpoints to map requests to replicas based on consistent hashing.

## Features

- Consistent Hashing for request mapping
- Dynamic addition and removal of server replicas
- Docker integration for container management
- Simple API endpoints for interaction

## Requirements

- Docker
- Docker Compose
- Python 3.9+
- Flask

## Setup

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and run the Docker containers:**
   ```sh
   docker-compose up --build
   ```

3. **Verify the setup:**
   Open your browser or a tool like Postman and access the following URL:
   ```sh
   http://<host-ip>:5000/heartbeat
   ```
   You should receive a `Hello` response.

## API Endpoints

### 1. Home
- **URL:** `/home`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "message": "Hello from Server: <server_id>",
    "status": "successful"
  }
  ```

### 2. Heartbeat
- **URL:** `/heartbeat`
- **Method:** `GET`
- **Response:** `Hello`

### 3. Map Request
- **URL:** `/map_request`
- **Method:** `GET`
- **Params:** `id` (integer, required)
- **Response:**
  ```json
  {
    "request_id": <request_id>,
    "mapped_server": <server_id>
  }
  ```

### 4. Get Replicas
- **URL:** `/rep`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "N": <number_of_replicas>,
    "replicas": ["<replica1>", "<replica2>", ...]
  }
  ```

### 5. Add Replicas
- **URL:** `/add`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "n": <number_of_replicas_to_add>,
    "hostnames": ["<hostname1>", "<hostname2>", ...]  // Optional
  }
  ```
- **Response:**
  ```json
  {
    "message": {
      "N": <total_number_of_replicas>,
      "replicas": ["<replica1>", "<replica2>", ...]
    },
    "status": "successful"
  }
  ```

### 6. Remove Replicas
- **URL:** `/rm`
- **Method:** `DELETE`
- **Body:**
  ```json
  {
    "n": <number_of_replicas_to_remove>,
    "hostnames": ["<hostname1>", "<hostname2>", ...]  // Optional
  }
  ```
- **Response:**
  ```json
  {
    "message": {
      "N": <total_number_of_replicas>,
      "replicas": ["<remaining_replica1>", "<remaining_replica2>", ...]
    },
    "status": "successful"
  }
  ```

## Accessing the Endpoints from Another Device

Use the host machine's IP address to access the endpoints. For example:
   ```sh
   http://<host-ip>:5000/add
   ```

## Troubleshooting

1. **Docker Command Not Found:**
   Ensure Docker is installed and the Docker daemon is running. Verify by running:
   ```sh
   docker --version
   ```

2. **Port Access Issues:**
   Ensure no firewall or security software is blocking incoming connections on port 5000. Verify network configuration and connectivity between devices.

3. **Container Management Errors:**
   Ensure Docker Compose is properly set up and configured. Check the Docker Compose file for correct port mappings and volume mounts.
