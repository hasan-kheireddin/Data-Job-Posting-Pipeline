import boto3

s3 = boto3.client('s3')
# s3.upload_file("data/yourfile.csv", "yourname-data-pipeline-2026", "raw/yourfile.csv")
s3.upload_file('ai-ds-job-salaries', 'ai_ds_job_salaries_2026.csv', 'raw/ai_ds_job_salaries_2026.csv')
print("File uploaded successfully to S3 bucket.")