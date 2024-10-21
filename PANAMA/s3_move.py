import subprocess

def move_files(local_path, s3_path):
    try:
        subprocess.run(['aws', 's3', 'mv', local_path, s3_path, '--recursive'])
        print('Successfully Moved!')
    except:
        print('No html files to move / error')


