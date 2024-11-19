import requests
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Application URL
APP_URL = 'http://your-application-url.com'

# Check interval in seconds
CHECK_INTERVAL = 60

def check_application_health():
    try:
        response = requests.get(APP_URL)
        if response.status_code == 200:
            logging.info("Application is UP")
            return True
        else:
            logging.warning(f"Application is DOWN. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        logging.error(f"Failed to connect to the application: {str(e)}")
        return False

def main():
    while True:
        is_up = check_application_health()
        if not is_up:
            # You could add additional actions here, like sending an alert
            pass
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()