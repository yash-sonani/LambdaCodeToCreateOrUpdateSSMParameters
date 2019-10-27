import boto3
import xlrd
from xlrd.book import open_workbook_xls


class s3():
    
    def __init__(self,bucketName,filePath):
        
        self.__bucketName = bucketName
        self.__filePath = filePath
        self.__client = boto3.client('s3')
        
    
    def read_content(self):
        
        try:
            
            # Read File From S3 Bucket
            
            data = self.__client.get_object(Bucket=self.__bucketName, Key=self.__filePath)

            content = data['Body'].read()
            
            return content
            
        except Exception as e:
            
            print('Exception in Read S3 Contenet: ', str(e))
            return None
            
    def read_xls_file(self, s3_content):
        
        try:
            
            # Read xls File for ssm parameter Detail
            workbook = open_workbook_xls(file_contents=s3_content)
            sheet1 = workbook.sheet_by_index(0)
            
            data = []
            row = {}
            index = 1
            
            while(True):
                
                if (sheet1.nrows == index):
                    break
                
                row = {}
                row['parameter_name'] = sheet1.cell_value(index,0).strip()
                row['parameter_value'] = sheet1.cell_value(index,1).strip()
                
                data.append(row)
                
                index = index + 1
            
            return data
            
        except Exception as e:
            
            print('Exception in Read S3 Contenet: ', str(e))
            return None
            
