
# 1. Base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy project files
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the code
COPY . .

# 6. Expose the port your app runs on (Render will map it)
EXPOSE 8000

# 7. Run your app
CMD ["python", "agent.py"]

