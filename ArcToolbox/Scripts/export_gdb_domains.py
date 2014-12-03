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

def get_domains(gdb):
    desc = arcpy.Describe(gdb)
    return desc.domains

def export_domains(domains):
    for domain in domains:
        arcpy.AddMessage('Exporting %s CV to table in %s' % (domain, gdb))
        table = os.path.join(gdb, domain)
        arcpy.DomainToTable_management(gdb, domain, table,
            'field','description', '#')

if __name__ == "__main__":
    domains = get_domains(gdb)
    export_domains(domains)