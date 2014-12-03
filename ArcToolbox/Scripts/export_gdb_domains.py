''' Export all coded value domains in a geodatabase to tables in that gdb
	http://gis.stackexchange.com/questions/26215
'''
import os, sys
import arcpy

gdb = sys.argv[0]

desc = arcpy.Describe(gdb)
domains = desc.domains

for domain in domains:
    print 'Exporting %s CV to table in %s' % (domain, gdb)
    table = os.path.join(gdb, domain)
    arcpy.DomainToTable_management(gdb, domain, table,
        'field','description', '#')
