# 1. Base Image (Official Python)
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install the package and its runtime dependencies
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir .

# 4. Copy the model checkpoint and other runtime assets
COPY model ./model

# 4. Train the model inside the container (Optional, ensures fresh model)
# RUN python data/generate_expert_data.py
# RUN python train.py

# 5. Expose the port
EXPOSE 8000

# 6. Run the API
CMD ["uvicorn", "stylerslm.api:app", "--host", "0.0.0.0", "--port", "8000"]
