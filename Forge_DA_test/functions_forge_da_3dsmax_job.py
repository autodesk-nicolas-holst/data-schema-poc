# python implementation equivalent of createanduploadapp.js

import os, requests,json,time,string,zipfile
from pymxs import runtime as rt


#############################################################################################
#############################################################################################
##
## Log in
##
#############################################################################################
#############################################################################################
def login(scope):
	token=""
	client_id=""
	if os.path.exists("d:/d/forge2018/client_id.txt"): 
		f=open("d:/d/forge2018/client_id.txt","r")
		client_id=f.read()
		f.close()
		
	client_secret=""
	if os.path.exists("d:/d/forge2018/client_secret.txt"):
		f=open("d:/d/forge2018/client_secret.txt","r")
		client_secret=f.read()
		f.close()
		
	d={'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials', 'scope': scope}
	t=requests.post("https://developer.api.autodesk.com/authentication/v1/authenticate", data=d)

	if t.status_code==200:
		token="%s %s"%(t.json()['token_type'],t.json()['access_token'])

	return t.status_code,token,client_id
	
	
#############################################################################################
#############################################################################################
##
## Delete the app bundle if it already exists
##
#############################################################################################
#############################################################################################
def delete_appbundle(token,appbundle_id):
	h={"Authorization": token}
	url="https://developer.api.autodesk.com/da/us-east/v3/appbundles/%s"%(appbundle_id)
	t=requests.delete(url, headers=h)
	status=400
	if t.status_code==404:
		#print "\n\nsuccess: no old app bundle found"
		status=200
	elif t.status_code==204:
		#print "\n\nsuccess: old app bundle deleted"
		status=200
	else:
		pass
		#print "failed to delete app bundle!",t.status_code

	return status


#############################################################################################
#############################################################################################
##
##Create the new app bundle
##
#############################################################################################
#############################################################################################
def create_appbundle(token,appbundle_id):
	url='https://developer.api.autodesk.com/da/us-east/v3/appbundles' 
	h={"Authorization": token,  "Content-Type": "application/json"}
	d={"id": appbundle_id,"engine": "Autodesk.3dsMax+2019","description": "March 1st test"}
	t=requests.post(url,headers=h,json=d)
	
	uploadparameters={}
	if t.status_code==200:
		uploadparameters=t.json()["uploadParameters"]

	return t.status_code,uploadparameters
	

#############################################################################################
#############################################################################################
##
## Zip the bundle up
##
#############################################################################################
#############################################################################################
def zip_app_bundle(zipfilename,folder_to_zip):
	z=zipfile.ZipFile(zipfilename, mode='w', compression=zipfile.ZIP_DEFLATED)
	f=string.replace(folder_to_zip,"/","\\")
    
	for foldername, subfolders, filenames in os.walk(folder_to_zip):
		archive_folder_name=os.path.relpath(foldername, folder_to_zip)
		#print archive_folder_name
		if archive_folder_name!=".":
			z.write(foldername, arcname=archive_folder_name)
		for filename in filenames:
			if filename[-4:]!=".zip":
				z.write(os.path.join(foldername, filename), arcname=os.path.join(archive_folder_name, filename))
	z.close()
	

#############################################################################################
#############################################################################################
##
## Upload the new app bundle
##
#############################################################################################
#############################################################################################
def upload_appbundle(token,appbundlefile,uploadparameters):
	# uploading the app package
	#print t.json()["engine"]
	#print t.json()["id"]
	#print t.json()["version"]
	#print t.json()["description"]
	#print t.json()["uploadParameters"]

	#my_app_id=t.json()["id"]
	#print my_app_id
	#my_app_version=t.json()["version"]
	#print my_app_version

	aws_url=uploadparameters["endpointURL"] #"https://bucketname.s3.amazonaws.com/"
	aws_d=uploadparameters["formData"]
#	print d

	f=open(appbundlefile,'rb')
	rf=f.read()
	f.close()

	aws_f={"file": rf}
	t=requests.post(aws_url, data=aws_d,files=aws_f)
	#print t
	#print t.status_code
	
	
	return t.status_code
	

#############################################################################################
#############################################################################################
##
## Create an alias for the app bundle 
##
#############################################################################################
#############################################################################################
def create_appbundle_alias(token,appbundle_id,appbundle_alias):
	# create an app bundle alias
	#print "\n\ncreating an alias for the app bundle"

	url="https://developer.api.autodesk.com/da/us-east/v3/appbundles/%s/aliases"%(appbundle_id)
	h={"Authorization": token,  "Content-Type": "application/json"}
	d={"id": appbundle_alias, "version": 1}
	t=requests.post(url,headers=h, data=json.dumps(d))
	#print t
	#print t.status_code
	#print t.json()
	return t.status_code

