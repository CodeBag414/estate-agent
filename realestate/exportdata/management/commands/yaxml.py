# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from exportdata.custom_makers.yaxml import YandexXML
import pinject

class Command(BaseCommand):
    def handle(self, *args, **options):
        use_cache = not 'nocache' in args        
        obj_graph = pinject.new_object_graph()
        feed = obj_graph.provide(YandexXML)        
        feed.gen_XML(use_cache)
        