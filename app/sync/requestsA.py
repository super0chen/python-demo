import requests
import urllib3

response = requests.get("http://www.baidu.com")
print(type(response))
print(response.status_code)
print(type(response.text))
print(response.text)
print(response.cookies)

# 各种请求方式：
requests.post("http://httpbin.org/post")
requests.put("http://httpbin.org/put")
requests.delete("http://httpbin.org/delete")
requests.head("http://httpbin.org/head")
requests.options("http://httpbin.org/options")
requests.get("http://httpbin.org/get")

# 基本get请求：
response = requests.get("http://httpbin.org/get")
print(response.text)

# 带参数get请求1:
response = requests.get("http://httpbin.org/get?name=yiqing&age=18")
print(response.text)

# 带参数get请求2：
data = {
    "name": "yiqing",
    "age": 18
}
response = requests.get("http://httpbin.org/get", params=data)
print(response.text)

# 解析JSON：
response = requests.get("http://httpbin.org/get")
print(response.json())
print(type(response.json()))

# 获取二进制数据（给出了一个图片的地址，下载到本地）：
response = requests.get("http://p1.music.126.net/vvZLXI5EqFLsKLlvfqz0uA==/19088621370291879.jpg")
with open("pic.jpg", "wb") as f:
    f.write(response.content)

# 添加headers:
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}
response = requests.get("http://www.baidu.com", headers=headers)
print(response.text)

# 基本post请求：
data = {
    "name": "yiqing",
    "age": 18
}
response = requests.post("http://httpbin.org/post", data=data)
print(response.text)

# 带参数post请求：
data = {
    "name": "yiqing",
    "age": 18
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}
response = requests.post("http://httpbin.org/post", data=data, headers=headers)
print(response.json())

# 状态码判断:
response = requests.get("http://www.baidu.com")
exit() if not response.status_code == requests.codes.ok else print("Requests Successfully")
# 相当于：
response = requests.get("http://www.baidu.com")
exit() if not response.status_code == 200 else print("Requests Successfully")

# 文件上传（用刚才下载的图片）：
files = {"file": open("pic.jpg", "rb")}
response = requests.post("http://httpbin.org/post", files=files)
print(response.text)

# 获取cookie:
response = requests.get("http://blog.csdn.net/")
print(response.cookies)
for key, value in response.cookies.items():
    print(key + "=" + value)

# 尝试模拟登录:
requests.get("http://httpbin.org/cookies/set/number/123456789")
response = requests.get("http://www.httpbin.org/cookies")
print(response.text)

'''发现这样登录会失败，这里两次用get方式发起请求，实际上这两次是完全独立的过程，
相当于在两个没有关联的浏览器上进行操作的。因此获取不到任何的cookie信息。
要做到两次访问用一个浏览器，就是下面的方法：
'''
s = requests.Session()
s.get("http://httpbin.org/cookies/set/number/123456789")
response = s.get("http://www.httpbin.org/cookies")
print(response.text)

# 证书验证：
response = requests.get("https://www.12306.cn")
print(response.status_code)

# 发现出现了错误，原因是没有合法证书
# 这里可以避免：
response = requests.get("https://www.12306.cn", verify=False)
print(response.status_code)

# 不过依然有警告信息，再这样操作可以去除警告信息：
urllib3.disable_warnings()
response = requests.get("https://www.12306.cn", verify=False)
print(response.status_code)

# 代理设置：
proxies = {
    "http": "http://222.222.169.60:53281",
    "https": "http://222.222.169.60:53281"
}
response = requests.get("http://www.baidu.com", proxies=proxies)
print(response.status_code)

# 有密码的代理：
proxies = {
    "http": "http://user:password@222.222.169.60:53281/",
}
response = requests.get("http://www.baidu.com", proxies=proxies)
print(response.status_code)

# 超时设置：
response = requests.get("http://www.baidu.com", timeout=1)
print(response.status_code)

# 抓住异常：
from requests.exceptions import ConnectTimeout

try:
    response = requests.get("http://httpbin.org/get", timeout=0.1)
    print(response.status_code)
except ConnectTimeout:
    print("TIMEOUT")
