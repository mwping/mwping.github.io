#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import requests
import json
import yaml
import sys

def read(path):
	file = open(path,'r')
	result = file.read()
	file.close()
	return result

def upload():
	variants = json.loads(read("./variants.json"))
	count = len(variants)

	print "Code","Task"
	for i in range(0, count):
		item = variants[i]
		print " %d " % i," assemble%s" % item['name']
	code = -1
	while code < 0 or code >= count:
		code = input("Select an task number(>=%d and <%d): " % (0, count))

	variant = variants[code]
	cmd = "./gradlew clean assemble%s" % (variant['name'])

	sure = raw_input("You are going to run cmd: %s\nAre you sure?(Y or N)" % cmd)
	if sure != "Y" and sure != "y":
		print "Task is canceled!"
		return

	firstFlavor = variant['flavorList'][0]

	changelogPath = r'changelog_%s.yml' % firstFlavor
	if os.access(changelogPath, os.F_OK) == False:
		print "You need a changelog_%s.yml" % firstFlavor
		return

	changelogFile = open(changelogPath)

	print "Run cmd: %s" % cmd
	os.system(cmd)

	base_url = 'https://apps.springtech.info/apps'


	cfg = yaml.load_all(changelogFile, yaml.SafeLoader)
	latest=next(cfg)['changelog']
	changelog=''
	for item in latest:
		changelog += '- ' + item + '\n'

	app_file_path = variant['path']

	print app_file_path, changelog

	files = {'file' : open(app_file_path, 'r')}
	datas = {'changelog' : changelog}

	resp = requests.post(base_url, files=files, data=datas)
	
	if resp.status_code != requests.codes.ok:
		print 'Error!', resp.text
	else:
		content = json.loads(resp.content)
		print 'Name:', content['name'] + '\nVersion:', content['version'] + '\nPackage url:', (base_url + 'app/' + content['package'])

if __name__ == "__main__":
	upload()


