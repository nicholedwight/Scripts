import json
import boto3
import time

client = boto3.client('servicecatalog')
products = {}

def get_provisioned_product():
    response = client.search_provisioned_products(
        AcceptLanguage='en',
        AccessLevelFilter={
            'Key': 'Account',
            'Value': 'self'
        },
        SortBy='name',
        SortOrder='ASCENDING',
        PageSize=100
    )
    
    for i in response['ProvisionedProducts']:
        product_str = json.dumps(i, default=str)
        product_dict = json.loads(product_str)
        products[i['Id']] = i['IdempotencyToken']
              
    delete_provisioned_product(products)
            
def delete_provisioned_product(products):
    for id, token in products.items():
        response = client.terminate_provisioned_product(
            ProvisionedProductId=id,
            TerminateToken=token,
            IgnoreErrors=False,
            AcceptLanguage='en',
            RetainPhysicalResources=False
        )
    print(response)

def lambda_handler(event, context):
    get_provisioned_product()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
