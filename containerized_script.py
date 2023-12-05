import os

import boto3
import click
from dagster_pipes import open_dagster_pipes


@click.command()
@click.option('--obj', 'key', help="S3 object to read in as input", type=str, required=True)
def main(key: str = None):
    session = boto3.session.Session()
    bucket = os.environ['AWS_BUCKET']
    client = session.client(
        service_name='s3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        endpoint_url=os.environ['AWS_ENDPOINT_URL'],
    )

    # get the s3_obj from the bucket
    s3_obj = client.get_object(Bucket=bucket, Key=key)
    # read the contents of the object
    s3_obj = s3_obj['Body'].read().decode('utf-8')
    # write the contents to a new object with the suffix "_processed"
    client.put_object(Bucket=bucket, Key=key + "_processed", Body=s3_obj)

    with open_dagster_pipes() as pipes:
        pipes.log.info(f"[CONTAINER] Read in {key} from S3, from bucket {bucket}")
        pipes.log.info(f"[CONTAINER] Processed {key} and wrote to {key}_processed")
        pipes.report_asset_materialization(
            metadata={"key": key, "bucket": bucket, "processed_key": key + "_processed"},
            asset_key=key + "_processed",
        )


if __name__ == '__main__':
    main()
