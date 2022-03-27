
import requests,json,random,string,os
from datetime import datetime

from captcha.image import ImageCaptcha
from PIL import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
import base64
from uuid import uuid4
from Crypto.Cipher import AES

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

class ArithmeticCaptchaAbstract(ImageCaptcha):
    def __init__(self, width=160, height=60, fonts=None, font_sizes=None):
        self._width= width
        self._height = height
        self._fonts = fonts
        self._font_sizes = font_sizes



    def create_captcha_image(self,chars, color, background):
        image = Image.new('RGB', (self._width, self._height), background)
        draw = Draw(image)

        def _draw_character(c):
            font =  truetype(font=self._fonts,size=self._font_sizes)
            w, h =  draw.textsize(c,font=font)
            dx = random.randint(0, 10)
            dy = random.randint(0, 10)
            im = Image.new("RGBA",(w + dx, h + dy),background)
            Draw(im).text((dx,dy),c,font=font,fill=random_color())
            return im     
        images = []
        for c in chars:
            images.append(_draw_character(c))
        
        text_width = sum([im.size[0] for im in images])
        width = max(text_width, self._width)
        image = image.resize((width, self._height))

        average = int(text_width / len(chars))
        rand = int(0.10 * average)
        offset = int(average * 0.1)
        for im in images:
            w,h = im.size
            image.paste(im, (offset, int((self._height - h) / 2)))
            offset = offset + w + random.randint(-rand, 0)
        if width > self._width:
            image = image.resize((self._width, self._height))
        
        return image

            


#获取随机颜色
def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#随机生成文件名
def generate_name():
    nowTime= datetime.now().strftime("%Y%m%d%H%M%S")
    randomNum = random.randint(0,100)
    if randomNum <=10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return uniqueNum


    
def get_public_ip():
    html_text = requests.get("http://ip.42.pl/raw").text
    return html_text 




###获取IP归属地
def getIpInfo(ip):
    try:
        ipinfo=requests.get("http://ip.taobao.com/service/getIpInfo.php?ip={}&accessKey=alibaba-inc".format(ip)).text
        ipinfo=json.loads(ipinfo).get('data')
        ipinfo_str=ipinfo.get('country')+'|'+ipinfo.get('region')+"|"+ipinfo.get('city')+"|"+ipinfo.get('isp')
        return ipinfo_str
    except Exception as e:
         print(e)



def menu_tree(data,root,root_filed,node_filed):
    """
    解析list数据为树结构
    :param data:  被解析的数据
    :param root: 根节点值
    :param root_field: 根节点字段
    :param node_field: 节点字段
    :return: list
    """
    menu = [ item for item in data if item.get(root_filed) == root ]

    for i in data:
        node = i.get(node_filed)
        children = []
        for j in data:
            parent = j.get(root_filed)
            if node == parent:
                j['component']=j.get('component')
                del j['alwaysShow']
                del j['redirect']
                children.append(j)
                i['children'] = children 
    return menu

def dept_tree(data,root,root_filed,node_filed):
    menu = [ item for item in data if item.get(root_filed) == root ]
    
    for i in data:
        node = i.get(node_filed)
        children = []
        for j in data:
            parent = j.get(root_filed)
            if node == parent:
                children.append(j)
                i['children'] = children
    return menu


def getColor():
    return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

if __name__ == "__main__":
    pass

    



