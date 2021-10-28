import requests
def check_login_type(ip):
    headers = requests.utils.default_headers()
    print(headers)
    headers["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Cecko'
    headers["Referer"] = "http://" + ip
    try:
        r = requests.get('http://'+ip, headers=headers)
    except:
        return 'connection error'
    print(r.status_code)
    print(r.content)
    #
    if r.status_code == 401:
        return 'basic'
    elif r.text.find('/info/Login.html')!=-1:
        return 'dlink_hnap'
    elif r.text.find('log_passs')!=-1 or r.text.find('login_auth.asp')!=-1:
        return 'dlink_asp'
    else:
        return 'unknown'
    #两次MD5运算
trans_5C = "".join(chr(x^0x5c) for x in range(256))
trans_36 = "".join(chr(x^0x36) for x in range(256))
blocksize = md5().block_size #消息摘要内部块大小

BASIC_CRED ={'dlink':(b'admin',b'')}
CRED = {'dlink': ['admin', 'admin']}
PRIVATE_KEY = ''

def hmac_md5(key, mag):
    if len(key) > blocksize:
        key = md5(key).digest()
    key = str(key) + '\x00' * (blocksize - len(key))
    o_key_pad = key.translate(trans_5C).encode()


def get_session(brand,ip):
    s = requests.Session()
    login_type = check_login_type(ip)
    if login_type == 'basic':
        s.auth = BASIC_CRED[brand]
        return login_type, s
    elif login_type == 'dlink_asp':
        username, password = BASIC_CRED[brand]
        headers = requests.utils.default_headers()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
        headers["Origin"] = "http://"+ip
        headers["Referer"] = "http://"+ip
        headers["Cache-Control"] = "max-age=0"
        payload = {'html_response_page':'login_fail.asp','login_name':'YWRtaW4A','login_pass':'','graph_id':'d360e','log_pass':'','graph_code':'','Login':'Log In'}
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

        challenge = str(data[data.find("Challenge")+11:data.find("</Challenge>")])
        cookie = str(data[data.find("<Cookie>")+8:data.find("</Cookie>")])
        publicKey = str(data[data.find("<PublicKey>")+11:data.find("</PublicKey>")])

        PRIVATE_KEY = hmac_md5(publicKey+password, challenge).hexdigest().upper()
        md5_password = hmac_md5(PRIVATE_KEY, challenge).hexdigest().upper()

        cookies ={"uid": cookie}
        headers["HNAP_AUTH"] = HNAP_AUTH("Login",PRIVATE_KEY)
        payload = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Login xmlns="http://purenetworks.com/HNAP1/"><Action>login</Action><Username>Admin</Username><LoginPassword>'+md5_password+'</LoginPassword><Captcha></Captcha></Login></soap:Body></soap:Envelope>'
        requests.post('http://'+ip+'/HNAP1/',headers=headers,data=payload,cookies=cookies)
        return login_type, cookies
    else:
        return login_type, s
ip = input("IP")
check_login_type(ip)