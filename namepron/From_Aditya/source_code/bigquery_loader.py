# -*- coding: utf-8 -*-
"""
Created on Thu May 18 13:21:10 2023

@author: benda
"""

from google.cloud import bigquery
import io
import tempfile

#%%
class BigQueryLoader:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path

    def create_bigquery_table(self, dataset_name, table_name):
        bigquery_client = bigquery.Client.from_service_account_json(self.credentials_path)
        dataset_ref = bigquery_client.dataset(dataset_name)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = 'US'  # Set the location of the dataset
        dataset = bigquery_client.create_dataset(dataset)

        schema = [
            bigquery.SchemaField('UM_ID_Number', 'STRING'),
            bigquery.SchemaField('Full_Name', 'STRING'),
            bigquery.SchemaField('University_Mail_ID', 'STRING'),
            bigquery.SchemaField('Major', 'STRING'),
            bigquery.SchemaField('School', 'STRING')
        ]

        table_ref = dataset.table(table_name)
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)

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

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE  # Replace with desired write disposition

        # Convert responses to newline-delimited JSON string
        data = '\n'.join([str(response) for response in transformed_responses])

        # Create an in-memory file-like object
        file_obj = io.StringIO(data)

        # Create a temporary file to write the data
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(data)
            temp_file.close()

            # Load data from the temporary file
            with open(temp_file.name, 'rb') as file:
                load_job = bigquery_client.load_table_from_file(file, table_ref, job_config=job_config)
                load_job.result()

        load_job = bigquery_client.load_table_from_file(file_obj, table_ref, job_config=job_config)
        load_job.result()

        print('Data loaded into BigQuery.')