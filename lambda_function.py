import json
import boto3
import os

import xlwt
import sys

from S3 import s3
from SSM_PARAMETER import ssm_parameter

def lambda_handler(event, context):
    
    # Get Bucket name and File Name from S3 Put event.    
    bucketName = event['Records'][0]['s3']['bucket']['name']
    filePath = event['Records'][0]['s3']['object']['key']
    
    # create ssm Client.
    ssmClient = boto3.client('ssm')
    
    # Create s3 class object.
    s3_object = s3(bucketName, filePath)
    
    # Read xls file.
    file_content = s3_object.read_content()
    
    if file_content is not None:
        
        # Read paramter name and value.
        parameter_list = s3_object.read_xls_file(file_content)

    if parameter_list is not None:
        
        for parameter in parameter_list:
            
            # Create ssm_parameter class object.
            ssm_parameter_object = ssm_parameter(parameter['parameter_name'],parameter['parameter_value'])
            
            # Check whether parameter is already present or not.
            result = ssm_parameter_object.check_parameter()
            
            if 'Parameter' in result:
                
                if 'Value' in result['Parameter']:
                    
                    if result['Parameter']['Value'] == ssm_parameter_object.get_parameter_value():
                
                        print('Parameter ', parameter['parameter_name'], ' is already present with value ', result['Parameter']['Value'])
            
                    else:
                        
                        # Create ssm parameter.
                        result = ssm_parameter_object.create_parameter()
                        
                        if 'Version' in result:
                            
                            print('Parameter ', parameter['parameter_name'],' override with version: ',  result['Version'])
            else:
                        
                result = ssm_parameter_object.create_parameter()
                
                if 'Version' in result:
                    
                    print('Parameter ', parameter['parameter_name'],' Created with version: ',  result['Version'])
        
    
    return {
        'body': 'Lambda Works!!!'
    }
