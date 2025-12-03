#!/usr/bin/python3


from xml.sax.handler import ContentHandler
from xml.sax import make_parser


class CamHandler(ContentHandler):

    def __init__(self):
        self.inCamara = False
        self.inContent = False
        self.content = ""
        self.lugar = ""
        self.coordenadas = ""
        self.id = ""
        self.src = ""
        self.cams = []

    def startElement(self, name, attrs):
        if name == 'camara':
            self.inCamara = True
        elif self.inCamara:
            if name == 'lugar':
                self.inContent = True
            elif name == 'coordenadas':
                self.inContent = True
            elif name == 'src':
                self.inContent = True
            elif name == 'id':
                self.inContent = True

    def endElement(self, name):
        global cams

        if name == 'camara':
            self.inCamara = False
            self.cams.append({'src': self.src,
                              'coordenadas': self.coordenadas,
                              'lugar': self.lugar,
                              'id': self.id})
        elif self.inCamara:
            if name == 'lugar':
                self.lugar = self.content
                self.content = ""
                self.inContent = False
            elif name == 'id':
                self.id = self.content
                self.content = ""
                self.inContent = False
            elif name == 'coordenadas':
                self.coordenadas = self.content
                self.content = ""
                self.inContent = False
            elif name == 'src':
                self.src = self.content
                self.content = ""
                self.inContent = False

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars


class CamChanel:
    def __init__(self, stream):
        self.parser = make_parser()
        self.handler = CamHandler()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(stream)

    def cams(self):
        return self.handler.cams

