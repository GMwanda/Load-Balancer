# Task 1 - Flask Application Dockerization

This project demonstrates how to Dockerize a Flask application, making it easy to deploy and run in a containerized environment.

## Prerequisites

- Docker: Ensure that Docker is installed on your system. You can download and install Docker from [here](https://www.docker.com/get-started).

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build the Docker image:
   ```bash
   docker build -t my-flask-app .
   ```

3. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 --name my-flask-container my-flask-app
   ```

4. Access the Flask application:
   Open a web browser and navigate to `http://localhost:5000` to access the Flask application running in the Docker container.

## Remote Access Instructions
- To access the Flask application remotely from another device on the same network.
- On Linux: Use the ifconfig or ip addr command to find the IP address associated with the network interface (e.g., wlp2s0, eth0).
- On Windows: Use the ipconfig command to find the IPv4 address associated with the active network adapter (Ethernet, Wi-Fi).
- Once you have the host machine's IP address, access the Flask application from another device's web browser using the following URL format:

   ```bash
   http://<host-ip>:5000
   ```

- Replace <host-ip> with the IP address of the host machine running Docker. You should now be able to access the Flask application remotely from any device on the same network.

## Customization

- **Python Script**: Modify the `Test.py` file to customize the Flask application logic and routes.
- **Dockerfile**: Customize the Dockerfile to include additional dependencies or configurations as needed.
- **Environment Variables**: You can set environment variables in the Dockerfile or when running the container to configure the Flask application.

## Troubleshooting

- If you encounter any issues during the Docker build or run process, refer to the error messages for troubleshooting guidance.
- Make sure that Docker is installed correctly and running on your system.

