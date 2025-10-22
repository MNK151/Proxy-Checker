import threading
import queue
import requests

q = queue.Queue()
valid_proxies = []

# Load proxies into the queue
with open(r"C:\Users\Tejj\Desktop\Python Parsing\Proxy\proxy.txt", "r") as f:
    proxies = f.read().splitlines()
    for p in proxies:
        q.put(p)

def check_proxies():
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json", 
                               proxies={"http": proxy, "https": proxy},
                               timeout=5)
            if res.status_code == 200:
                print(f"{proxy}")
                valid_proxies.append(proxy)
        except requests.RequestException as e:
            print(f"❌ Failed proxy: {proxy} - {e}")
        finally:
            q.task_done()

# Start threads
threads = []
for _ in range(10):
    t = threading.Thread(target=check_proxies)
    t.start()
    threads.append(t)

# Wait for all threads to finish
for t in threads:
    t.join()

# Optional: Save working proxies
with open("working_proxies.txt", "w") as f:
    for proxy in valid_proxies:
        f.write(proxy + "\n")
