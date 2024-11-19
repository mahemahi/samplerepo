import os
import paramiko
import datetime
import logging

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# SSH connection details
REMOTE_HOST = 'your_remote_host'
REMOTE_USER = 'your_username'
REMOTE_PASSWORD = 'your_password'
REMOTE_PATH = '/path/to/remote/backup/directory'

# Local directory to backup
LOCAL_PATH = '/path/to/local/directory'

def create_ssh_client():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASSWORD)
    return client

def backup_directory():
    try:
        client = create_ssh_client()
        sftp = client.open_sftp()

        # Create a timestamp for the backup
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        remote_backup_path = f"{REMOTE_PATH}/backup_{timestamp}"

        # Create the remote backup directory
        sftp.mkdir(remote_backup_path)

        # Recursively upload files
        for root, dirs, files in os.walk(LOCAL_PATH):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, LOCAL_PATH)
                remote_file_path = os.path.join(remote_backup_path, relative_path)
                
                # Create remote directories if they don't exist
                remote_dir = os.path.dirname(remote_file_path)
                try:
                    sftp.stat(remote_dir)
                except FileNotFoundError:
                    sftp.mkdir(remote_dir)

                sftp.put(local_file_path, remote_file_path)

        logging.info(f"Backup completed successfully to {remote_backup_path}")
    except Exception as e:
        logging.error(f"Backup failed: {str(e)}")
    finally:
        sftp.close()
        client.close()

if __name__ == "__main__":
    backup_directory()