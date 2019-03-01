import MaxPlus 
from pymxs import runtime as rt
import uuid

# extract data to file	
# note that this does NOT support prs animation

# get filename
filename=rt.maxFileName

if filename=="":
	print "please save file first!"
else:
	# for each object get
	# UUID
	# name
	# original_name
	# position
	# scale 
	# rotation


	for c in rt.geometry:
		if rt.getUserPropVal(c,"original_name")==None:
			rt.setUserPropVal(c,"original_name",c.Name)
		if rt.getUserPropVal(c,"uuid")==None:
			rt.setUserPropVal(c,"uuid",uuid.uuid4().hex)
		# then rename the object so it's uuid+name (checking the this hasn't been done already)

		original_name=rt.getUserPropVal(c,"original_name")
		uuid=rt.getUserPropVal(c,"uuid")
		name=c.Name
		posx=c.pos.x
		posy=c.pos.y
		posz=c.pos.z
		
		# needs to change to quaternions!
		rotx=c.rotation.x
		roty=c.rotation.y
		rotz=c.rotation.z
		rotw=c.rotation.w
		
		scalex=c.scale.x
		scaley=c.scale.y
		scalez=c.scale.z

		s="%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s"%(filename,uuid,original_name,name,posx,posy,posz,rotx,roty,rotz,rotw,scalex,scaley,scalez)

		f=open("d:/d/forge_2018_da/test_data.txt","a")
		f.write(s+"\n")
		f.close()
	
print "done"