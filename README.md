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

## Customization

- **Python Script**: Modify the `Test.py` file to customize the Flask application logic and routes.
- **Dockerfile**: Customize the Dockerfile to include additional dependencies or configurations as needed.
- **Environment Variables**: You can set environment variables in the Dockerfile or when running the container to configure the Flask application.

## Troubleshooting

- If you encounter any issues during the Docker build or run process, refer to the error messages for troubleshooting guidance.
- Make sure that Docker is installed correctly and running on your system.
