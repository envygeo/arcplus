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

def export_domains(domains):
    for domain in domains:
        arcpy.AddMessage('Exporting %s CV to table in %s' % (domain.name, gdb))
        table = os.path.join(gdb, domain.name)
        arcpy.DomainToTable_management(gdb, domain.name, table,
            'field','description', '#')

if __name__ == "__main__":
    domains = arcpy.da.ListDomains(gdb)
    export_domains(domains)