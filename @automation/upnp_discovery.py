#!/usr/bin/env python

# see: http://omz-forums.appspot.com/pythonista/post/6417706764992512#post-5212093439541248

import socket

SSDP_DICT = { 'ip_address' : '239.255.255.250',
              'port'       : 1900,
              'mx'         : 10,
              'st'         : 'ssdp:all' }

ssdp_request = '''M-SEARCH * HTTP/1.1
HOST: {ip_address}:{port}
MAN: "ssdp:discover"
MX: {mx}
ST: {st}

'''.replace('\n', '\r\n').format(**SSDP_DICT) + '\r\n'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.sendto(ssdp_request, (SSDP_DICT['ip_address'], SSDP_DICT['port']))
print(sock.getsockname())

def upnp_discover(match_str='', timeout_secs=5):
    sock.settimeout(timeout_secs)
    responses = []
    try:
        while True:
            response = sock.recv(1000)
            if match_str in response:
                print(response)
                responses.append(response)
    except socket.timeout as e:
        pass
    return responses

def ip_addresses(upnp_endpoints):
    return sorted(set([line.split('/')[2] for line
           in '\n'.join(upnp_endpoints).splitlines()
           if line.lower().startswith('location:')]))

if __name__ == '__main__':
    upnp_endpoints = upnp_discover()  # 'ST: urn:Belkin:service:basicevent:1')
    print(ip_addresses(upnp_endpoints))
    print('Done.')
