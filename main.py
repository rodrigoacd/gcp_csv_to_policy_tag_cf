from google.cloud import datacatalog_v1
from google.cloud import bigquery
import gcsfs
import pandas as pd
import os 

project_id = os.environ['project_id']
taxonomy_id = os.environ['taxonomy_id']

def policy_tag_schema(taxonomy_id):

    ptm_client = datacatalog_v1.PolicyTagManagerClient()
    
    request = datacatalog_v1.ListPolicyTagsRequest(
        parent=taxonomy_id
    )
    print(request)
    try:
        page_result = ptm_client.list_policy_tags(request=request)
    except Exception as e:
        print('Unable to retrieve the policy tag taxonomy for taxonomy_id ' + taxonomy_id + '. Error message: ', e)
        return 'error'    

    policy_tag_names = [] # list of fully qualified policy tag names and sensitive categories

    for response in page_result:
        policy_tag_names.append((response.name, response.display_name))

    return policy_tag_names






def main(event, context):
    fileName=event['name']
    bucketName=event['bucket']
    
    dataList=fileName.split("/")
    tableProject=dataList[0]
    fileName=dataList[1]

    ### Reading bucket file
    print (f"gs://{ bucketName }/{ tableProject }/{ fileName }")
    fs = gcsfs.GCSFileSystem(project=project_id, mode="r")
    with fs.open(f"gs://{ bucketName }/{ tableProject }/{ fileName }") as f:
        df = pd.read_csv(f, delimiter=';',on_bad_lines='skip')
    ### End reading bucket file

    ### Reading taxonomy
    policy_tag_names = policy_tag_schema(taxonomy_id)
    #print (policy_tag_names)
    
    policy_tag_requests = []    # to store the list of fully qualified policy tag names and table column names, 
    
                                # so that we can create the policy tags on the various columns
    table = ''
    for index, row in df.iterrows():

        ### adding column + policy tag name 
        for policy_tag_name, policy_tag_category in policy_tag_names:
            if policy_tag_category == row['Etiqueta_seguridad']:
                policy_tag_requests.append((row['column'], policy_tag_name)) 

        print(policy_tag_requests)

        print( f"{ tableProject }.{row['dataset']}.{row['table']}")
        
        apply_policy_tags(f"{ tableProject }.{row['dataset']}.{row['table']}",policy_tag_requests)
        #apply_policy_tags(f"{ tableProject }.poc_catalog_policy.poc_policy_tag",policy_tag_requests)



def apply_policy_tags(uri, policy_tag_requests):
    
    print('enter apply_policy_tags')

    bq_client = bigquery.Client()

    table_id = uri.replace('/datasets/', '.').replace('/tables/', '.')
    table = bq_client.get_table(table_id) 
    schema = table.schema
    new_schema = []
    
    for field in schema:
        
        field_match = False
        
        for column, policy_tag_name in policy_tag_requests:
            
            if field.name == column:
                
                policy = bigquery.schema.PolicyTagList(names=[policy_tag_name,])
                new_schema.append(bigquery.schema.SchemaField(field.name, field.field_type, field.mode, policy_tags=policy)) 
                field_match = True
                break
    
        if field_match == False:    
            new_schema.append(field)
            
    table.schema = new_schema
    print (table.schema)
    table = bq_client.update_table(table, ["schema"])  

