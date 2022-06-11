from openpyxl import Workbook
def excel_file_maker(data, loc):

    file = Workbook()
    file_sheet = file.active
    file_sheet.title = loc
    file_sheet.append(['품목명', '입고번호', '입고일', '유효기간',
                       '판매일', '수량', '단위',
                       '분류'])
    for i in data:
        for j in i['product_list']:
            if not j['sold_date']:
                j['sold_date'] = 'N/A'
            file_sheet.append([j['product_name'], j['serial'], j['in_date'],
                               j['date'], j['sold_date'], j['amount'],
                               i['unit'], j['location']])

    return file