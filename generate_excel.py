import xlsxwriter

workbook = xlsxwriter.Workbook('Project_Estimation_and_Cost_Comparison.xlsx')
worksheet = workbook.add_worksheet('Project Estimation')

# Formats
title_format = workbook.add_format({'bold': True, 'font_size': 16, 'font_color': '#1F497D', 'bottom': 2, 'bottom_color': '#1F497D'})
header_format = workbook.add_format({'bold': True, 'bg_color': '#4F81BD', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
bold_format = workbook.add_format({'bold': True})
currency_format = workbook.add_format({'num_format': '#,##0.00 €', 'border': 1, 'align': 'right'})
number_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'align': 'right'})
int_format = workbook.add_format({'num_format': '0', 'border': 1, 'align': 'right'})
border_format = workbook.add_format({'border': 1})
cell_format = workbook.add_format({'border': 1, 'align': 'left'})
sum_header_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#DCE6F1'})
sum_val_format = workbook.add_format({'bold': True, 'border': 1, 'num_format': '0', 'bg_color': '#DCE6F1', 'align': 'right'})
info_format = workbook.add_format({'italic': True, 'font_color': '#595959'})

worksheet.set_column('A:A', 35)
worksheet.set_column('B:D', 18)
worksheet.set_column('E:E', 45)

worksheet.write('A1', 'Software Project Estimation & Cost Comparison', title_format)
worksheet.write('A2', 'Based on Function Point Method, COCOMO Organic Mode, and Cost Analysis', info_format)

# Row 5 (index 4)
worksheet.write('A5', '1. Function Point Method (FPA)', bold_format)
headers_fp = ['Type', 'Factor', 'Number', 'FP']
for col_num, data in enumerate(headers_fp):
    worksheet.write(5, col_num, data, header_format) # Row 6

fp_data = [
    ['Inputs (EI)', 4, 1, 4],     # Row 7
    ['Outputs (EO)', 5, 7, 35],   # Row 8
    ['Queries (EQ)', 4, 0, 0],    # Row 9
    ['Internal files (ILF)', 10, 0, 0], # Row 10
    ['External files (EIF)', 7, 2, 14], # Row 11
]

row = 6
for item in fp_data:
    worksheet.write(row, 0, item[0], cell_format)
    worksheet.write_number(row, 1, item[1], int_format)
    worksheet.write_number(row, 2, item[2], int_format)
    worksheet.write_number(row, 3, item[3], int_format)
    row += 1

worksheet.write(11, 0, 'Sum', sum_header_format)  # Row 12
worksheet.write(11, 1, '', sum_header_format)
worksheet.write(11, 2, '', sum_header_format)
worksheet.write_formula('D12', '=SUM(D7:D11)', sum_val_format)

worksheet.write('A16', '2. LOC & COCOMO Estimation', bold_format) # Row 16

headers_cocomo = ['Parameter', 'Value', 'Unit', 'Formula / Description']
for col_num, data in enumerate(headers_cocomo):
    worksheet.write(16, col_num, data, header_format) # Row 17

cocomo_data = [
    ['LOC per FP (Power Automate)', 16, 'LOC', 'Given Estimation'], # Row 18
    ['Total FP', '=D12', 'FP', 'From FPA Table'], # Row 19
    ['Total LOC', '=B18*B19', 'LOC', 'LOC per FP * Total FP'], # Row 20
    ['Total KLOC', '=B20/1000', 'KLOC', 'Total LOC / 1000'], # Row 21
    ['Effort', '=2.4*(B21^1.05)', 'Person-Months', '2.4 * (KLOC)^1.05 (Organic Mode)'], # Row 22
    ['Time (Project Duration)', '=2.5*(B22^0.38)', 'Months', '2.5 * (Effort)^0.38'], # Row 23
    ['Implied Team Size', '=B22/B23', 'FTE', 'Effort / Time'], # Row 24
    ['Total Required Hours', '=B22*160', 'Hours', 'Effort * 160 hours/month'] # Row 25
]

row = 17
for item in cocomo_data:
    worksheet.write(row, 0, item[0], cell_format)
    
    if isinstance(item[1], str) and item[1].startswith('='):
        worksheet.write_formula(row, 1, item[1], number_format)
    else:
        worksheet.write_number(row, 1, item[1], number_format)
        
    worksheet.write(row, 2, item[2], cell_format)
    worksheet.write(row, 3, item[3], cell_format)
    row += 1

worksheet.write('A29', '3. Cost Comparison', bold_format) # Row 29
worksheet.write('B29', 'Working Students vs. Regular Developer', info_format)

headers_cost = ['Parameter', 'Working Students (Actual Team)', 'Regular Developer', 'Unit']
for col_num, data in enumerate(headers_cost):
    worksheet.write(29, col_num, data, header_format) # Row 30

cost_data = [
    ['Team Size', 3, 1, 'Persons'], # Row 31
    ['Hourly Rate / Equivalent', 23, '=400/8', '€/h'], # Row 32
    ['Total Required Hours', '=B25', '=B25', 'Hours'], # Row 33
    ['Project Duration', '=B23', '=C33/(160*C31)', 'Months'], # Row 34
    ['Avg. Hours / Week / Person', '=B33/(B34*4.33*B31)', '=C33/(C34*4.33*C31)', 'Hours/Week'], # Row 35
    ['Total Cost', '=B32*B33', '=C32*C33', '€'] # Row 36
]

row = 30
for item in cost_data:
    worksheet.write(row, 0, item[0], cell_format)
    
    # Col 1: Working Students
    if isinstance(item[1], str) and item[1].startswith('='):
        fmt = currency_format if item[3] == '€' or item[0] == 'Hourly Rate / Equivalent' else number_format
        if item[0] == 'Team Size': fmt = int_format
        worksheet.write_formula(row, 1, item[1], fmt)
    else:
        fmt = currency_format if item[3] == '€' or item[0] == 'Hourly Rate / Equivalent' else number_format
        if item[0] == 'Team Size': fmt = int_format
        worksheet.write_number(row, 1, item[1], fmt)

    # Col 2: Regular Dev
    if isinstance(item[2], str) and item[2].startswith('='):
        fmt = currency_format if item[3] == '€' or item[0] == 'Hourly Rate / Equivalent' else number_format
        if item[0] == 'Team Size': fmt = int_format
        worksheet.write_formula(row, 2, item[2], fmt)
    else:
        fmt = currency_format if item[3] == '€' or item[0] == 'Hourly Rate / Equivalent' else number_format
        if item[0] == 'Team Size': fmt = int_format
        worksheet.write_number(row, 2, item[2], fmt)

    # Col 3: Unit
    worksheet.write(row, 3, item[3], cell_format)
    row += 1

worksheet.write('A39', 'Note on Working Students:', bold_format)
worksheet.write('A40', 'The project was already successfully completed with a team of 3 working students.')
worksheet.write('A41', 'The calculated workload of approx. 7.7 hours per week per student fits perfectly within')
worksheet.write('A42', 'the maximum allowed 20 hours per week for working students, demonstrating the feasibility')
worksheet.write('A43', 'and efficiency of this setup.')

workbook.close()
