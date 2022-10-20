#python3 -m venv .venv to create a virtual enviroment with .venv name 
#then pip install flask
#flask run to run the app after the boiler plate
##For moaul exploratori testing INsombia is an amazing client as well as postman

##first we create our docker file
##then we run focker build -t name path-to-dockerfile -t means that we are tagging
##in this case build -t rest-apis-flask-python 
##from comand line we can run imagest (to container) with docker run -p 5005:5000 name
## we also can run -d to run it on bkacgroudn a a deamon   docker run -d -p 5005:5000 name
##5005:5000 means taht we ar fowarding the incommming request from 5005 local port to 5000 container port