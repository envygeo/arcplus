# -*- coding: utf-8 -*-
"""
Tool name: Import Excel Sheets To Tables
Source: ExcelSheetsToTables.py
Author: Esri, Matt Wilkie

Convert all sheets in a Microsoft Excel (xls or xlsx) file to geodatabase, dbf or INFO tables.

Adapted from Excel To Table (Conversion)
    http://resources.arcgis.com/en/help/main/10.2/index.html#//001200000055000000
"""
import os
import xlrd
import arcpy

import os
import xlrd
import arcpy

def importallsheets(in_excel, table_prefix, out_gdb):
    workbook = xlrd.open_workbook(in_excel)
    sheets = [sheet.name for sheet in workbook.sheets()]

    arcpy.AddMessage('{} sheets found: {}'.format(len(sheets), ','.join(sheets)))
    for sheet in sheets:
        out_table = os.path.join(
            out_gdb,
            arcpy.ValidateTableName(
                "{0}_{1}".format(table_prefix, sheet),
                out_gdb))

        arcpy.AddMessage('Converting {} to {}'.format(sheet, out_table))

        # Perform the conversion
        arcpy.ExcelToTable_conversion(in_excel, out_table, sheet)

if __name__ == "__main__":
    in_excel = arcpy.GetParameterAsText(0)
    table_prefix = arcpy.GetParameterAsText(1)
    out_gdb = arcpy.GetParameterAsText(2)
    importallsheets(in_excel, table_prefix, out_gdb)
