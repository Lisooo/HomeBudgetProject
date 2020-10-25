from flask import request, url_for


def redirect_url(default='home'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)
