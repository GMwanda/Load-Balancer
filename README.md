---

# Flask Consistent Hash Map Application

This is a Flask application that implements a consistent hash map for distributing requests across multiple servers. The application provides endpoints for basic health checks and mapping requests to servers.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [License](#license)

## Prerequisites

Ensure you have the following installed:
- Python 3.9 or higher
- Docker

## Installation

1. **Clone the repository**:
   ```sh
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Running the Application Locally

1. **Set the `SERVER_ID` environment variable** (optional):
   ```sh
   export SERVER_ID="Server1"
   ```

2. **Run the Flask application**:
   ```sh
   python Task.py
   ```

### Running the Application with Docker

1. **Build the Docker image**:
   ```sh
   docker build -t flask-consistent-hash-map .
   ```

2. **Run the Docker container**:
   ```sh
   docker run -p 5000:5000 -e SERVER_ID="Server1" flask-consistent-hash-map
   ```

## Endpoints

### `/home` (GET)
Returns a greeting message with the server ID.

**Response**:
```json
{
  "message": "Hello from Server: <SERVER_ID>",
  "status": "successful"
}
```

### `/heartbeat` (GET)
Returns a simple health check message.

**Response**:
```
Hello
```

### `/map_request` (GET)
Maps a request ID to a server using the consistent hash map.

**Query Parameters**:
- `id` (integer): The request ID to be mapped.

**Response**:
```json
{
  "request_id": <request_id>,
  "mapped_server": <server_id>
}
```

**Error Response**:
```json
{
  "error": "Request ID is required"
}
```
or
```json
{
  "error": "<error_message>"
}
```

## Docker Setup

The Docker setup is defined in the `Dockerfile` and includes the following steps:

1. Use the Python 3.9-slim base image.
2. Set the working directory to `/app`.
3. Copy the application files to the working directory.
4. Install Flask using `pip`.
5. Expose port 5000.
6. Set the `SERVER_ID` environment variable.
7. Run the Flask application using the command `CMD ["python", "Task.py"]`.

## Environment Variables

- `SERVER_ID`: Specifies the ID of the server. Defaults to `DefaultServer` if not set.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
