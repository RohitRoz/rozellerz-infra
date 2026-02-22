#!/usr/bin/env python3
"""
Clean up manually-created AWS resources so CloudFormation can take over.
Run this BEFORE the first GHA deploy.

Usage: python scripts/cleanup_manual.py
"""
import boto3
import sys
import time

REGION = 'us-east-1'
BUCKET = 'rozellerz.com'
CF_DIST_ID = 'E2KM5K74FB5PS'  # your existing distribution

s3 = boto3.client('s3', region_name=REGION)
cf = boto3.client('cloudfront', region_name=REGION)


def empty_bucket(bucket):
    print(f'Emptying bucket: {bucket}')
    paginator = s3.get_paginator('list_object_versions')
    for page in paginator.paginate(Bucket=bucket):
        objects = []
        for v in page.get('Versions', []):
            objects.append({'Key': v['Key'], 'VersionId': v['VersionId']})
        for d in page.get('DeleteMarkers', []):
            objects.append({'Key': d['Key'], 'VersionId': d['VersionId']})
        if objects:
            s3.delete_objects(Bucket=bucket, Delete={'Objects': objects})
            print(f'  Deleted {len(objects)} objects/versions')
    print(f'  ✓ Bucket empty')


def disable_and_delete_distribution(dist_id):
    print(f'Disabling CloudFront distribution: {dist_id}')
    resp = cf.get_distribution_config(Id=dist_id)
    config = resp['DistributionConfig']
    etag = resp['ETag']

    if config['Enabled']:
        config['Enabled'] = False
        # Remove aliases to avoid conflict with new CF
        config['Aliases'] = {'Quantity': 0}
        if 'Items' in config.get('Aliases', {}):
            del config['Aliases']['Items']
        resp = cf.update_distribution(
            DistributionConfig=config,
            Id=dist_id,
            IfMatch=etag
        )
        etag = resp['ETag']
        print('  Waiting for distribution to disable (this takes ~5 min)...')
        waiter = cf.get_waiter('distribution_deployed')
        waiter.wait(Id=dist_id)

    print(f'  Deleting distribution...')
    cf.delete_distribution(Id=dist_id, IfMatch=etag)
    print(f'  ✓ Distribution deleted')


def delete_bucket(bucket):
    print(f'Deleting bucket: {bucket}')
    s3.delete_bucket(Bucket=bucket)
    print(f'  ✓ Bucket deleted')


def main():
    print('=== Cleaning up manually-created resources ===')
    print(f'Bucket: {BUCKET}')
    print(f'CloudFront: {CF_DIST_ID}')
    print()

    confirm = input('Type DELETE to confirm: ')
    if confirm != 'DELETE':
        print('Aborted.')
        sys.exit(1)

    print()
    try:
        empty_bucket(BUCKET)
        delete_bucket(BUCKET)
    except Exception as e:
        print(f'  Bucket error (may already be gone): {e}')

    try:
        disable_and_delete_distribution(CF_DIST_ID)
    except Exception as e:
        print(f'  CloudFront error (may already be gone): {e}')

    print()
    print('✓ Manual resources cleaned up.')
    print('  You can now run the GHA deploy workflow.')
    print('  The first deploy with seed_db=true will recreate everything via CloudFormation.')


if __name__ == '__main__':
    main()
