
import requests

def generateUrl(ip, username, password):
    return "http://%s:%s@%s/ISAPI/System/Video/inputs/channels/1/overlays/text" % (username, password, ip)

class Camera:

    @staticmethod
    def test(ip, username,  password):
        url = generateUrl(ip, username, password)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def clearTextOverlay(ip, username, password):
        url = generateUrl(ip, username, password)

        try:
            requests.delete(url, timeout=10)
            return True
        except:
            return False

    @staticmethod
    def writeTextOverlay(ip, username, password, text1, text2):
        text1_1 = text1[:44]
        text1_2 = text1[44:]
        text2_1 = text2[:44]
        text2_2 = text2[44:]
        
        text1_1 = text1_1.replace("&", "&amp;")
        text1_2 = text1_2.replace("&", "&amp;")
        text2_1 = text2_1.replace("&", "&amp;")
        text2_2 = text2_2.replace("&", "&amp;")

        print(text1_1, text1_2)
        print(text2_1, text2_2)

        body = '\
        <TextOverlayList version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
            <TextOverlay version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
                <id>1</id>\
                <enabled>true</enabled>\
                <positionX>0</positionX>\
                <positionY>160</positionY>\
                <displayText>%s</displayText>\
            </TextOverlay>\
            <TextOverlay version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
                <id>2</id>\
                <enabled>true</enabled>\
                <positionX>0</positionX>\
                <positionY>128</positionY>\
                <displayText>%s</displayText>\
            </TextOverlay>\
            <TextOverlay version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
                <id>3</id>\
                <enabled>true</enabled>\
                <positionX>0</positionX>\
                <positionY>64</positionY>\
                <displayText>%s</displayText>\
            </TextOverlay>\
            <TextOverlay version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
                <id>4</id>\
                <enabled>true</enabled>\
                <positionX>0</positionX>\
                <positionY>32</positionY>\
                <displayText>%s</displayText>\
            </TextOverlay>\
        </TextOverlayList>\
        ' % (text1_1, text1_2, text2_1, text2_2)
        url = generateUrl(ip, username, password)

        try:
            response = requests.put(url, body, timeout=10)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False