#############################################################################################
#############################################################################################
## 
## Show all available app bundles - SKIPPED
##
#############################################################################################
#############################################################################################
def list_appbundle_alias(token,appbundle_id,client_id):
	appbundles=[]
	
	h={"Authorization": token}
	url="https://developer.api.autodesk.com/da/us-east/v3/appbundles"
	page=""
	t=requests.get(url, headers=h)
	if t.status_code==200: 
		#print "\n\ngetting the available app bundles"
		page=t.json()["paginationToken"]
		for i in t.json()["data"]:
			appbundles.append((i))
		while page!="":
			url="https://developer.api.autodesk.com/da/us-east/v3/appbundles?page=%s"%(page)
			h={"Authorization": token}
			t=requests.get(url, headers=h)
			page=""
			#print t
			#print t.status_code
			#print t.json()
			if t.status_code==200:
				page=t.json()["paginationToken"]
				for i in t.json()["data"]:		
					appbundles.append((i))

	return 200,appbundles

def pretty_print_list(list,client_id):
	# only show 3ds Max and this client_id related items
	for i in list:
		if string.find(i,"3dsMax")!=-1:
			print "   3ds Max:",i
		if string.find(i,client_id)!=-1:
			print "   This app:",i


#############################################################################################
#############################################################################################
##
## Delete the activity if it already exists
##
#############################################################################################
#############################################################################################
def delete_activity(token,activity_id):
	h={"Authorization": token}
	url="https://developer.api.autodesk.com/da/us-east/v3/activities/%s"%(activity_id)
	t=requests.delete(url, headers=h)
	#print t
	# success is either 404 when we've never uploaded it, or 204 if the delete was successfull
	status=400
	if t.status_code==404:
		#print "\n\nsuccess: no old activity found"
		status=200
	elif t.status_code==204:
		#print "\n\nsuccess: old activity deleted"
		status=200
	else:
		pass
		#print "failed to delete activity!",t.status_code

	return status


#############################################################################################
#############################################################################################
##
## Create the new activity
##
#############################################################################################
#############################################################################################
def create_activity(token,activity_id,appbundle_id,client_id):
	#print "create an activity for the app bundle"

	url="https://developer.api.autodesk.com/da/us-east/v3/activities"
	h={"Authorization": token,  "Content-Type": "application/json"}
	d={ "id":  activity_id,    "commandLine": "$(engine.path)/3dsmaxbatch.exe -sceneFile \"$(args[InputFile].path)\" \"$(settings[script].path)\"",    "description": "Export a single max file to FBX",     "appbundles": [client_id+"."+appbundle_id+"+prod"],    "engine" :  "Autodesk.3dsMax+2019",    "parameters": {        "InputFile" : {            "zip": False,            "description": "Input 3ds Max file",            "ondemand": False,            "required": True,            "verb": "get",            "localName": "input.max"        },        "OutputFile": {            "zip": False,            "ondemand": False,            "verb": "put",            "description": "Output FBX file",             "required": True,            "localName": "output.fbx"        }    },    "settings": {        "script": "exportFile (sysInfo.currentdir + \"/output.fbx\") #noPrompt using:FBXEXP"    }}	
	#print d
	t=requests.post(url,headers=h, data=json.dumps(d))
	#print t
	#print t.status_code
	#print t.json()
	
	return t.status_code


#############################################################################################
#############################################################################################
##
## Create an alias for the new activity
##
#############################################################################################
#############################################################################################
def create_activity_alias(token,activity_id,alias):
	#print "\n\ncreate an alias for the activity"
			
	#print activity_id
	url="https://developer.api.autodesk.com/da/us-east/v3/activities/%s/aliases"%(activity_id)
	h={"Authorization": token,  "Content-Type": "application/json"}
	d={"id": alias, "version": 1}
	t=requests.post(url,headers=h, data=json.dumps(d))
	#print t
	#print t.status_code
	#print t.json()
	return t.status_code


#############################################################################################
#############################################################################################
##
## List available activities
##
#############################################################################################
#############################################################################################
def list_activities(token):
	#print "\n\ncheck available activities"
	activities=[]
	# check what we have available
	url="https://developer.api.autodesk.com/da/us-east/v3/activities"
	h={"Authorization": token}
	t=requests.get(url, headers=h)
	page=""
	#print t
	#print t.status_code
	#print t.json()


	if t.status_code==200: 
		#print "\n\ngetting the available activities"
		page=t.json()["paginationToken"]
		for i in t.json()["data"]:
			activities.append((i))
		while page!="":
			url="https://developer.api.autodesk.com/da/us-east/v3/activities?page=%s"%(page)
			h={"Authorization": token}
			t=requests.get(url, headers=h)
			page=""
			#print t
			#print t.status_code
			#print t.json()
			if t.status_code==200:
				page=t.json()["paginationToken"]
				for i in t.json()["data"]:
					activities.append((i))
	return activities




