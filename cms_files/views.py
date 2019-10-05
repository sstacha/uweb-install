# NOTE: DO NOT UPDATE THIS FILE - Create a new views_common.py and place any views there if you need it.  then reference
#   your new one in the urls.py file (which should be edited by you)

import os
import logging
import mimetypes
import importlib.util
import json
import codecs

from django.conf import settings
# from django.template import Context
from django.template import Template, Origin, RequestContext
from django.http import HttpResponse, FileResponse, JsonResponse, HttpResponseForbidden
from django.views.generic import View
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
# from pprint import pprint
# from django.shortcuts import redirect
# from django.shortcuts import render

from .models import Content

log = logging.getLogger("cms.views")


# This view is called from DocrootFallbackMiddleware.process_response
# when a 404 is raised and we are not working with a template (we want to look for a static file in the docroot)
def static(request):
    docroot_dir = getattr(settings, "DOCROOT_ROOT", "")
    use_static = getattr(settings, "USE_STATIC_FORBIDDEN", False)
    log.debug("docroot dir: " + docroot_dir)
    path = request.path_info
    if path.startswith("/"):
        path = path[1:]
    log.debug("path: " + path)
    file = os.path.join(docroot_dir, path)
    log.debug("file: " + file)
    if os.path.isfile(file):
        # for various reasons we don't want to serve up various file extensions. Let's look at a setting containing
        # extensions to ignore
        # USE CASE: Apache at root passes .htaccess, .dt and .py files through we don't want to show these static files
        if use_static:
            forbidden_extensions = getattr(settings, "STATIC_FORBIDDEN_EXTENSIONS", [])
            forbidden_file_names = getattr(settings, "STATIC_FORBIDDEN_FILE_NAMES", [])
            filename, ext = os.path.splitext(file)
            if ext in forbidden_extensions:
                return HttpResponseForbidden()
            elif os.path.basename(filename) in forbidden_file_names:
                return HttpResponseForbidden()
        log.debug("found static file: " + file)
        log.debug("downloading...")
        response = FileResponse(open(file, 'rb'), content_type=mimetypes.guess_type(path)[0])
        return response
    else:
        return None


# This view is called from DocrootFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching page exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation (render page).
def page(request):
    # NEW VERSION: pushed meta processing down to class TemplateMeta
    meta = TemplateMeta(request)
    # NOTE: only calls render_page if the template is found
    return meta.render()

    # """
    # We are going to try to look for a template a couple of ways based on the request; if nothing is found we return
    # None
    #  and things proceed like never called.  If found we return the response it should return instead
    # """
    # docroot_dir = getattr(settings, "DOCROOT_ROOT", "")
    # log.debug("docroot dir: " + docroot_dir)
    # path = request.path_info
    # if path.startswith("/"):
    #     path = path[1:]
    # file=os.path.join(docroot_dir, path)
    # log.debug("file: " + file)
    # url = file
    # module_name = path
    # template_name = path
    # template = None
    # # if the url ends in .html then try to load a corresponding template from the docroot/files directory
    # if url.endswith(".html"):
    #     # our url will request .html but we want to look for a .dt file (required for template processing)
    #     url = url[:-4]
    #     url += "dt"
    #     template_name = template_name[:-4]
    #     template_name += "dt"
    #     if os.path.isfile(url):
    #         log.debug("found file: " + url)
    #     else:
    #         url = None
    #
    # elif url.endswith('/'):
    #     url += "index.dt"
    #     if os.path.isfile(url):
    #         log.debug("found file: " + url)
    #         module_name += "index.html"
    #         template_name += "index.dt"
    #     else:
    #         url = None
    #
    # else:
    #     url += ".dt"
    #     if os.path.isfile(url):
    #         log.debug("found file: " + url)
    #         module_name += ".html"
    #         template_name += ".dt"
    #     else:
    #         url = None
    #
    # if url:
    #     log.debug("opening file: " + url)
    #     # fp = open(url)
    #     fp = codecs.open(url, "r", encoding='utf-8')
    #     log.debug("loading template...")
    #     # template = Template(fp.read(), Origin(url), template_name)
    #     template = Template(fp.read().encode('utf-8'), Origin(url), template_name)
    #     log.debug("closing file")
    #     fp.close()
    #
    # if template:
    #     log.debug("attempting to load context and render the template...")
    #     return render_page(request, template, module_name)
    # else:
    #     return None


