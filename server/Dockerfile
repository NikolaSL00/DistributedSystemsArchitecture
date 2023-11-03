FROM python:3.11

ENV ALPHA_VANTAGE_API_KEY=your_api_key
ENV STOCK_API_PORT=18871
# Other environment variables

# Install the required dependencies
RUN pip install alpha_vantage redis flask

COPY . .

# Expose the port for the Flask app (matching STOCK_API_PORT)
EXPOSE 18871

# Start the server using Flask's development server
CMD ["python", "main.py"]
