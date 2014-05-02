$package_list = [
	'python-dev',
	'python-pip',
	'libxml2-dev', 
	'libxslt-dev', 
	'libz-dev',
	'python-pycurl',
	'mysql-server',
	'mysql-client',
	'libmysqlclient-dev'
]

package{$package_list:
	ensuer => present
}