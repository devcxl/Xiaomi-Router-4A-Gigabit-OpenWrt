import tarfile
import requests


router_ip = '192.168.31.1'
stok = '6cb7bf8731d8ffcd4e0d71d752178a0e'

with tarfile.open("build/2023-09-02--21 51 04.tar.gz", "w:gz") as tar:
    tar.add("files/speedtest_urls.xml", "speedtest_urls.xml")
    tar.add("files/script.sh", "script.sh")

r1 = requests.post(
    f"http://{router_ip}/cgi-bin/luci/;stok={stok}/api/misystem/c_upload",
    files={"image": open("build/2023-09-02--21 51 04.tar.gz", 'rb')},
)

print(r1.status_code)
print(r1.text)

r = requests.get(
    f"http://{router_ip}/cgi-bin/luci/;stok={stok}/api/xqnetdetect/netspeed?0"
)

print(r.status_code)
print(r.text)
