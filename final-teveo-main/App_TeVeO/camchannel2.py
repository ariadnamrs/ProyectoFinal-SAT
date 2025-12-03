#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys


class CamHandler(ContentHandler):

    def __init__(self):
        self.inCamara = False
        self.inContent = False
        self.content = ""
        self.longitude = ""
        self.latitude = ""
        self.place = ""
        self.url = ""
        self.info = ""
        self.id = ""
        self.cams = []

    def startElement(self, name, attrs):
        if name == 'cam':
            self.inCamara = True
            self.id = attrs.get('id')
        elif self.inCamara:
            if name == 'url':
                self.inContent = True
            elif name == 'info':
                self.inContent = True
            elif name == 'latitude':
                self.inContent = True
            elif name == 'longitude':
                self.inContent = True

    def endElement(self, name):
        if name == 'cam':
            self.inCamara = False
            self.cams.append({'src': self.url,
                              'coordenadas': self.latitude + self.longitude,
                              'lugar': self.info,
                              'id': self.id})
        elif self.inCamara:
            if name == 'info':
                self.info = self.content
                self.content = ""
                self.inContent = False
            elif name == 'latitude':
                self.latitude = self.content
                self.content = ""
                self.inContent = False
            elif name == 'longitude':
                self.longitude = self.content
                self.content = ""
                self.inContent = False
            elif name == 'url':
                self.url = self.content
                self.content = ""
                self.inContent = False

    def characters(self, chars):
        if self.inContent:
            self.content += chars


class CamChanel2:
    def __init__(self, stream):
        self.parser = make_parser()
        self.handler = CamHandler()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(stream)

    def cams(self):
        return self.handler.cams

# Example of usage
if __name__ == "__main__":
    cams_data = CamChanel2(open("canales.xml"))
    for cam in cams_data.cams():
        print(cam)
