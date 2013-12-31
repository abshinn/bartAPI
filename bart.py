#!/usr/bin/env python3

import os, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
import pdb

envkey = os.environ.get("BART_API_KEY")
if envkey:
    key = envkey
else:
    print("BART_API_KEY environment variable does not exist")
    sys.exit()

def APIquery(API = "", **parameters):
    """bart.APIquery(**parameters) retrieves the xmltree root object from http://api.bart.gov"""
    if not API:
        try:
            API = parameters["cmd"]
        except KeyError:
            print("cmd is a required keyword")
            sys.exit()
    parameters["key"] = key
    queryStr = urllib.parse.urlencode(parameters)
    url = "http://api.bart.gov/api/{}.aspx?{}".format(API, queryStr)
    #print("Querying BART with: {}".format(url))
    with urllib.request.urlopen(url) as BART:
        tree = ET.parse(BART)
    root = tree.getroot()
    return root

class BSAstruct:
    """bart.BSAstruct(): handles the xmltree root specific to the BART API bsa command"""
    def __init__(self, xmlroot):
        self.date = xmlroot.find("date").text
        self.time = xmlroot.find("time").text
        self.advisory = []
        for bsa in xmlroot.findall("bsa"):
            station = bsa.find("station").text
            descrip = bsa.find("description").text
            try:
                typeadv = bsa.find("type").text
            except AttributeError:
                typeadv = None
            self.advisory.append({"station":station, "descrip":descrip, "type":typeadv})
    def __str__(self):
        strResult = "BART Service Advisory {self.date}; {self.time}\n".format(self=self)
        for bsa in self.advisory:
            strResult += "Station: {}\n" \
                         "Description: [{}] {}\n".format(bsa["station"], bsa["type"], bsa["descrip"])
        return strResult

class COUNTstruct:
    """bart.COUNTstruct(): handles the xmltree root specific to the BART API count command"""
    def __init__(self, xmlroot):
        self.date = xmlroot.find("date").text
        self.time = xmlroot.find("time").text
        self.traincount = xmlroot.find("traincount").text
    def __str__(self):
        return "BART train count {self.date}; {self.time}\n{self.traincount} trains\n".format(self=self)

class ELEVstruct:
    """bart.ELEVstruct(): handles the xmltree root specific to the BART API elev command"""
    def __init__(self, xmlroot):
        self.date = xmlroot.find("date").text
        self.time = xmlroot.find("time").text
        self.bsa_id = []
        for bsa in xmlroot.findall("bsa"):
            station = bsa.find("station").text
            typeof  = bsa.find("type").text
            descrip = bsa.find("description").text
            self.bsa_id.append({"station":station, "type":typeof, "descrip":descrip})
    def __str__(self):
        strResult = "BART Elevator Advisory {self.date}; {self.time}\n".format(self=self)
        for bsa in self.bsa_id:
            strResult += "Station: {}\n" \
                         "Description: [{}] {}\n".format(bsa["station"], bsa["type"], bsa["descrip"])
        return strResult


class bsa:
    """bart.bsa: BART Service Advisory API"""

    class bsa(object):
        """bart.bsa.bsa()"""
        def __init__(self, **parameters):
            self.root = APIquery(API = "bsa", cmd = "bsa", **parameters)
            #self.string = ET.tostring(self.root, encoding = "unicode") # string result
            self.result = BSAstruct(self.root)
        def __str__(self):
            return self.result.__str__()

    class count(object):
        """bart.bsa.count(): BART Train Count"""
        def __init__(self, **parameters):
            self.root = APIquery(API = "bsa", cmd = "count", **parameters)
            self.result = COUNTstruct(self.root)
        def __str__(self):
            return self.result.__str__()

    class elev(object):
        """bart.bsa.elev(): BART Elevator Advisory"""
        def __init__(self, **parameters):
            self.root = APIquery(API = "bsa", cmd = "elev", **parameters)
            self.result = ELEVstruct(self.root)
        def __str__(self):
            return self.result.__str__()

class STNSstruct:
    """bart.STNSstruct(): handles the xmltree root specific to the BART API stns command"""
    def __init__(self, xmlroot):
        self.stations = xmlroot.find("station")
        for station in stations.findall("station"):
            pass


if __name__ == "__main__":
    print(bsa.bsa())
    print(bsa.count())
    print(bsa.elev())
