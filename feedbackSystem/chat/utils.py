from urllib import parse

def bodyToDict(body: bytes):
    """Turns a `request.body` object into a Dictionary."""
    body = body.decode().split('&')
    retDict = dict()
    for i in body:
        data = i.split('=')
        retDict[data[0]] = parse.unquote(data[1])
    return retDict