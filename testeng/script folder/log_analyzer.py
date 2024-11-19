import re
from collections import Counter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log file path
LOG_FILE = '/path/to/your/web/server/log'

def analyze_log():
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    page_pattern = r'GET (\S+) HTTP/\d\.\d'
    status_pattern = r'" (\d{3}) '

    ip_addresses = []
    pages = []
    status_codes = []

    with open(LOG_FILE, 'r') as file:
        for line in file:
            ip = re.search(ip_pattern, line)
            if ip:
                ip_addresses.append(ip.group())

            page = re.search(page_pattern, line)
            if page:
                pages.append(page.group(1))

            status = re.search(status_pattern, line)
            if status:
                status_codes.append(status.group(1))

    # Analyze data
    total_requests = len(ip_addresses)
    unique_ips = len(set(ip_addresses))
    top_ips = Counter(ip_addresses).most_common(5)
    top_pages = Counter(pages).most_common(5)
    error_404 = status_codes.count('404')

    # Log results
    logging.info(f"Total requests: {total_requests}")
    logging.info(f"Unique IP addresses: {unique_ips}")
    logging.info("Top 5 IP addresses:")
    for ip, count in top_ips:
        logging.info(f"  {ip}: {count}")
    logging.info("Top 5 requested pages:")
    for page, count in top_pages:
        logging.info(f"  {page}: {count}")
    logging.info(f"404 errors: {error_404}")

if __name__ == "__main__":
    analyze_log()