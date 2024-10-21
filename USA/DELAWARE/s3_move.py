import subprocess

def configure_aws(access_key_id, secret_access_key, region):

    aws_configure_command = [
        'aws',
        'configure',
        'set',
        'aws_access_key_id',
        access_key_id
    ]

    subprocess.run(aws_configure_command, check=True)

    aws_configure_command = [
        'aws',
        'configure',
        'set',
        'aws_secret_access_key',
        secret_access_key
    ]

    subprocess.run(aws_configure_command, check=True)

    aws_configure_command = [
        'aws',
        'configure',
        'set',
        'region',
        region
    ]

    subprocess.run(aws_configure_command, check=True)

def move_files(local_path, s3_path):
    try:
        subprocess.run(['aws', 's3', 'mv', local_path, s3_path, '--recursive'])
        print('Successfully Moved!')
    except:
        print('No html files to move / error')