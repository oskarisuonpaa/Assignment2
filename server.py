from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime as DT
import xml.etree.ElementTree as ET
import requests

# Adds a new note to the xml database
def addNote(topicHeading, noteHeading, text):
    xmlTree = ET.parse("db.xml")
    root = xmlTree.getroot()

    timestamp = DT.now().strftime("%m/%d/%y - %H:%M:%S") # Gets current time

    noteElement = ET.Element("note")
    noteElement.attrib["name"] = noteHeading

    textElement = ET.SubElement(noteElement, "text")
    textElement.text = text

    timestampElement = ET.SubElement(noteElement, "timestamp")
    timestampElement.text = timestamp

    topicElements = root.findall("topic")

    if len(topicElements) == 0:
        topicElement = ET.SubElement(root, "topic")
        topicElement.attrib["name"] = topicHeading
    else:
        for topic in topicElements:
            if topic.attrib["name"] == topicHeading:
                topicElement = topic
                break

    topicElement.append(noteElement)

    ET.indent(root, space="\t", level=0) # Formats file to "pretty" format
    xmlTree.write("db.xml", encoding="utf8")
    return

# Finds any given topic from the xml database
def fetchByTopic(topicHeading):
    xmlTree = ET.parse("db.xml")
    root = xmlTree.getroot()

    topicElements = root.findall("topic")

    if len(topicElements) == 0:
        return "No topics found"
    else:
        for topic in topicElements:
            if topic.attrib["name"] == topicHeading:
                topicElement = topic
                return ET.tostring(topicElement, encoding="utf8", method="html")
    
    return "No specified topic found"

# Queries Wikipedia and then appends the link to the Wikipedia page to the given topic
def queryWikipedia(searchTerm, topicHeading):
    session = requests.Session()

    url = "https://en.wikipedia.org/w/api.php"

    parameters = {
        "action": "opensearch",
        "namespace": "0",
        "search": searchTerm,
        "limit": "1",
        "format": "json"
    }

    response = session.get(url=url, params=parameters)

    data = response.json()
    session.close()

    if len(data[3]) == 0:
        return "Wikipedia article not found"
    
    wikipediaArticleURL = data[3][0]

    xmlTree = ET.parse("db.xml")
    root = xmlTree.getroot()

    articleLinkElement = ET.Element('articleLink')
    articleLinkElement.text = wikipediaArticleURL

    topicElements = root.findall("topic")

    if len(topicElements) == 0:
        topicElement = ET.SubElement(root, "topic")
        topicElement.attrib["name"] = topicHeading
    else:
        for topic in topicElements:
            if topic.attrib["name"] == topicHeading:
                topicElement = topic
                break
    
    topicElement.append(articleLinkElement)

    ET.indent(root, space="\t", level=0) # Formats file to "pretty" format
    xmlTree.write("db.xml", encoding="utf8")


server = SimpleXMLRPCServer(("localhost", 5000), allow_none=True)

server.register_function(addNote, "addNote")
server.register_function(fetchByTopic, "fetchByTopic")
server.register_function(queryWikipedia, "queryWikipedia")

server.serve_forever()