# Customizable Load Balancer

## Overview

This project implements a customizable load balancer that routes requests from multiple clients to several server replicas, ensuring an even distribution of load. The load balancer employs consistent hashing to distribute client requests efficiently among server instances. The project is containerized using Docker and includes various endpoints to manage server replicas and monitor their status.

## Table of Contents
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Consistent Hashing](#consistent-hashing)
- [Analysis](#analysis)
- [References](#references)

## System Architecture

The system consists of a load balancer and multiple server replicas, all running within a Docker network. The load balancer exposes endpoints to interact with the server replicas, handle client requests, and manage server failures.

<!-- Add the correct path to the system diagram -->

## Installation

### Prerequisites
- **OS:** Ubuntu 20.04 LTS or above
- **Docker:** Version 20.10.23 or above
- **Programming Languages:** Python (preferred), C++, Java, or any other language of your choice

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/GMwanda/Load-Balancer.git
    cd Load-Balancer
    ```

2. Build the Docker images:
    ```sh
    docker-compose build
    ```

3. Deploy the application:
    ```sh
    docker-compose up
    ```

## Usage

### Starting the Load Balancer

To start the load balancer and the server replicas, run:
```sh
make start
```

### Stopping the Load Balancer

To stop the load balancer and the server replicas, run:
```sh
make stop
```

### Cleaning Up

To remove all containers and networks, run:
```sh
make clean
```
### Screenshots of System Running on Ubuntu Terminal
The screenshots below were taken as per the steps above
![image](https://github.com/user-attachments/assets/7ea9b8ec-1fab-4b32-863e-bf1a7f256103)
![image](https://github.com/user-attachments/assets/db1102e8-b423-4254-8a0b-1e076c3c1fe1)
![image](https://github.com/user-attachments/assets/ec5a1413-09dd-4f21-a176-83cb82373c1b)


## Endpoints

### Load Balancer Endpoints

- **`/rep` (GET):** Returns the status of the replicas managed by the load balancer.
    ```json
    Response:
    {
        "message": {
            "N": 3,
            "replicas": ["Server 1", "Server 2", "Server 3"]
        },
        "status": "successful"
    }
    ```

- **`/add` (POST):** Adds new server instances.
    ```json
    Request:
    {
        "n": 4,
        "hostnames": ["S5", "S4", "S10", "S11"]
    }

    Response:
    {
        "message": {
            "N": 7,
            "replicas": ["Server 1", "Server 2", "Server 3", "S5", "S4", "S10", "S11"]
        },
        "status": "successful"
    }
    ```

- **`/rm` (DELETE):** Removes server instances.
    ```json
    Request:
    {
        "n": 2,
        "hostnames": ["S5", "S4"]
    }

    Response:
    {
        "message": {
            "N": 4,
            "replicas": ["Server 1", "Server 3", "S10", "S11"]
        },
        "status": "successful"
    }
    ```

- **`/<path>` (GET):** Routes the request to a server replica. Example: `/home`
    ```json
    Response:
    {
        "message": "Hello from Server: 3",
        "status": "successful"
    }
    ```

### Server Endpoints

- **`/home` (GET):** Returns a string with the unique identifier of the server instance.
    ```json
    Response:
    {
        "message": "Hello from Server: [ID]",
        "status": "successful"
    }
    ```

- **`/heartbeat` (GET):** Sends heartbeat responses to monitor server status.
    ```json
    Response: [EMPTY]
    ```

## Consistent Hashing

The load balancer uses consistent hashing to evenly distribute client requests among server instances. The following parameters and hash functions are used:

- **Number of Server Containers (N):** 3
- **Total Number of Slots (#slots):** 512
- **Number of Virtual Servers per Server Container (K):** 9
- **Hash Function for Request Mapping (H(i)):** i + 2*i^2 + 17
- **Hash Function for Virtual Server Mapping (Φ(i, j)):** i + j + 2*j^2 + 25

### Implementation Details

- **Consistent Hash Map:** Maps client requests to server instances in a circular data structure to avoid data shifts during server addition or removal.
- **Server Addition:** Adds a new server instance and redistributes requests.
- **Server Failure:** Detects server failure using the `/heartbeat` endpoint and redistributes requests to maintain balanced load.
- **Virtual Servers:** Uses multiple virtual replicas for each server instance to ensure even load distribution.

## Analysis

### Performance Experiments

- **Load Distribution:** Launch 10,000 async requests on 3 server containers and visualize the request count handled by each server in a bar chart.

- **Scalability:** Increment the number of server containers from 2 to 6 and launch 10,000 requests at each increment. Plot the average load in a line chart.

- **Failure Recovery:** Test all endpoints and demonstrate the load balancer's quick recovery from server failures.

- **Hash Function Modification:** Modify the hash functions and report observations on load distribution and scalability.

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Makefile Tutorial](https://makefiletutorial.com/)
- [Stanford Consistent Hashing Lecture](https://www.youtube.com/watch?v=Qjb7_1yhF2A)
- [Dynamic Load Balancing Algorithm](https://en.wikipedia.org/wiki/Load_balancing_(computing))
