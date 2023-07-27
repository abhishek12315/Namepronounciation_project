from google.cloud import bigquery
from google.oauth2 import service_account
import io
import json

#%%
class BigQueryDataLoader:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path

    def load_data_into_bigquery(self, dataset_name, table_name, name, email_id, umid, degree, school):
        bigquery_client = bigquery.Client.from_service_account_json(self.credentials_path)
        dataset_ref = bigquery_client.dataset(dataset_name)
        table_ref = dataset_ref.table(table_name)

        # Check if the data already exists in the table
        query = f"SELECT * FROM `{dataset_name}.{table_name}` WHERE CAST(UM_ID_Number AS STRING) = '{umid}'"
        query_job = bigquery_client.query(query)
        results = query_job.result()

        if len(list(results)) > 0:
            # Delete the existing row(s) with the same data
            print(f"The data available with associated {umid}, Now its replaced with latest information.\n")
            delete_query = f"DELETE FROM `{dataset_name}.{table_name}` WHERE CAST(UM_ID_Number AS STRING) = '{umid}'"
            delete_job = bigquery_client.query(delete_query)
            delete_job.result()

        # Prepare the data to be loaded into BigQuery
        rows_to_insert = [
            {
                'UM_ID_Number': umid,
                'Full_name': name,
                'University_Mail_ID': email_id,
                'Major': degree,
                'School': school
            }
        ]

        # Convert the rows to newline-delimited JSON string
        data = '\n'.join([json.dumps(row) for row in rows_to_insert])

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND  # Append the row if it already exists

        # Load the data into BigQuery
        load_job = bigquery_client.load_table_from_file(io.StringIO(data), table_ref, job_config=job_config)
        load_job.result()

        print('Data loaded into BigQuery.')

