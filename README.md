# Flask Load Balancer with Consistent Hashing

This project implements a simple load balancer using Flask and Consistent Hashing. It supports dynamically adding and removing replicas (server containers) and provides endpoints to map requests to replicas based on consistent hashing.

## Features

- Consistent Hashing for request mapping
- Dynamic addition and removal of server replicas
- Docker integration for container management
- Simple API endpoints for interaction

## Requirements

- Git
- Make
- Docker
- Docker Compose
- Python 3.9+
- Flask

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Git
- Make
- Docker
- Docker Compose

## Installation

Follow these steps to get the project up and running:

### 1. Clone the Repository

Open your terminal and clone the repository:

```sh
git clone https://github.com/GMwanda/Load-Balancer.git
cd Load-Balancer
```

### 2. Install Make

If `make` is not installed, install it using the following command:

For Ubuntu/Debian:
```sh
sudo apt update
sudo apt install make
```

For MacOS:
```sh
brew install make
```

### 3. Install Docker

Follow the instructions on the [Docker website](https://docs.docker.com/get-docker/) to install Docker for your operating system.

For Ubuntu/Debian:
```sh
sudo apt update
sudo apt install docker.io
```

### 4. Install Docker Compose

Follow the instructions on the [Docker Compose website](https://docs.docker.com/compose/install/) to install Docker Compose.

For Ubuntu/Debian:
```sh
sudo apt install docker-compose
```

## Setup

1. **Build the Docker Image**

Run the following command to build the Docker image:

```sh
make build
```

2. **Run the Project**

Start the Docker containers using the following command:

```sh
make up
```

### Handling Errors

If you encounter errors, such as orphan containers, you can resolve them by running:

```sh
docker-compose down --remove-orphans
```

Then, rebuild and restart the containers using:

```sh
sudo make rebuild
```

## Accessing the Application

Once the containers are running, you can access the Flask application at `http://localhost:5000`.

## Stopping the Project

To stop the running containers, use:

```sh
make down
```

## Additional Makefile Commands

- **View Logs**:
  ```sh
  make logs
  ```

- **Run Containers in Detached Mode**:
  ```sh
  make up-detached
  ```

- **Stop Containers**:
  ```sh
  make stop
  ```

- **Remove Containers**:
  ```sh
  make rm
  ```

## Verify the Setup

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
      "N": <total_number_of replicas>,
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

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
```