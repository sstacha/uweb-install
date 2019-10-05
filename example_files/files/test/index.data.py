# from myapp.models import Web_Region
import re
context = {}

def get_context(request):
    regex_http_ = re.compile(r'^HTTP_.+$')
    regex_content_type = re.compile(r'^CONTENT_TYPE$')
    regex_content_length = re.compile(r'^CONTENT_LENGTH$')

    request_headers = {}
    for header in request.META:
        if regex_http_.match(header) or regex_content_type.match(header) or regex_content_length.match(header):
            request_headers[header] = request.META[header]

    request_ip = request.META.get('REMOTE_ADDR')
    real_ip = request.META.get('HTTP_X_REAL_IP')
    context.update({'headers': request_headers, 'request_ip': str(request_ip), 'real_ip': str(real_ip)})
    return context