import requests
from hashlib import md5
import base64
import time
import math

trans_5C = "".join(chr(x ^ 0x5c) for x in range(256))
trans_36 = "".join(chr(x ^ 0x36) for x in range(256))
blocksize = md5().block_size #消息摘要内部块大小

# dlink default is 'admin'/'' but password not be null
BASIC_CRED = {'dlink':(b'admin', b'')}
CRED = {'dlink':['admin', 'admin']}
PRIVATE_KEY = ''

def hmac_md5(key, msg):
    if len(key) > blocksize:
        key = md5(key).digest()
    key = str(key) + '\x00' * (blocksize - len(key))

    o_key_pad = key.translate(trans_5C).encode()
    i_key_pad = key.translate(trans_36).encode()
    return md5(o_key_pad + md5(i_key_pad + msg.encode()).digest())

def HNAP_AUTH(SOAPAction, privateKey):
    b = math.floor(int(time.time())) % 2000000000;
    b = str(b)[:-2]
    h = hmac_md5(privateKey, b + '"http://purenetworks.com/HNAP1/' + SOAPAction + '"').hexdigest().upper()
    return h + " " + b



    if r.status_code == 401:
        return 'basic'
    elif r.text.find('/info/Login.html') != -1: # dlink hnap
        return 'dlink_hnap'
    elif r.text.find('log_pass') != -1 or r.text.find('login_auth.asp') != -1: # dlink normal login
        return 'dlink_asp'
    else:
        return 'unknown'

def get_session(brand, ip):
    s = requests.Session()
    login_type = check_login_type(ip)
    if login_type == 'basic':
        s.auth = BASIC_CRED[brand]
        return login_type, s

    elif login_type == 'dlink_asp':
        username, password = BASIC_CRED[brand]
        headers = requests.utils.default_headers()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
        headers["Origin"] = "http://" + ip
        headers["Referer"] = "http://" + ip
        headers["Cache-Control"] = "max-age=0"
        payload = {'html_response_page':'login_fail.asp','login_name':'YWRtaW4A','login_pass':'','graph_id':'d360e','log_pass':'','graph_code':'','Login':'Log In'}
        s.post('http://{}/login.cgi'.format(ip), headers=headers, data=payload)
        return login_type, s

    elif login_type == 'dlink_hnap':
        username, password = CRED[brand]
        headers = requests.utils.default_headers()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
        headers["SOAPAction"] = '"http://purenetworks.com/HNAP1/Login"'
        headers["Origin"] = "http://" + ip
        headers["Referer"] = "http://" + ip + "/info/Login.html"
        headers["Content-Type"] = "text/xml; charset=UTF-8"
        headers["X-Requested-With"] = "XMLHttpRequest"

        payload = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Login xmlns="http://purenetworks.com/HNAP1/"><Action>request</Action><Username>Admin</Username><LoginPassword></LoginPassword><Captcha></Captcha></Login></soap:Body></soap:Envelope>'
        r = requests.post('http://'+ip+'/HNAP1/', headers=headers, data=payload)
        data = r.text

        challenge = str(data[data.find("<Challenge>") + 11: data.find("</Challenge>")])
        cookie = str(data[data.find("<Cookie>") + 8: data.find("</Cookie>")])
        publicKey = str(data[data.find("<PublicKey>") + 11: data.find("</PublicKey>")])

        PRIVATE_KEY = hmac_md5(publicKey + password, challenge).hexdigest().upper()
        md5_password = hmac_md5(PRIVATE_KEY, challenge).hexdigest().upper()

        cookies = {"uid": cookie}
        headers["HNAP_AUTH"] = HNAP_AUTH("Login", PRIVATE_KEY)
        payload = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Login xmlns="http://purenetworks.com/HNAP1/"><Action>login</Action><Username>Admin</Username><LoginPassword>'+md5_password+'</LoginPassword><Captcha></Captcha></Login></soap:Body></soap:Envelope>'
        requests.post('http://'+ip+'/HNAP1/', headers=headers, data=payload, cookies=cookies)
        return login_type, cookies
    else:
        return login_type, s