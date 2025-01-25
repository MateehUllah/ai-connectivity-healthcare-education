FROM python:3.9-slim AS backend
WORKDIR /app
COPY backend/ /app
RUN pip install -r requirements.txt

# Frontend setup
FROM node:16 AS frontend
WORKDIR /frontend
COPY frontend/ /frontend
RUN npm install
RUN npm run build

# Combine both
FROM python:3.9-slim
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /frontend/build /app/frontend
CMD ["python", "app.py"]
