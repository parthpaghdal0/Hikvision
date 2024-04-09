
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
            requests.put(url, timeout=10)
            return True
        except:
            return False

    @staticmethod
    def writeTextOverlay(ip, username, password, text1, text2):
        body = '\
        <TextOverlayList version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
            <TextOverlay version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
                <id>1</id>\
                <enabled>true</enabled>\
                <positionX>0</positionX>\
                <positionY>48</positionY>\
                <displayText>51-510504, 20YD DISPOSAL C&amp;D INBD TN, </displayText>\
            </TextOverlay>\
            <TextOverlay version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
                <id>2</id>\
                <enabled>true</enabled>\
                <positionX>400</positionX>\
                <positionY>48</positionY>\
                <displayText>SW WASTE ROLLOFF, 36040, 32220</displayText>\
            </TextOverlay>\
            <TextOverlay version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
                <id>3</id>\
                <enabled>true</enabled>\
                <positionX>0</positionX>\
                <positionY>0</positionY>\
                <displayText>51-510504, 20YD DISPOSAL C&amp;D INBD YD, SW WASTE ROLLOFF, 0, 0</displayText>\
            </TextOverlay>\
            <TextOverlay version="2.0" xmlns="http://www.isapi.org/ver20/XMLSchema">\
                <id>4</id>\
                <enabled>true</enabled>\
                <positionX>400</positionX>\
                <positionY>0</positionY>\
                <displayText>SW WASTE ROLLOFF, 0, 0</displayText>\
            </TextOverlay>\
        </TextOverlayList>\
        '
        url = generateUrl(ip, username, password)

        try:
            requests.put(url, body, timeout=10)
            return True
        except:
            return False


