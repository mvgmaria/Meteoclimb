import threading
import queue
import requests
import random
from requests.exceptions import SSLError, ProxyError, Timeout, RequestException

# Initialize queue and list to store valid proxies
q = queue.Queue()
valid_proxies = []

# Load the proxy list from file
with open("PY/CLIMB/proxy_list.txt", "r") as f:
    proxies = f.read().splitlines()
    for p in proxies:
        q.put(p)

# List of user agents to rotate
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
]


# Proxy checker function
def check_proxies():
    global q, valid_proxies
    while not q.empty():
        proxy = q.get()
        try:
            # Set random user agent for each request
            headers = {"User-Agent": random.choice(user_agents)}

            # Test both HTTP and HTTPS protocols with SSL validation
            res = requests.get(
                "https://ipinfo.io/json",  # Use HTTPS to trigger SSL certificate validation
                proxies={"http": proxy, "https": proxy},
                headers=headers,
                timeout=5,
                verify=True,  # Ensure SSL certificates are verified
            )

            # Check if the proxy is working
            if res.status_code == 200:
                data = res.json()
                ip = data.get("ip", "Unknown")
                country = data.get("country", "Unknown")
                # Print only the proxies that work
                print(f"Working Proxy: {proxy} | IP: {ip} | Country: {country}")
                valid_proxies.append(proxy)  # Add valid proxy to list

                # Save valid proxies incrementally to avoid data loss in case of script interruption
                with open("PY/CLIMB/valid_proxies.txt", "a") as f:
                    f.write(proxy + "\n")

        except (SSLError, ProxyError, Timeout, RequestException):
            # Skip any printing for failed proxies
            pass
        finally:
            q.task_done()


# Start proxy checking with threading (10 threads)
for _ in range(10):
    threading.Thread(target=check_proxies).start()

# Wait for all threads to finish
q.join()

print("Proxy checking completed. Valid proxies are saved to valid_proxies.txt.")
