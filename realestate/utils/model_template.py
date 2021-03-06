# -*- coding: utf-8 -*-
from django.utils.encoding import force_unicode

capfirst = lambda x: x and force_unicode(x)[0].upper() + force_unicode(x)[1:]

class ModelMaker(object):
    
    template = \
"""
class %(cname)s(SimpleDict):
    '''
    %(cname)s
    %(corig)s = models.ForeignKey(%(cname)s,verbose_name=_('%(cname)s'),%(cblank)s)
    '''
    class Meta(%(cmeta)s):
        verbose_name = _('%(cverb)s')
        verbose_name_plural = _('%(cverb_p)s')
"""
    
    def __init__(self,base_model,model_name,base_model_meta='parent'):
        self.base_model = base_model
        self.base_model_meta = base_model_meta
        self.model_name = model_name           
    def get_meta(self):
        if self.base_model_meta == 'parent':
            return '%s.Meta' % self.base_model
        else:
            return self.base_model_meta
    @property    
    def model_name_parts(self):
        return self.model_name.split('_')
    
    def get_params(self):
        cparam = {'cname':''}  
        for name in self.model_name_parts:
            cparam['cname'] += capfirst(name)            
        cparam['cmeta'] = self.get_meta()
        cparam['cverb'] = capfirst(' '.join(self.model_name_parts))    
        cparam['cverb_p'] = '%ss' % cparam['cverb']
        cparam['corig'] = self.model_name
        cparam['cblank'] = 'blank=True,null=True'
        return cparam    
    
    def get_model_code(self):
        return self.template % self.get_params()


class FixtureSimpleMaker(object):
    c_template = \
'''{
    "pk": %(pk)s,
    "model": "%(model)s",
    "fields": {
        "name": "%(name)s",
        "order": "%(pk)s"                
    }
}'''
    a_template = \
'''{
    "pk": %(pk)s,
    "model": "%(model)s",
    "fields": {
        "name": "%(0)s"
    }
}'''    
    
    p_template = \
'''{
    "pk": %(pk)s,
    "model": "%(model)s",
    "fields": {
        "name": "%(0)s",
        "prep_name":"%(1)s" 
    }
}'''    
    
    
    def __init__(self,app_name,model_name,name_list):
        self.model_name = '%s.%s' % (app_name.lower(), model_name.lower())        
        self.name_list = name_list
        self.fixfile = '%s.json' % model_name.lower()
        self.template = self.p_template    
    def get_json(self):
        pk = 1
        result = []
        lines = self.name_list.splitlines()
        lines = sorted(lines)
        fields = None
        json_fields ={}        
        for line in lines:            
            try:                
                if line: 
                    fields = line.split(';')                    
                    for ind, val in enumerate(fields):
                        json_fields['%s' % ind] = capfirst(val.strip())                  
            except:                
                pass    
            if len(json_fields):                
                template_dict = {'model':self.model_name,'pk':pk}
                template_dict.update(json_fields)                             
                result.append(self.template % template_dict)
                pk += 1   
        return result


'''

path = 'c://Users//picasso//My Documents//Aptana Studio 3 Workspace//estate-agent//realestate//'
f = open("%stemp.json" % path, 'rb').read().decode("unicode_escape").encode("utf8")
open("%stemp.json" % path, 'wb').write(f)

Загрузить все файлы
find . -name "*.json" -exec manage.py loaddata {} \;

Регулярка для вытаскивания опций их списка select
^.*>(.*)<\/.*$
\1
'''

options = \
'''
город;городе
село;селе
поселок;поселке
хутор;хуторе
'''


MODEL = 'FeedLocality'

import settings
import os

FIXTURE_ROOT = os.path.join(settings.SITE_ROOT, 'estatebase', 'fixtures')

fm = FixtureSimpleMaker('estatebase',MODEL,options)
fixfile = os.path.join(FIXTURE_ROOT, fm.fixfile)
if not os.path.isfile(fixfile):
    open(fixfile, 'wb').write('[\n%s\n]' % ','.join(fm.get_json()))
    print './manage.py loaddata %s' % fm.fixfile 
else:
    print ','.join(fm.get_json())
    print 'Fixture already exists!'     



mm = ModelMaker('SimpleDict', 'gear')
print mm.get_model_code()