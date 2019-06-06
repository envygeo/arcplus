# -*- coding: utf-8 -*-
"""
Tool name: Export GDB Domains to Tables
Source: export_gdb_domains.py
Author: Matt Wilkie (Environment Yukon)
License: X/MIT open source

Export all coded value domains in a geodatabase to tables in that gdb
    http://gis.stackexchange.com/questions/26215
"""
import os, sys
import arcpy

gdb = arcpy.GetParameterAsText(0)
xls = str.title(arcpy.GetParameterAsText(1))
    # True or False
arcpy.env.overwriteOutput = str.title(arcpy.GetParameterAsText(2))
    # True or False

if not os.path.exists(gdb):
    print('Usage:\n\n   python export_gdb_domains.py [input geodatabase] {write_xls} {overwrite}')
    print('   python export_gdb_domains.py [input geodatabase] true false')
    sys.exit()


def export_domains(domains):
    for domain in domains:
        arcpy.AddMessage('Exporting %s CV to table in %s' % (domain.name, gdb))
        table = os.path.join(gdb, domain.name)
        arcpy.DomainToTable_management(gdb, domain.name, table,
            'field','descript', '#')
        if xls:
            os.chdir(gdb)
            os.chdir('..')
            xlsfile = '%s_%s.xls' % (os.path.join(os.path.basename(gdb)),domain.name)
            arcpy.AddMessage('Exporting %s CV to table in %s' % (domain.name, xlsfile))
            arcpy.TableToExcel_conversion(table, xlsfile)


if __name__ == "__main__":
    domains = arcpy.da.ListDomains(gdb)
    export_domains(domains)
