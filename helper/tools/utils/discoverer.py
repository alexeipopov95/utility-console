# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Custom
from tools.utils.utils_services import UtilsService

#Python
import dns.resolver
import requests
import tldextract
import subprocess
import platform
import json


class DomainDiscover(UtilsService):
    

    # @params domain STR
    def get_domain(self, domain):
        """ return the domain """

        tldObject = None
        try:
            tldObject = tldextract.extract(domain).domain
        except Exception as Error:
            print("[DomainDiscover] - get_domain\n%s" % Error)

        return tldObject


    # @params domain STR
    def get_subdomain(self, domain):
        """ return the subdomain of the domain """

        tldObject = None
        try:
            tldObject = tldextract.extract(domain).subdomain
        except Exception as Error:
            print("[DomainDiscover] - get_subdomain\n%s" % Error)

        return tldObject


    # @params domain STR
    def get_suffix(self, domain):
        """ return the suffix of the domain """

        tldObject = None
        try:
            tldObject = tldextract.extract(domain).suffix
        except Exception as Error:
            print("[DomainDiscover] - get_suffix\n%s" % Error)
        
        return tldObject


    # @params json from RDAP
    def get_rdap_events(self, json_data):
        """ get expiration, update and creation dates from rdap protocol """

        eventData  = {
            'creation_date'  : None,
            'expiration_date': None,
            'last_date_rdap' : None,
            'last_date'      : None
        }
        try:
            for event in json_data['events']:
                if event['eventAction'] == 'registration':
                    eventData['creation_date'] = event['eventDate']

                if event['eventAction'] == 'expiration':
                    eventData['expiration_date'] = event['eventDate']

                if event['eventAction'] == 'last update of RDAP database':
                    eventData['last_date_rdap'] = event['eventDate']

                if event['eventAction'] == 'last changed':
                    eventData['last_date'] = event['eventDate']

        except Exception as Error:
            print("[DomainDiscover] - get_rdap_events\n%s" % Error)

        return eventData

    
    # @params json from RDAP
    def get_nameservers(self, json_data):
        """ get the dns of a domain from rdap protocol """

        dns = []
        try:
            if 'nameservers' in json_data:
                while len(dns) < (len(json_data['nameservers'])):
                    dns.append(json_data['nameservers'][len(dns)]['ldhName'].lower())

        except Exception as Error:
            print("[DomainDiscover] - get_nameservers\n%s" % Error)

        return dns


    # @params domain STR
    def ping(self, domain):
        """ make a ping using subprocess command to retrive the status of the domain """

        result = "Name or service not know"
        try:
            param = None
            if platform.system().lower() == "windows":
                param = "-n"
            else:
                param = "-c"
            
            command = subprocess.check_output(['ping', param, '5', domain])
            result  = "".join(command).split('\n')
        except Exception as Error:
            print("[DomainDiscover] - ping\n%s" % Error)
        
        return result


    # @params domain STR
    def get_information(self, domain, json_data):
        """ get basic information about the domain """

        domain_data = {
            'entity' : None,
            'cuit'   : None,
            'name'   : None,
        }

        try:
            if domain.endswith('.ar') or domain.endswith('com.ar'):
                domain_data['entity'] = "Nic Argentina"
                
                for elements in json_data['response']['data']['entities'][0]:
                    domain_data['cuit'] = json_data['response']['data']['entities'][0]['handle']
                for url in json_data['response']['data']['entities'][0]['links']:
                    response = requests.get(url['href'])
                    domain_data['name'] = json.loads(response.text)['vcardArray'][1][1][-1]
            else:
                domain_data['entity'] = json_data['response']['data']['entities'][0]['vcardArray'][1][1][-1]
                domain_data['cuit']   = "Datos restringidos"
                domain_data['name']   = "Datos restringidos"
            
        except Exception as Error:
            print("[DomainDiscover] - get_information\n%s" % Error)
        
        return domain_data


    # @params domain STR, nameservers LIST
    def nslookup(self, domain, nameservers=None):
        """ make a nslookup to the domain and the nameservers of the domain """
        domain_data = {
            'A'     : None,
            'MX'    : None,
            'A-DNS' : None,
        }
        a_records     = []
        mx_records    = []
        a_dns_records = []

        try:
            has_subdomain = self.get_subdomain(domain)
            if has_subdomain:
                domain = domain.replace("%s." % has_subdomain,'')

            #A record for domain only
            domain_a = dns.resolver.query(str(domain),'A')
            for A in domain_a:
                a_records.append(A)
            domain_data['A'] = a_records

            #MX record for domain only
            domain_mx = dns.resolver.query(str(domain),'MX')
            for MX in domain_mx:
                mx_records.append(MX)
            domain_data['MX'] = mx_records

            #A-DNS record for nameservers
            if nameservers:
                for nameserver in nameservers:
                    nameserver_a = dns.resolver.query(str(nameserver),'A')
                    for ADNS in nameserver_a:
                        a_dns_records.append(ADNS)
                domain_data['A-DNS'] = a_dns_records

        except Exception as Error:
            print("[DomainDiscover] - nslookup\n%s" % Error)
        
        return domain_data


    # @params domain STR
    def discover(self, domain):
        """ main method of DomainDiscover in charge of gather all the relevant information about the domain """

        domain_data = {
            'domain'        : None,
            'subdomain'     : None,
            'suffix'        : None,
            'events'        : None,
            'nameservers'   : None,
            'domain_ping'   : None,
            'subdomain_ping': None,
            'nslookup'      : None,
            'extra_data'    : None,
            'status'        : False,
        }

        try:

            has_subdomain = self.get_subdomain(domain)
            if has_subdomain:

                domain_data['subdomain_ping'] = self.ping(domain)
                domain = domain.replace("%s." % has_subdomain,'')

            json_data = self.rdap_data_provider(domain)

            if json_data['status']:
                _domain     = self.get_domain(domain)
                _subdomain  = self.get_subdomain(domain)
                _suffix     = self.get_suffix(domain)
                _ping       = self.ping(domain)
                _dns        = self.get_nameservers(json_data=json_data['response']['data'])
                _events     = self.get_rdap_events(json_data=json_data['response']['data'])
                _extra_data = self.get_information(domain, json_data)

                domain_data['domain']      = _domain
                domain_data['subdomain']   = _subdomain
                domain_data['suffix']      = _suffix
                domain_data['domain_ping']        = _ping
                domain_data['events']      = _events
                domain_data['nameservers'] = _dns
                domain_data['extra_data']  =_extra_data

                if _events['expiration_date']:
                    domain_data['status'] = True

                if len(_dns) > 0:
                    _nslookup  = self.nslookup(domain, nameservers=_dns)
                    domain_data['nslookup'] = _nslookup

        except Exception as Error:
            print("[DomainDiscover] - discover\n%s" % Error)

        return domain_data


