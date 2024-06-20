# multi-threading

import threading
import requests
from queue import Queue


def worker(queue):
    while not queue.empty():
        url = queue.get()
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Success: {url}")
            else:
                print(f"Failed: {url} with status code {response.status_code}")
        except requests.RequestException as e:
            print(f"Error: {url} with exception {e}")
        finally:
            queue.task_done()


def main(urls, num_threads):
    # Create a queue to hold the URLs
    queue = Queue()
    
    # Add URLs to the queue
    for url in urls:
        queue.put(url)
    
    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(queue,))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    print("All tasks are done.")

if __name__ == "__main__":
    urls = [
        "https://example.com/api/1",
        "https://example.com/api/2",
        "https://example.com/api/3",
        # Add more URLs as needed
    ]
    num_threads = 5  # Adjust the number of threads based on your requirements
    main(urls, num_threads)
