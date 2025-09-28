# Simple container for the API
FROM python:3.11-slim
WORKDIR /app
COPY api/ /app/api
COPY data/ /app/data
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" requests pydantic streamlit
ENV PORT=8080 API_KEY=dev-key DB_PATH=/app/data/calls.db
EXPOSE 8080
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8080"]
