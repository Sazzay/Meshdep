# The idea here is to be able to call this in once and then for use in the
# http request handler to simplify the process of making calls between the
# requests from a client -> server -> node.
#
# Initialize with a reference to a database connection and a node server
# and then you may use the built in functions.
#
# addFolder adds a folder with path to the folders in the database as per
# the queryFolderAddition and returns success or fail.
# 
# delFolder removes a folder by sending a request to the node and if the
# deletion is actually successful on the node it is deleted
#

class Helper:
	__init__(self, db, ns):
		self.DATABASE = db
		self.NODE_SERVER = ns

	__repr__(self):
		pass

	def addFolder(userName, path):
		try:
			db.queryFolderAddition(userName, path)
			return "Successfully added the folder with path %s" % path
		except:
			return "Failed to add the folder with path %s" % path

	def delFolder(userName, path):
		mids = db.queryNodesWithFolder(userName, path)

		if len(nodes) == 0:
			return "The amount of nodes containing this folder is zero, something went wrong..."
		
		for i in range(len(mids)):
			node = ns.NHT.find_node_by_mid(mids[i])

			if node:
				node.send_del_folder_req(userName, path)

		mids = db.queryNodesWithFolder(userName, path)

		if len(mids) > 0
			return "Failed to remove folder from all nodes, this is most likely due to a node being disconnected."
		else:
			return "Successfully removed all folder."

	def addFile():
		pass
		#todo, potentially, slightly complicated

	def remFile(self, mid, userName, path, filename):
		pass
		


