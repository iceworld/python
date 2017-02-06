#this script can get captcha from 10086.cn and post 30M traffic request other than do it from your poor mobile phone
#working for 10086 vocalno event occurring randomly
#todo list: captcha recogniztion, not too hard
import requests
import re
import json
import mylog
import base64


if __name__ == "__main__":
    #cookie is expiring every 1 hour, please grab new one ahead 5-10 mins b4 run the script
    cookie = 'koa.sid=qFiLuRgoVmYYA5qY'
    for times in range(100):
        url = 'http://wx.10086.cn/hbhs/exchange'
        headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36,10086APP',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept' : 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'zz.dela.cmcc.traffic', 
            'Referer': 'http://wx.10086.cn/hbhs/index?telephone=47956EE957C4CB6F1D002B78BC23DE8800F69D52392175AF0B3FAB430226659B',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': cookie
        }            
        s=requests.session()
        s.headers=headers
        try:
            r=s.get(url)
        except requests.TooManyRedirects:
            print('URL not reachable')
        else:
            pass
        
        #2. obtain csrf value id="csrf" name="_csrf" value="bYnFkbQo-3x2C9O5xNRDG5TfQhAhlcgElQ_M"/>        
        content = r.text
        m = re.search('name="_csrf" value="([^"]+)"', content)
        csrf = m.group(1)
        print(csrf)
        
        #3. get captcha
        url = 'http://wx.10086.cn/hbhs/captcha'
        try:
            r=s.get(url)
        except requests.TooManyRedirects:
            pass
        else:
            pass
        content = r.text
        result = json.loads(content)
        data = result['data']
        photo = data.partition('base64,')[2]
        image_data = base64.b64decode(photo)
        fp = open('user.jpg', 'wb')
        fp.write(image_data)
        fp.close()
        captcha = input('captcha required!!!')
    
    
        #3. post signature 
        url = 'http://wx.10086.cn/hbhs/api/getJsSignature'
        data = 'url=http%3A%2F%2Fwx.10086.cn%2Fhbhs%2Fexchange'
        try:
            r=s.post(url,data=data,timeout=1)
        except:
            r=s.post(url,data=data,timeout=1)
        else:
            pass
    
        #4. post: http://wx.10086.cn/hbhs/exchange
        url = 'http://wx.10086.cn/hbhs/exchange'
        data = 'captcha='+captcha
        s.headers['x-csrf-token'] = csrf
        s.headers['Referer'] = url
        try:
            r=s.post(url,data=data,timeout=1)
        except:
            pass
        else:
            pass
        print(r.text)