thislist = [1, 2, 3]
for index in range(len(thislist)):
	print(len(thislist))
	thislist[index]-=1
	if thislist[index]==1:
		thislist.remove(thislist[index])
       
print(thislist)
