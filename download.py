import os
import sys
import urllib3
import requests 
from time import time
from multiprocessing.pool import ThreadPool
import ssl
import concurrent.futures

ssl._create_default_https_context = ssl._create_unverified_context

start = time()

args = sys.argv
dirname = "files"
playlist_data = ""
urls = []

hostname = "https://wssd32.fastcdn.stream/hls/lnhont5qfx5ee35huvlkcjveio54mvgqbte2ok2dh3hlnzw5gz7idj3rdtdq/"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

s = requests.Session()
s.verify = False

if len(args) > 1 and args[1] is not None:
    dirname = args[1]

cwd = os.path.abspath(os.getcwd())

directory_path = os.path.join(cwd, dirname)

print(os.path.exists(directory_path))

def download_chunk(url):
    try:
        r = s.request("GET", url, stream=True)
        path = os.path.join(dirname, line.strip())
        print( "downloading... {0}".format(line.strip()), end=" " )
        with open(path, 'wb') as out:
            for chunk in r:
                out.write(chunk)
            print("done!")
        r.raw.release_conn()
        return "{0} -> {1}".format(url, r.raw.status)
    except e:
        print("Error!")
        print(e)

def parse_and_download(line):
    if line.startswith('#') is False:
        url = hostname + line.strip()
        print(url)

if os.path.exists(directory_path) is True:
    print("Directory not empty, exiting...")
else:
    os.mkdir(dirname)
    with open(os.path.join(cwd, 'index-v1-a1.m3u8')) as f:
        playlist_data = f.readlines()

    #for line in playlist_data:
    #    parse_and_download(line)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for line in playlist_data:
            futures.append(
                executor.submit(
                    parse_and_download, line=line
                )
            )
        for future in concurrent.futures.as_completed(futures):
            try:
                print(future.result())
            except requests.ConnectTimeout:
                print("ConnectTimeout.")

            
            
end = time()
print(end - start)