FROM python:3.10
##base image
EXPOSE 5000
##port to run the flask app
WORKDIR /app
##Then we copy the app.py on the image stora to be abble to use it on the /app directory
RUN pip install flask
COPY . .
#here we ar coping from our file system to images file system
# we are coping all . to current folder. that o this case are /app
CMD ["flask", "run", "--host", "0.0.0.0"]
##here we give some instructions tu run 