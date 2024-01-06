#!/usr/bin/python3

# If we ever have a worksheet, and we want to extract all cells and print them to our terminal/save them to a file:

import openpyxl

# Open the Excel file
workbook = openpyxl.load_workbook(str(__import__("sys").argv[1]))

# Iterate over all sheets
for sheet in workbook.worksheets:
    # Iterate over all cells in the sheet
    for row in sheet.iter_rows(values_only=True):
        print(row)

