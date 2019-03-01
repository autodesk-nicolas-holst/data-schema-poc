import MaxPlus 
from pymxs import runtime as rt
import uuid

# apply previously extracted data to objects in a file
# any animation on the objects prs WILL BE LOST

# get filename
filename=rt.maxFileName

f=open("d:/d/forge_2018_da/test_data.txt","r")
d=f.read().split("\n")
f.close()
d.reverse()

maxdelta=0.00001

for c in rt.geometry:
	# find the uuid that matches this object, if it doesn't have a uuid property then its data has never been stored.
	
	uuid=rt.getUserPropVal(c,"uuid")
	if uuid==None:
		print c.Name,"has nom properties stored in the data file"
	else:
		f=0
		for ti in d:
			i=ti.split("|")
			if len(i)==14:
				if i[1]==uuid:
					f=1
					print i

					# then rename the object so it's uuid+name (checking the this hasn't been done already)

					
					if rt.getUserPropVal(c,"original_name")==i[2]:
						print "no change in original_name"
					else:
						rt.setUserPropVal(c,"original_name",i[2])

					if c.Name==i[3]:
						print "no change in name"
					else:
						c.Name=i[3]
						
					tx=float(i[4])	
					ty=float(i[5])
					tz=float(i[6])
					
					if (abs(c.pos.x-tx)<maxdelta)and(abs(c.pos.y-ty)<maxdelta)and(abs(c.pos.z-tz)<maxdelta):
						print "no change in pos"
					else:
						print ("changed pos from %f %f %f to %f %f %f") %(c.pos.x,c.pos.y,c.pos.z,tx,ty,tz)
						c.pos=rt.Point3(tx,ty,tz)

					# doesn't work as we need to use quaternions instead :(
					tx=float(i[7])	
					ty=float(i[8])
					tz=float(i[9])
					tw=float(i[10])

					

					if (abs(c.rotation.x-tx)<maxdelta)and(abs(c.rotation.y-ty)<maxdelta)and(abs(c.rotation.z-tz)<maxdelta)and(abs(c.rotation.w-tw)<maxdelta):
						print "no change in rotation"
					else:
						print ("changed rotation from %f %f %f %f to %f %f %f %f") %(c.rotation.w,c.rotation.x,c.rotation.y,c.rotation.z,tw,tx,ty,tz)
						c.rotation=rt.Quat(tx,ty,tz,tw)

					tx=float(i[11])	
					ty=float(i[12])
					tz=float(i[13])
					
					if (abs(c.scale.x-tx)<maxdelta)and(abs(c.scale.y-ty)<maxdelta)and(abs(c.scale.z-tz)<maxdelta):
						print "no change in scale"
					else:
						print ("changed scale from %f %f %f to %f %f %f") %(c.scale.x,c.scale.y,c.scale.z,tx,ty,tz)
						c.scale=rt.Point3(tx,ty,tz)


						
					break
	
print "done"