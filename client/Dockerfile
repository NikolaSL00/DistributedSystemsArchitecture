FROM python:3.11

ENV LOAD_BALANCER_HOST=example.com
ENV LOAD_BALANCER_PORT=30000

# Install the required dependencies
RUN pip install requests

# Copy the Python client code into the container
COPY . .

# Start the client
CMD ["python", "main.py"]
