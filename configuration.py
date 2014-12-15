'''
Created on 15 Dec 2014

@author: kehurley
'''
import ConfigParser
import os
import logging


class Configuration(object):
    '''
    Holds configuration and option settings
        os.environ["http_proxy"]="http://emea-proxy-pool.eu.alcatel-lucent.com:8000"
        os.environ["https_proxy"]="https://emea-proxy-pool.eu.alcatel-lucent.com:8000"
    '''

    def __init__(self):
        '''
        Constructor
        '''
        logging.debug("configuration.Configuration constructor")
        self.usage_string="No help available"
        self.opts={
                   "hts_server_ip": {"value":"crookshanks.lan"},
                   "hts_server_username":{"value":"hts"},
                   "hts_server_password":{"value":"hts"},
                   "behind_firewall":{"value":True, 'type':'bool'},
                   "http_proxy":{"value": "http://emea-proxy-pool.eu.alcatel-lucent.com:8000"},
                   "https_proxy":{"value":"https://emea-proxy-pool.eu.alcatel-lucent.com:8000"},
                   }
        
    def parse_config_file(self, cfg_file="library.cfg"):
        if os.path.exists(cfg_file):
            logging.debug("parsing %s"%cfg_file)
            cfg_parser=ConfigParser.ConfigParser()
            cfg_parser.read(cfg_file)
            if "general" in cfg_parser.sections():
                for s in cfg_parser.items('general'):
                    key=s[0]
                    val=s[1]
                    if key in self.opts:
                        entry=self.opts[key]
                        if 'type' in entry:
                            val=eval(entry['type']+"("+val+")")
                        logging.debug("setting %s to %s"%(key,val))
                        entry['value']=val
    
    def __getattr__(self,attr):
        """ expose values in opts dictionary as though they were members of this class """  
        try:
            return self.opts[attr]["value"]
        except Exception:
            raise AttributeError, attr
        
    def apply(self):
        if self.behind_firewall:
            logging.debug("setting http(s) proxies")
            os.environ["http_proxy"]=self.http_proxy
            os.environ["https_proxy"]=self.https_proxy
            
            