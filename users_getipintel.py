import requests
import sys
ip = sys.argv[1]
resp = requests.get(f"http://check.getipintel.net/check.php?ip={ip}&contact=wuchang@pdx.edu&flags=f")
print(resp.text)
