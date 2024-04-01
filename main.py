import requests
import threading
import time

TARGET_URL = "http://localhost:8080/food"
THREADS_LIMITS = 2
REQUESTS_PER_THREAD = 100
HEADERS = {
    "Content-Type": "application/json",
}


def do_request():
    for _ in range(REQUESTS_PER_THREAD):
        try:
            start_time = time.time()
            response = requests.get(TARGET_URL, headers=HEADERS)
            response.raise_for_status()
            end_time = time.time()
            print(f"Status: {response.status_code}, Time: {(end_time - start_time)}")
            request_log = f"[{time.ctime()}] - STATUS: {response.status_code}\n"

            with open("logs\\requests.txt", "a") as log:
                log.write(request_log)

        except requests.exceptions.RequestException as e:
            error_log = f"[{time.ctime()}] - {e}\n"

            print(f"Request failed: {e}")
            with open("logs\error.txt", "a") as log:
                log.write(error_log)


def start():
    threads = []
    with open("logs\\requests.txt", "a") as log:
        requested_url = f"\n\n===- Requests done in: {TARGET_URL} -===\n\n\n"
        log.write(requested_url)

    for i in range(THREADS_LIMITS):
        t = threading.Thread(target=do_request)
        t.daemon = True
        threads.append(t)

    for j in range(THREADS_LIMITS):
        threads[j].start()

    for k in range(THREADS_LIMITS):
        threads[k].join()

    with open("logs\\requests.txt", "a") as log:
        log.write("\n\n\n===============================================")


start()
