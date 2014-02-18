# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from wp_helper.service import WPService
from settings import WP_PARAMS
from estatebase.models import Estate
from django.utils import translation
from wp_helper.models import EstateWordpressMeta
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')        
        wp_service = WPService(WP_PARAMS['site'])
        self.sync_correct(wp_service)      

    def sync_correct(self, wp_service):
        estates = Estate.objects.filter(wp_meta__status=EstateWordpressMeta.XMLRPC)
        for estate in estates:
            time.sleep(10)            
            wp_service.sync_post(estate)
            
        
        