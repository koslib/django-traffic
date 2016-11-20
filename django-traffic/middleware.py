# -*- coding: utf-8 -*-
# Author: Konstantinos Livieratos <livieratos.konstantinos@gmail.com>
# https://github.com/koslibpro/django-traffic/

import logging

import django
from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.contrib.gis.geoip2 import GeoIP2

from elasticsearch import Elasticsearch


class ESTrafficInfoMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response

        if settings.TRAFFIC_INDEX_NAME:
            self.index_name = settings.TRAFFIC_INDEX_NAME
        else:
            self.index_name = "django-traffic"

        self.geo_db_path = settings.GEO_DB_PATH

        if settings.ES_CLIENT:
            self.es = settings.ES_CLIENT
        else:
            assert settings.ES_HOST, 'ES_HOST definition in settings.py is required'
            self.es = Elasticsearch(
                hosts=[settings.ES_HOST]
            )

        super(ESTrafficInfoMiddleware, self).__init__(get_response=get_response)

    def process_request(self, request, *args, **kwargs):
        self.es_upstream(request)
        return None

    def es_upstream(self, request):
        device_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        device_ip = str(device_ip).split(',')[0]
        logging.info("[django-traffic] Device IP: %s" % device_ip)

        if not self.es.indices.exists(index=self.index_name):
            mapping = {
                "mappings": {
                    "request-info": {
                        "properties": {
                            "timestamp": {
                                "type": "date"
                            },
                            "text": {
                                "type": "string"
                            },
                            "location": {
                                "type": "geo_point"
                            },
                            "method": {
                                "type": "string"
                            },
                            "body": {
                                "type": "string"
                            },
                            "path": {
                                "type": "string"
                            },
                            "path_info": {
                                "type": "string"
                            },
                            "scheme": {
                                "type": "string"
                            },
                            "encoding": {
                                "type": "string"
                            },
                            "encoding_type": {
                                "type": "string"
                            },
                            "ip_addr": {
                                "type": "ip"
                            }
                        }
                    }
                }
            }
            logging.info("[django-traffic] Creating new elasticsearch indice...")
            self.es.indices.create(index=self.index_name, body=mapping)

        if self.geo_db_path is None:
            # assume the user has set GEOIP_PATH in settings.py
            g = GeoIP2()
        else:
            g = GeoIP2(path=self.geo_db_path)
        try:
            lat, lng = g.lat_lon(device_ip)
        except Exception as e:
            logging.error("[django-traffic] Error while getting lan/lon from GEOIP2: %s " % e)
            return

        doc = {
            "timestamp": timezone.now(),
            "text": "django-traffic geo-point object",
            "location": {
                "lat": lat,
                "lon": lng
            },
            "method": request.method,
            "body": request.body,
            "path": request.path,
            "path_info": request.path_info,
            "scheme": request.scheme,
            "encoding": request.encoding,
            "encoding_type": request.encoding_type if django.get_version() > '1.10' else '',
            "ip_addr": device_ip
        }

        res = self.es.index(index=self.index_name, doc_type='request-info', body=doc)
        if res['created']:
            logging.info("[django-traffic] request indexed")
