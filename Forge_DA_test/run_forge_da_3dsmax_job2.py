# python implementation equivalent of createanduploadapp.js

import os, requests,json,time,sys,zipfile
from pymxs import runtime as rt


sys.path.append("D:\\d\\forge_2018_da\\")
import functions_forge_da_3dsmax_job
reload(functions_forge_da_3dsmax_job)

# define the base name of the application we're creating, will be used for the app bundle and the activity by appending either "AppBunlde" or "Activity" to it.
local_folder="d:/d/forge_2018_da/"

app_id="NHExtractData" #"NHExportToFBX"
appbundle_id=app_id+"AppBundle"
activity_id=app_id+"Activity"
appbundlefolder=local_folder+"appBundle2/"
appbundlename=appbundlefolder+"export.bundle"
appbundlefile=appbundlename+".zip"

bucketname="nh20190301-142700testbucket3"
bucket_region="US"
bucket_type="persistent"

object_name="teapot.max"
local_file=local_folder+object_name

output_name="teapot.fbx"
output_file_name=local_folder+output_name


#############################################################################################
## Log in
#############################################################################################
print "Logging in"
scope="data:read data:write data:create data:search bucket:create bucket:read bucket:update bucket:delete viewables:read code:all"
status,token,client_id=functions_forge_da_3dsmax_job.login(scope)


#############################################################################################
#############################################################################################
## Appbundle section
#############################################################################################
#############################################################################################

#############################################################################################
## Zip up the appbundle
#############################################################################################
if token!="":
	functions_forge_da_3dsmax_job.zip_app_bundle(appbundlefile,appbundlefolder)

#############################################################################################
## Delete the app bundle if it already exists
#############################################################################################
if token!="":
	print "Delete the app bundle if it exists already"
	status=functions_forge_da_3dsmax_job.delete_appbundle(token,appbundle_id)


#############################################################################################
## Create the new app bundle
#############################################################################################
if status==200:
	print "Create the app bundle"
	status,uploadparameters=functions_forge_da_3dsmax_job.create_appbundle(token,appbundle_id)
	

#############################################################################################
## Upload the new app bundle
#############################################################################################
if status==200:
	print "Upload the app bundle"
	status=functions_forge_da_3dsmax_job.upload_appbundle(token,appbundlefile,uploadparameters)


#############################################################################################
## Create an alias for the app bundle 
#############################################################################################
if status==200:
	print "Create an alias for the app bundle"
	status=functions_forge_da_3dsmax_job.create_appbundle_alias(token,appbundle_id,"prod")


#############################################################################################
## Show all available app bundles 
#############################################################################################
if status==200:
	print "Show all available app bundles"
	status,appbundles=functions_forge_da_3dsmax_job.list_appbundle_alias(token,appbundle_id,"prod")
	functions_forge_da_3dsmax_job.pretty_print_list(appbundles,client_id)
	
	
#############################################################################################
#############################################################################################
## activity section
#############################################################################################
#############################################################################################
	
#############################################################################################
## Delete the activity if it already exists
#############################################################################################
if status==200:
	print "Delete the activity if it already exists"
	status=functions_forge_da_3dsmax_job.delete_activity(token,activity_id)


#############################################################################################
## Create the new activity
#############################################################################################
if status==200:
	print "Create the activity"
	status=functions_forge_da_3dsmax_job.create_activity(token,activity_id,appbundle_id,client_id)


#############################################################################################
## Create an alias for the new activity
#############################################################################################
if status==200:
	print "Create an alias for the activty"
	status=functions_forge_da_3dsmax_job.create_activity_alias(token,activity_id,"prod")


#############################################################################################
## List available activities
#############################################################################################
if status==200:
	print "List available activities"
	activities=functions_forge_da_3dsmax_job.list_activities(token)
	functions_forge_da_3dsmax_job.pretty_print_list(activities,client_id)
	

#############################################################################################
## Upload the scene file and if required first create the bucket
#############################################################################################
if status==200:
	print "Upload the scene file"

	status,bucket=functions_forge_da_3dsmax_job.get_bucket(token,bucketname,bucket_region)
	if status==200 and bucket=="":
		status=functions_forge_da_3dsmax_job.create_bucket(token,bucketname,bucket_region,bucket_type)
	
	if status==200:
		status=functions_forge_da_3dsmax_job.upload_file(token,bucketname,local_file,object_name)


#############################################################################################
## Getting the bucket details again
#############################################################################################
if status==200:
	print "Getting bucket details"
	status,bucket=functions_forge_da_3dsmax_job.get_bucket(token,bucketname,bucket_region)


#############################################################################################
## Getting the signed url of the uploaded file
#############################################################################################
if status==200:
	print "Generating the signed url of the scene file"
	status,input_url=functions_forge_da_3dsmax_job.get_signed_url(token,bucketname,object_name,bucket_region,"")



#############################################################################################
## Getting a signed url for the output file
#############################################################################################
if status==200:
	print "Generating the signed url for the output file"
	status,output_url=functions_forge_da_3dsmax_job.get_signed_url(token,bucketname,output_name,bucket_region,"?access=write")


#############################################################################################
#############################################################################################
## workitem section
#############################################################################################
#############################################################################################

#############################################################################################
## Submit the workitem
#############################################################################################
if status==200:
	print "Submitting the workitem"
	
	activity_id=activity_id+"+prod"
	status,workitem_id=functions_forge_da_3dsmax_job.submit_workitem(token,activity_id,client_id,input_url,output_url)


#############################################################################################
## Wait for the workitem to complete
#############################################################################################
if status==200:
	print "Waiting for the workitem to complete"
	status=functions_forge_da_3dsmax_job.wait_for_workitem(token,workitem_id)

if status==200:
	print "Workitem completed"


#############################################################################################
## Download the resulting file
#############################################################################################
if status==200:
	print "Downloading the resulting file"
	if os.path.exists(output_file_name)==True:
		os.unlink(output_file_name)
	status=functions_forge_da_3dsmax_job.download_file_from_forge(token, bucketname, bucket_region,output_name,output_file_name)


#############################################################################################
## End
#############################################################################################
print "Done!"