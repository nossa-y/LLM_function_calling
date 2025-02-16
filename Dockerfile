# Use an official lightweight Python image.
FROM python:3.11.1-slim

# Set the working directory in the container.
WORKDIR /app

# Copy requirements and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code.
COPY . .

# Expose the port Streamlit runs on.
EXPOSE 8501

# Run the Streamlit app.
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
