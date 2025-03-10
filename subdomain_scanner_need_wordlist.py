#!/usr/bin/python3

from threading import Thread, Lock
from queue import Queue
import requests

queue = Queue()
list_lock = Lock()
discovered_subdomains = []

def scan_subdomains(domain):
    global queue
    while True:
        subdomain = queue.get()
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print("[+] Discovered subdomain:, url")
            with list_lock:
                discovered_subdomains.append(url)
        queue.task_done()

def main(domain, n_threads, subdomains):
    global queue

    for subdomain in subdomains:
        queue.put(subdomain)
    for t in range(n_threads):
        worker = Thread(target=scan_subdomains, args=(domain,))
        worker.daemon = True
        worker.start()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Subdomain scanner using threads")
    parser.add_argument("domain", help="domain to scan without protocol (http or https)")
    parser.add_argument("-l", "--wordlist", help="file with subdomains. default is subdomains.txt", default="subdomains.txt")
    parser.add_argument("-t", "--threads-count", help="number of threads to use. default is 10.", default=10, type=int)
    parser.add_argument("-o", "--out-file", help="specify the output file. default is discovered_subdomains.txt", default="discovered_subdomains.txt")

    args = parser.parse_args()
    domain = args.domain
    wordlist = args.wordlist
    threads_count = args.threads_count
    out_file = args.out_file

    main(domain=domain, n_threads=threads_count, subdomains=open(wordlist).read().splitlines())

    # save file
    with open(out_file, "w") as f:
        for url in discovered_subdomains:
            print(url, file=f)