class TemplateMeta:
    """
        encapsulates the core atts and methods to get a valid template
    """

    def __init__(self, request):
        # setup our basic attributes for the meta-data we will use for validation and template creation
        self.is_found = False
        self.request = request
        self.docroot_dir = getattr(settings, "DOCROOT_ROOT", "")
        log.debug("docroot dir: " + self.docroot_dir)
        self.original_path = request.path_info.strip()
        self.path = self.original_path
        if self.path.startswith("/"):
            self.path = self.path[1:]
        self.file_name = os.path.join(self.docroot_dir, self.path)
        log.debug("file: " + str(self.file_name))
        self.module_name = self.path
        self.template_name = self.path
        # try and modify urls for logic on how to pull the correct template
        self.find_template()

        if not settings.IGNORE_LANGUAGE_PREFIX:
            # if not found lets try and make sure it is not because of language
            if not self.is_found and request.LANGUAGE_CODE:
                # new code to make us django language aware (strip language code when looking for a template)
                # print('request lang: ' + str(request.LANGUAGE_CODE))
                # print('settings lang: ' + str(settings.LANGUAGE_CODE))
                # print('languages: ' + str(settings.LANGUAGES))
                lang = '/' + request.LANGUAGE_CODE + "/"
                if self.original_path.startswith(lang):
                    self.path = self.original_path[len(lang):]
                    self.file_name = os.path.join(self.docroot_dir, self.path)
                    log.debug("language stripped file: " + str(self.file_name))
                    self.module_name = self.path
                    self.template_name = self.path
                    # re-try and modify urls for logic on how to pull the correct template
                    self.find_template()

            # finally if we still don't have a template and ends with / and APPEND_SLASH is set and False strip it
            if not self.is_found and request.LANGUAGE_CODE and settings.APPEND_SLASH and self.original_path.endswith('/'):
                lang = '/' + request.LANGUAGE_CODE + "/"
                if self.original_path.startswith(lang):
                    # same as above except now try to strip the last slash
                    self.path = self.original_path[len(lang):len(self.original_path)-1]
                    self.file_name = os.path.join(self.docroot_dir, self.path)
                    log.debug("language stripped file: " + str(self.file_name))
                    self.module_name = self.path
                    self.template_name = self.path

                    # re-try and modify urls for logic on how to pull the correct template
                    self.find_template()


    # contains the logic for taking a request url and attempting to locate a page template for it
    def find_template(self):
        # if the url ends in .html then try to load a corresponding template from the docroot/files directory
        if self.file_name.endswith(".html"):
            # our url will request .html but we want to look for a .dt file (required for template processing)
            self.file_name = self.file_name[:-4]
            self.file_name += "dt"
            self.template_name = self.template_name[:-4]
            self.template_name += "dt"
            if os.path.isfile(self.file_name):
                log.debug("found file: " + self.file_name)
                self.is_found = True

        elif self.file_name.endswith('/'):
            self.file_name += "index.dt"
            if os.path.isfile(self.file_name):
                log.debug("found file: " + self.file_name)
                self.module_name += "index.html"
                self.template_name += "index.dt"
                self.is_found = True

        else:
            self.file_name += ".dt"
            if os.path.isfile(self.file_name):
                log.debug("found file: " + self.file_name)
                self.module_name += ".html"
                self.template_name += ".dt"
                self.is_found = True

    def render(self):
        if self.is_found:
            log.debug("opening file: " + self.file_name)
            fp = codecs.open(self.file_name, "r", encoding='utf-8')
            log.debug("loading template...")
            # template = Template(fp.read(), Origin(url), template_name)
            template = Template(fp.read().encode('utf-8'), Origin(self.file_name), self.template_name)
            log.debug("closing file")
            fp.close()

            if template:
                log.debug("attempting to load context and render the template...")
                return render_page(self.request, template, self.module_name)
            else:
                return None

    def is_found(self):
        return self.is_found

    def __str__(self):
        return self.file_name


