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

def export_domain_meta(domains):
    table = 'domain_metadata'
    arcpy.AddMessage('Saving some domain metadata to %s' % table)
    fields = 'Name, Description, Type'.split(',')
    arcpy.CreateTable_management(gdb, table)
    for f in fields:
        arcpy.AddField_management(table, f, "TEXT")
    cursor = arcpy.da.InsertCursor(table, fields)
    for d in domains:
        cursor.InsertRow(d.name, d.description, d.type)

if __name__ == "__main__":
    domains = arcpy.da.ListDomains(gdb)
    export_domains(domains)
    export_domain_meta(domains)