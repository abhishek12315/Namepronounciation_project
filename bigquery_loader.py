from google.cloud import bigquery
import io
import tempfile
import json

#%%
class BigQueryLoader:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path

    def create_bigquery_table(self, dataset_name, table_name):
        bigquery_client = bigquery.Client.from_service_account_json(self.credentials_path)
        dataset_ref = bigquery_client.dataset(dataset_name)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = 'US'  # Set the location of the dataset
        try: 
            dataset = bigquery_client.create_dataset(dataset)
        except:
            print("Bigquerry Dataset already exists")

        schema = [
            bigquery.SchemaField('UM_ID_Number', 'STRING'),
            bigquery.SchemaField('Full_Name', 'STRING'),
            bigquery.SchemaField('University_Mail_ID', 'STRING'),
            bigquery.SchemaField('Major', 'STRING'),
            bigquery.SchemaField('School', 'STRING')
        ]

        table_ref = dataset.table(table_name)
        table = bigquery.Table(table_ref, schema=schema)
        try:
            table = bigquery_client.create_table(table)
        except:
            print("Bigquerry table already exists")

        print('BigQuery table created.')

    def transform_responses(self, responses):
        transformed_responses = []
        for item in responses['responses']:
            transformed_item = {}
            answers = item['answers']
            transformed_item['UM_ID_Number'] = answers['0e0e5a68']['textAnswers']['answers'][0]['value']
            transformed_item['Full_Name'] = answers['5bef89a7']['textAnswers']['answers'][0]['value']
            transformed_item['University_Mail_ID'] = answers['69a71cb8']['textAnswers']['answers'][0]['value']
            transformed_item['Major'] = answers['6dd4e876']['textAnswers']['answers'][0]['value']
            transformed_item['School'] = answers['7e371c19']['textAnswers']['answers'][0]['value']
            transformed_responses.append(transformed_item)
        return transformed_responses

    def load_data_into_bigquery(self, dataset_name, table_name, transformed_responses):
        bigquery_client = bigquery.Client.from_service_account_json(self.credentials_path)
        dataset_ref = bigquery_client.dataset(dataset_name)
        table_ref = dataset_ref.table(table_name)

        # Check if the data already exists in the table using UMID
        umids = [response['UM_ID_Number'] for response in transformed_responses]
        umid_condition = " OR ".join([f"UM_ID_Number = '{umid}'" for umid in umids])
        query = f"SELECT COUNT(*) AS count FROM `{dataset_name}.{table_name}` WHERE {umid_condition}"
        query_job = bigquery_client.query(query)
        result = query_job.result().total_rows

        if result > 0:
            # Delete the existing rows with the same UMIDs
            print(f"The data available with associated {umid_condition}, Now its replaced with latest information.")
            delete_query = f"DELETE FROM `{dataset_name}.{table_name}` WHERE {umid_condition}"
            delete_job = bigquery_client.query(delete_query)
            delete_job.result()

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  # Append the data

        # Convert responses to newline-delimited JSON string
        data = '\n'.join([json.dumps(response) for response in transformed_responses])

        # Load the data into BigQuery
        load_job = bigquery_client.load_table_from_file(io.StringIO(data), table_ref, job_config=job_config)
        load_job.result()

        print('Data loaded into BigQuery.')