@csrf_protect
def render_page(request, template, module_name):
    """
    Internal interface to the dev page view.
    """
    context = {}
    log.debug("template name: " + template.name)
    log.debug("module_name: " + module_name)
    datafile_name = template.origin.name
    # strip off the html and try data.py
    if datafile_name.endswith('dt'):
        datafile_name = datafile_name[0:len(datafile_name) - 2]
        datafile_name += 'data.py'
        log.debug("datafilename: " + datafile_name)
    # else:
    #     datafile_name += '.data.py'
    # try to load a data file if it is there in order to get the context
    # all data files should support get_context() or a context property
    try:
        log.debug("attempting to load data_file...")
        spec = importlib.util.spec_from_file_location(module_name, datafile_name)
        data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(data)

        # datafile = imp.load_source(module_name, datafile_name)
        # note changing datafile below to data
    except Exception:
        # logging.error(traceback.format_exc())
        data = None
    if data:
        try:
            initmethod = getattr(data, 'get_context')
        except AttributeError:
            initmethod = None
        if initmethod:
            context = initmethod(request)
        else:
            try:
                context = getattr(data, 'context')
            except AttributeError:
                context = {}
    # print("context string: " + str(context))
    template_context = RequestContext(request)
    if (context):
        template_context.push(context)
    response = HttpResponse(template.render(template_context))
    return response


# class based view for getting and putting cms content
class ContentApi(View):
    def get(self, request):
        db_content = None
        # get the requested uri
        uri = request.GET.get('uri', None)
        if uri:
            db_content = Content.objects.filter(uri=uri).values('uri', 'element_id', 'content')
        # return any content for this url
        return JsonResponse(list(db_content) or [], safe=False)

    def post(self, request):
        # save and return any content for this url
        received_json_data = json.loads(request.body.decode("utf-8"))
        # data = request.body.decode('utf-8')
        # received_json_data = json.loads(data)
        content = received_json_data.get('content', None)
        if content:
            uri = received_json_data.get('uri', '')
            element_id = received_json_data.get('element_id', None)
            # lookup a record for this uri, element_id combination
            try:
                db_content = Content.objects.get(uri=uri, element_id=element_id)
            except Content.DoesNotExist:
                db_content = None

            if db_content:
                db_content.content = content
                db_content.save()
            else:
                db_content = Content()
                db_content.uri = uri
                db_content.element_id = element_id
                db_content.content = content
                db_content.save()

            serialized_object = serializers.serialize('json', [db_content, ])
            return JsonResponse(serialized_object or [], safe=False)
        else:
            return HttpResponse(status=204)


# redo this after we figure out about the requests requirement
# class UrlValidationApi(View):
#     def get(self, request):
#         # we will attempt to validate every URL parameter passed in
#
#         is_valid = True
#
#         dict_buffer = {}
#         # list_dicts = []
#
#         items = request.GET.items()
#         if not items:
#             items = request.POST.items()
#         for _key, _val in items:
#             # build a json list and return it
#             print(_key, _val)
#             check_response = False
#             check_status = 500
#
#             try:
#                 r = requests.head(_val, allow_redirects=True)
#
#                 if r.status_code >= 200 and r.status_code < 400:
#                     check_status = r.status_code
#                     # if we were intercepted by a login screen then we treat that as a forbidden instead of success
#                     if r.request.path_url.lower().startswith('/en/admin/login/' or r.request.path_url.lower(
#                     ).startswith('/admin/login/')):
#                         # print('starts with login')
#                         check_response = False
#                         is_valid = False
#                         check_status = 403
#                     else:
#                         check_response = True
#                 else:
#                     check_response = False
#                     is_valid = False
#
#                 dict_buffer[_key] = {}
#                 dict_buffer[_key]["response"] = check_response
#                 dict_buffer[_key]["status_code"] = check_status
#                 # list_dicts.append(dict_buffer)
#
#             except Exception as e:
#                 is_valid = False
#                 dict_buffer[_key] = {}
#                 dict_buffer[_key]["response"] = False
#                 dict_buffer[_key]["status_code"] = 500
#                 # list_dicts.append(dict_buffer)
#
#         # myurl = request.GET.get("myurl", None)
#         # # try and do a lookup for the url passed
#         # myresponse = False
#         # mystatus = None
#         # try:
#         #     r = requests.head(myurl)
#         #     if r.status_code >= 200 and r.status_code < 400:
#         #         myresponse = True
#         #     mystatus=r.status_code
#         # except Exception as e:
#         #     mystatus=500
#         return JsonResponse({'valid': is_valid, 'results': dict_buffer})