#############################################################################################
#############################################################################################
##
## Upload the scene file
##
#############################################################################################
#############################################################################################
def upload_file(token,bucketname,file_to_upload,object_name):
	# read the file in
	f=open(file_to_upload,"rb")	
	d=f.read()
	f.close()

	h={"Authorization": token, "x-ads-region":  "US",  "Content-Type": "text/plain; charset=UTF-8", "Content-Disposition": file_to_upload, "Content-Length": "%s"%(len(d))}
	t=requests.put("https://developer.api.autodesk.com/oss/v2/buckets/%s/objects/%s"%(bucketname,object_name), headers=h, data=d)

	return t.status_code


#############################################################################################
#############################################################################################
##
## Create the bucket
##
#############################################################################################
#############################################################################################
def create_bucket(token,bucketname,bucket_region,bucket_type):
	h={"Authorization": token,"Content-Type": "application/json", "x-ads-region": bucket_region}
	d={"bucketKey": bucket_name, "policyKey": bucket_type}
	t=requests.post("https://developer.api.autodesk.com/oss/v2/buckets", headers=h, data=json.dumps(d))
	
	return t.status_code


#############################################################################################
#############################################################################################
##
## Getting the bucket details
##
#############################################################################################
#############################################################################################
def get_bucket(token,bucketname,bucket_region):
	h={"Authorization": token,"Content-Type":  "application/json", "x-ads-region": bucket_region}
	d={}
	t=requests.get("https://developer.api.autodesk.com/oss/v2/buckets/%s/details"%(bucketname), headers=h)

	bucket=""
	if t.status_code==200:
		if "bucketKey" in t.json() and t.json()["bucketKey"]==bucketname:
			bucket=bucketname
			
	return t.status_code,bucket

	
#############################################################################################
#############################################################################################
##
## Getting the signed url of the uploaded file
##
#############################################################################################
#############################################################################################
def get_signed_url(token,bucketname,objectname,bucket_region,access):
	url="https://developer.api.autodesk.com/oss/v2/buckets/%s/objects/%s/signed%s"%(bucketname,objectname,access)
	h={"Authorization": token,  "Content-Type": "application/json", "x-ads-region": bucket_region}
	t=requests.post(url, headers=h,json={})
	
	url=""
	if t.status_code==200:
		url=t.json()["signedUrl"]
	
	return t.status_code,url
	
		
#############################################################################################
#############################################################################################
##
## Submit the workitem
##
#############################################################################################
#############################################################################################
def submit_workitem(token,activity_id,client_id,input_url,output_url):
	h={"Authorization": token,  "Content-Type": "application/json"}
	d={"activityId": client_id+"."+activity_id , "arguments": {"InputFile": {"url": input_url ,"verb": "get"}, "OutputFile": {"url": output_url,"verb": "put"} }}
	url="https://developer.api.autodesk.com/da/us-east/v3/workitems"
	#print d
	t=requests.post(url, headers=h, data=json.dumps(d))
	#print t
	#print t.status_code
	#print t.json()
	workitem_id=""
	if t.status_code==200:
		workitem_id=t.json()["id"]
		
	return t.status_code,workitem_id


#############################################################################################
#############################################################################################
##
## Wait for the workitem to complete
##
#############################################################################################
#############################################################################################
def wait_for_workitem(token,workitem_id):
	s="pending"

	while s=="pending":
		h={"Authorization": token,  "Content-Type": "application/json"}
		url="https://developer.api.autodesk.com/da/us-east/v3/workitems/%s"%(workitem_id)
		t=requests.get(url,headers=h)
		if t.status_code==200:
			rt.windows.processPostedMessages()
			print t.json()["status"]
			# whille status is pending or not completed/cancelled etc
			time.sleep(10)
		
			s=t.json()["status"]
		else:
			print t
			print t.json()
	return t.status_code
	
	
	
#############################################################################################
#############################################################################################
##
## Download the resulting file
##
#############################################################################################
#############################################################################################
def download_file_from_forge(token, bucket_name, bucket_region,object_name,local_file_name):
	# grab the object from the cloud and save it locally
	h={"Authorization": token,"Content-Type": "application/json", "x-ads-region":  bucket_region}
	d={}
	t=requests.get("https://developer.api.autodesk.com/oss/v2/buckets/%s/details"%(bucket_name), headers=h)
	#print r
	#print r.json()

	if "bucketKey" in t.json() and t.json()["bucketKey"]==bucket_name:
		# if we get here we have access to the bucket

		t=requests.get("https://developer.api.autodesk.com/oss/v2/buckets/%s/objects/%s"%(bucket_name,object_name), headers=h)
		#print t
		if t.status_code==200:
			f=open(local_file_name,"wb")
			f.write(t.content)
			f.close()

	return t.status_code