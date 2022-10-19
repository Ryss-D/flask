FROM python:3.10
#This is a pre-created image, published on the cloud(Docker-library)
EXPOSE 5000
WORKDIR /app
RUN pip install flask
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]