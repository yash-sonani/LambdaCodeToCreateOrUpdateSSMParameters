import boto3

class ssm_parameter():
    
    def __init__(self,parameterName,parameterValue):
        
        self.__parameterName = parameterName
        self.__parameterValue = parameterValue
        self.__parameterType = 'String'
        self.__client = boto3.client('ssm')

    def get_parameter_value(self):
        
        return self.__parameterValue
    
    def check_parameter(self):
        
        try:
            response = self.__client.get_parameter(
                Name=self.__parameterName
            )
            
            print('check_parameter: ', response)
            
            return response
        
        except Exception as e:
            print('Exception inside check_parameter: ', str(e))
            return []
        
    def create_parameter(self):
        
      try:
        response = self.__client.put_parameter(
          Name=self.__parameterName,
          Value=self.__parameterValue,
          Type=self.__parameterType,
          Overwrite=True,
        )

        print('create_parameter: ', response)
        return response

      except Exception as e:
        print('Exception inside create_parameter: ', str(e))
      
    
      
