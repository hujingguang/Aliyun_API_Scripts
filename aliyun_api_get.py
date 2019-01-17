#!/usr/local/python2.7/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815.DescribeDBInstancesRequest import DescribeDBInstancesRequest
import json
import sys
reload(sys) 
from datetime import datetime
from datetime import timedelta
import time
import urllib
import urllib2
from datetime import datetime
import random	
import hmac
import hashlib
import base64
import requests
sys.setdefaultencoding('utf8')
__author__='hjg'


def get_iso8601():
    '''
    FORMAT_ISO8601="%Y-%m-%dT%H:%M:%SZ"
    import time
    return time.strftime(FORMAT_ISO8601,time.gmtime())
    '''
    return datetime.strftime(datetime.utcnow(),"%Y-%m-%dT%H:%M:%SZ")

def get_randint():
    '''
    import uuid
    return str(uuid.uuid4())
    '''
    return random.randint(10000000000000,99999999999999)


def get_all_parameters(userData,action,accessKeyId,version):
    timestamp=get_iso8601()
    nonce=get_randint()
    parameters={
               "Format":"JSON",
               "Version":version,
               "AccessKeyId":accessKeyId,
               "SignatureMethod":"HMAC-SHA1",
               "Timestamp":timestamp,
               "SignatureVersion":"1.0",
               "SignatureNonce":str(nonce),
               "Action":action
               }
    for (k,v) in sorted(userData.iteritems()):
        parameters[k]=v
    return parameters

def get_param_string(parameter):
    param_str=''
    for (k,v) in sorted(parameter.iteritems()):
        param_str+='&'+urllib.quote(k,safe='')+'='+urllib.quote(v,safe='')
    return param_str[1:]


def get_signature_str(parameter,param_str,aks):
    stringTosign="GET"+'&%2F&'+urllib.quote(param_str,safe='')
    hm=hmac.new(aks,stringTosign,hashlib.sha1)
    signature_str=base64.encodestring(hm.digest()).strip()
    return signature_str


def do_request():
    user_data={"RegionId":"cn-beijing"}
    action="DescribeDBInstances"
    ak="Your Aliyun AK ID"
    aks="Your Aliyun AK Secret"
    version="2014-08-15"
    parameter=get_all_parameters(user_data,action,ak,version)
    print parameter
    param_str=get_param_string(parameter) 
    print param_str
    signature=get_signature_str(parameter,param_str,aks)
    print signature
    #server_url='http://gpdb.aliyuncs.com/?'
    server_url='http://gpdb.aliyuncs.com/?'
    param_str=param_str+"&Signature="+urllib.quote(signature,safe='')
    request_url=server_url+param_str
    print request_url
    response=requests.get(request_url)
    print response.content
    

    

def main(server_url,ak,aks,action,user_data):
    server_url='http://'+server_url+'/?'




if __name__=='__main__':
    do_request()
