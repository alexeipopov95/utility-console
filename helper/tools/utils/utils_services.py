from datetime import datetime
from django.conf import settings
import requests
import json
import os

class UtilsService(object):
    BASE_DIR = settings.BASE_DIR
    DNS_JSON = os.path.join(BASE_DIR, 'tools', 'templates', 'json', 'rdap_dns.json')

    # @params None
    def make_dns_json(self):
        """ fills a json file with the urls and their respective TLDs to request latters """

        try:
            rdap_dns = requests.get('https://data.iana.org/rdap/dns.json')

            if rdap_dns.status_code == 200:
                response = rdap_dns.json()
                with open(self.DNS_JSON, 'w') as outfile:
                    json.dump(response, outfile)

                    print "[%12s] %5s %15s" % (
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        '[DONE]',
                        'rdap_dns.json created',
                    )

            else:
                print "[%12s] %5s %15s" % (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    '[FAIL]',
                    'Http Status Code: [ %s ]' % rdap_dns.status_code,
                )

        except Exception as MakeDnsListError:
            print "[%12s] %5s %15s" % (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                '[FAIL]',
                MakeDnsListError.__str__(),
            )


    # @params domain STR.
    def get_rdap_url(self, domain):
        """ get the url corresponding to the domain or None """

        try:
            with open(self.DNS_JSON,'r') as dns_list:
                dns_list = json.loads(dns_list.read())

            if dns_list:
                for keys in dns_list['services']:
                    for domain_extension in keys[0]:
                        if domain.endswith('.%s' % domain_extension):
                            for link in keys[1]:
                                return '%sdomain/%s' % (link, domain)

        except Exception as GetRdapUrlError:
            print "[%12s] %5s %5s %5s" % (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                '[FAIL]',
                '[get_rdap_url]',
                GetRdapUrlError.__str__(),
            )
            return None


    # @params domain STR.
    def rdap_data_provider(self, domain):
        """ Make a request to the URL provided by get_rdap_url and return a json """

        rdap_data = {
            'status'  : False,
            'response': {},
            'error'   : {},
        }

        try:
            rdap_url  = self.get_rdap_url(domain)
            if rdap_url:
                json_data = requests.get(rdap_url)

                if json_data.status_code == 200:
                    rdap_data['status']           = True
                    rdap_data['response']['data'] = json.loads(json_data.text)
                    rdap_data['url']              = rdap_url

                else:
                    rdap_data['status']            = False
                    rdap_data['response']          = {}
                    rdap_data['error']['internal'] = "Status Code [ %s ]" % json_data.status_code

            else:
                rdap_data['status']           = False
                rdap_data['error']['internal'] = 'rdap_url is None in: self.get_rdap_url(domain)'


        except Exception as RdapDataProviderError:
            rdap_data['status']            = False
            rdap_data['error']['internal'] = RdapDataProviderError.__str__()

        return rdap_data



