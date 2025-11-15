@echo off
echo Starting MLflow Model Registry with Docker Compose...

docker-compose up -d

echo.
echo Services starting...
echo MLflow UI: http://localhost:5000
echo API Docs: http://localhost:8000/docs
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down