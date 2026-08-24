import boto3

s3 = boto3.client('s3')
# s3.download_file("data/yourfile.csv", "yourname-data-pipeline", "yourfile.csv")
s3.download_file("data/yourfile.csv", "yourname-data-pipeline", "yourfile.csv")
print("File downloaded successfully from S3 bucket.")