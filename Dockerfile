FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the app
COPY . .



# Expose Flask port
EXPOSE 5000

# Set defaults (can be overridden at runtime)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Start Flask
CMD ["flask", "run"]
