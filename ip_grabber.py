#!/usr/bin/python3


from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def get_visitor_ip():
    ip = request.headers.get('X-Forwarded-For')
    # try to get IP from HTTP headers (X-Forwarded commonly used when behind proxy/LB)

    if ip is None:
        ip = request.headers.get('X-Real-IP')
    # if no X-Forwarded-For header, try other common headers

    if ip is None:
        ip = request.remote_addr
    # if no proxy headers, get direct remote addr

    if ip and ',' in ip:
        ip = ip.split('/')[0].strip()
    # if X-Forwarded-For contains multiple IPs, get first one (client IP)

    return {
            'visitor_ip': ip,
            'headers': {
                'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
                'X-Real-IP': request.headers.get('X-Real-IP'),
                'Remote-Addr': request.remote_addr
            }
    }

if __name__ == '__main__':
    app.run(debug=True)
