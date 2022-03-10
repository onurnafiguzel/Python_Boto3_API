from config import config
from flask import Flask, make_response, request, jsonify
import logging
import boto3
import botocore

app=Flask(__name__)
logging.basicConfig(
    filename=config['log_file'],
    level=config['log_level']
)

def get_client(aws_access_key_id, aws_secret_access_key,region_name ):   

    client=boto3.client('ec2',
    aws_access_key_id= aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
    )
    return client

def get_parameter(key):
    if (request.is_json):
        json_data=request.get_json()
        return json_data[key]

    return request.args[key]

@app.route("/ec2/list",methods=["GET"])
def list_instances():    
    instance_list = []
    try:
        aws_access_key_id = get_parameter("access_key")
        aws_secret_access_key=get_parameter("secret_key")
        region_name = get_parameter("region")
    except (KeyError,ValueError):
        return make_response(jsonify({"Message" : "access_key, secret_key and region are required"}),400)
    
    client = get_client(aws_access_key_id,aws_secret_access_key,region_name )

    try:        
        response = client.describe_instances()
    except botocore.exceptions.ClientError:
         return make_response(jsonify({"Message" : "AWS was not able to validate the provided access credentials"}),400)   

    for instance in range(len(response["Reservations"])):
        instance_list.append(response["Reservations"][instance]["Instances"][0]["InstanceId"])
    if instance_list==[]:
        return make_response(jsonify({"Message":"Not instance found!"},404))    
    return make_response(jsonify(instance_list),200)

@app.route("/ec2/start",methods=["POST"])
def start_instances():
    try:
        aws_access_key_id = get_parameter("access_key")
        aws_secret_access_key=get_parameter("secret_key")
        region_name = get_parameter("region")
        instance_Ids=get_parameter("instance_id")
    except (KeyError,ValueError):
        return make_response(jsonify({"Message" : "access_key, secret_key, instance_id and region are required"}),400)
    
    client = get_client(aws_access_key_id,aws_secret_access_key,region_name)
    try:        
        response=client.start_instances(
        InstanceIds= [instance_Ids])

    except botocore.exceptions.ClientError:
        return make_response(jsonify({"Message" : "AWS was not able to validate the provided access credentials"}),400)       

    return jsonify({
        "CurrentState" : response["StartingInstances"][0]["CurrentState"]["Name"],
        "PreviousState" : response["StartingInstances"][0]["PreviousState"]["Name"],
    })

@app.route("/ec2/stop",methods=["POST"])
def stop_instances():
    try:
        aws_access_key_id = get_parameter("access_key")
        aws_secret_access_key=get_parameter("secret_key")
        region_name = get_parameter("region")
        instance_Ids=get_parameter("instance_id")
    except (KeyError,ValueError):
        return make_response(jsonify({"Message" : "access_key, secret_key, instance_id and region are required"}),400)

    client = get_client(aws_access_key_id,aws_secret_access_key,region_name)
    try:        
        response=client.start_instances(
        InstanceIds= [instance_Ids])

    except botocore.exceptions.ClientError:
        return make_response(jsonify({"Message" : "AWS was not able to validate the provided access credentials"}),400)       

    response=client.stop_instances(
        InstanceIds= [instance_Ids]
    )
       
    return make_response(jsonify({
        "CurrentState" : response["StoppingInstances"][0]["CurrentState"]["Name"],
        "PreviousState" : response["StoppingInstances"][0]["PreviousState"]["Name"],
    }),200)    

if __name__ == "__main__":
    app.run(host=config["host"], port=config["port"], debug=True)