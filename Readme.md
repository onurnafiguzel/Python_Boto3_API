# Python Boto3 Basic API
This project is used for listing of all instances also start and stop a specific instance of authenticated user.

## Usage
``python3 -m source /bin/activate
source env/bin/activate
python3 initial.py``

### First endpoint
* http://localhost:8080/ec2/stop?access_key=&secret_key=&region=eu-west-1&instance_id=
* http://localhost:8080/ec2/start?access_key=&secret_key=&region=eu-west-1&instance_id=

### Second endpoint, you can use them wih json body as below
* http://localhost:8080/ec2/stop
* http://localhost:8080/ec2/start
`{
    "access_key": ,
    "secret_key" : ,    
    "region" :"eu-west-1"
    "instance_id: 
}`