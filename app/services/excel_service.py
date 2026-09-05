from openpyxl import load_workbook


def read_excel_rows(file_path: str):
    workbook = load_workbook(
        filename=file_path,
        read_only=True,     #it loads the workbook just in readable form
        data_only=True,      #it loads the workbook with only the data and not the formulas
    )

    worksheet = workbook.active   # to get the active sheet of the workbook

    headers = [
        cell.value
        for cell in next(worksheet.iter_rows())
    ]

    for row in worksheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        yield row_data        #it will generate the row ony by one not in once

    workbook.close()