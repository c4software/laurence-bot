import http.client, urllib.request, urllib.parse, urllib.error
import json
import socket
import _thread
from urllib.parse import urlparse
import codecs

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.10 Safari/537.36"

def callrest(domain="", port="",path="/",type="GET",params={},timeout=60,encode_post_param_as_json=False,ssl=False, user_headers={}):
    connection = False

    try:
        if port != "":
            port = int(port)
            if ssl:
                connection = http.client.HTTPSConnection(domain, port, timeout=timeout)
            else:
                connection = http.client.HTTPConnection(domain, port, timeout=timeout)
        else:
            if ssl:
                connection = http.client.HTTPSConnection(domain, timeout=timeout)
            else:
                connection = http.client.HTTPConnection(domain, timeout=timeout)

        if type == "POST":
            if encode_post_param_as_json:
                params = json.dumps(params)
                params = params.encode('utf-8')
                headers = override_headers({"User-Agent": USER_AGENT, "Content-type": "application/json","Accept": "application/json"}, user_headers)
            else:
                params = urllib.parse.urlencode(params)
                headers = override_headers({"User-Agent": USER_AGENT, "Content-type": "application/x-www-form-urlencoded","Accept": "*/*"}, user_headers)

            connection.request('POST', path, params, headers=headers)

        if type == "GET":
            headers = override_headers({"User-Agent": USER_AGENT}, user_headers)
            params = urllib.parse.urlencode(params)
            connection.request('GET', path+'?%s' % params, headers=headers)

        if type == "PUT":
            headers = override_headers({"User-Agent": USER_AGENT, "Content-type": "application/x-www-form-urlencoded","Accept": "*/*"}, user_headers)
            params = urllib.parse.urlencode(params)
            connection.request('PUT', path+'?%s' % params, headers=headers)

        result = connection.getresponse()

        reader = codecs.getreader("utf-8")
        if result.status == 302:
            headers = dict(result.getheaders())
            if 'location' in headers and headers['location']:
                o = urlparse(headers['location'])
                return callrest(domain=o.netloc, path=o.path)

            if 'Location' in headers and headers['Location']:
                o = urlparse(headers['Location'])
                return callrest(domain=o.netloc, path=o.path, user_headers=user_headers)


        return (result.status, result.reason, reader(result).read())
    except socket.timeout as e:
        return (408,"Timeout",None)
    except Exception as e:
        print("Erreur lors de lexecution de la requete : {0}".format(e))
        return (500,"Internal Error",None)
    finally:
        if connection:
            connection.close()

    return (500,"Internal Error",None)

def override_headers(headers, user_headers):
    return dict(list(headers.items())+list(user_headers.items()))

def call_async(domain="", port="",path="/",type="GET",params={},timeout=10,encode_post_param_as_json=False):
    # Appel de la fonction sans attendre de retour.
    _thread.start_new_thread(callrest, (domain, port,path,type,params,timeout,encode_post_param_as_json))
