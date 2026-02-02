# 1. Base Image (Official Python)
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 4. Train the model inside the container (Optional, ensures fresh model)
# RUN python data/generate_expert_data.py
# RUN python train.py

# 5. Expose the port
EXPOSE 8000

# 6. Run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
