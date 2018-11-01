#!/usr/bin/python
# -*- coding: utf-8 -*-
#阿里云ECS服务器信息自动发现脚本
from __future__ import division
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
import json
__author__='Hoover'
class AliyunEcsDescribe():
    _AK='Your Key'
    _AKS='Your Key Secret'
    def __init__(self):
	self._client=client.AcsClient(self._AK,self._AKS)
	self._region=list()
	self._instances=list()

    def _get_region_info(self):
	c=client.AcsClient(self._AK,self._AKS)
	req=DescribeRegionsRequest()
	req.set_AcceptLanguage('zh-CN')
	req.set_accept_format('json')
	try:
	    response=c.do_action(req)
	    result=json.loads(response)
	    for region_info in result['Regions']['Region']:
		self._region.append(region_info['RegionId'])
	except Exception as e:
	    print e

    def get_region_info(self):
	self._get_region_info()
	return self._region

    def _get_instance_info(self,region):
	c=client.AcsClient(self._AK,self._AKS,region)
	req=DescribeInstancesRequest()
	req.set_PageSize(100)
	req.set_accept_format('json')
	page_number=0
	try:
	    response=c.do_action(req)
	    instances=json.loads(response)
	    total=instances['TotalCount']
	    page_size=instances['PageSize']
	    if total/page_size > total//page_size:
		page_number=total//page_size+1
	    else:
		page_number=total//page_size
	except Exception as e:
	    print e
	for p_n in range(1,page_number+1):
	    req.set_PageNumber(p_n)
	    response=c.do_action(req)
	    instances=json.loads(response)
	    for host_info in instances['Instances']['Instance']:
		region_id=host_info['RegionId']
		eip=host_info['EipAddress']['IpAddress']
		pip=host_info['PublicIpAddress']['IpAddress']
		instance_name=host_info['InstanceName']
		instance_id=host_info['InstanceId']
		host_name=host_info['HostName']
		if eip != "":
		    self._instances.append([region_id,instance_name,eip,instance_id])
		elif len(pip)>=1:
		    self._instances.append([region_id,instance_name,pip[0],instance_id])

    def format_instance_info(self):
	region=self.get_region_info()
        for r in region:
	    self._get_instance_info(r)
	printf,format_data={},[]
	for ecs_info in self._instances:
	    format_data.append({"{#EIP_REGION}":ecs_info[0],"{#EIP_RENAME}":ecs_info[1],"{#EIP_IP}":ecs_info[2],"#EIP_ID":ecs_info[3]})

	printf['data']=format_data
	print json.dumps(printf,sort_keys=True,indent=4,ensure_ascii=False,separators=(',',':'))
	


if __name__=='__main__':
    ecs=AliyunEcsDescribe()
    ecs.format_instance_info()
