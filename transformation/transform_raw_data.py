import boto3
import pandas as pd
import io
from datetime import datetime


class DataPipeline:
    def __init__(self, bucket_name, file_name):
        self.bucket_name = bucket_name
        self.file_name = file_name
        self.s3_client = boto3.client('s3')

    def read_csv_from_s3(self):
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.file_name)
        data = response['Body'].read()
        df = pd.read_csv(io.BytesIO(data))
        return df

    def upload_to_s3(self, body, key):
        self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=body)

    def clean_data(self, df):
        # Remove duplicates
        df = df.drop_duplicates()

        # Cast salary to numeric, drop rows where it's missing/invalid
        df['salary_usd'] = pd.to_numeric(df['salary_usd'], errors='coerce')
        df = df.dropna(subset=['salary_usd', 'job_title', 'experience_level'])

        # Normalize text columns so Athena GROUP BY doesn't split on casing/whitespace
        df['job_title'] = df['job_title'].str.strip().str.title()
        df['experience_level'] = df['experience_level'].str.strip().str.title()

        # Derive work_mode from remote_ratio so Athena can GROUP BY it directly
        df['work_mode'] = df['remote_ratio'].map(
            lambda x: 'remote' if x == 100 else 'onsite' if x == 0 else 'hybrid'
        )

        # Remove columns not needed
        columns_to_remove = ['company_size', 'company_location', 'education', 'has_ml_in_title',
                              'manages_people', 'team_size', 'certifications_count',
                              'uses_ai_tools_daily', 'ai_tools_hours_per_week', 'salary_currency',
                              'equity_offered_pct', 'bonus_pct', 'job_satisfaction_score',
                              'interviews_to_offer', 'switched_jobs_last_year',
                              'upskilling_hours_per_month', 'fears_ai_automation_score']
        df = df.drop(columns=[c for c in columns_to_remove if c in df.columns])

        return df

    def upload_transformed_data(self):
        df = self.read_csv_from_s3()
        df_cleaned = self.clean_data(df)

        quality_summary = {
            "file": self.file_name,
            "rows_in": len(df),
            "rows_out": len(df_cleaned),
            "rows_dropped": len(df) - len(df_cleaned),
            "processed_at": datetime.utcnow().isoformat()
        }
        print(quality_summary)  # visible in CloudWatch Logs

        out_key = self.file_name.replace('raw/', 'processed/').replace('.csv', '.parquet')
        out_buffer = io.BytesIO()
        df_cleaned.to_parquet(out_buffer, index=False)
        self.upload_to_s3(out_buffer.getvalue(), out_key)

        return quality_summary
