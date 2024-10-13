import pyodbc
from fpdf import FPDF

# region
class PDF(FPDF):
    def header(self):
        global line_position
        global title
        line_position = 0
        self.add_font('Arial', '', 'arial.ttf', uni = True)
        self.add_font('Arial', 'I', 'arial.ttf', uni = True)
        self.add_font('Arial', 'B', 'arial.ttf', uni = True)
        # Arial bold 15
        self.set_font('Arial', 'B', 24)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, title, 0, 0, 'C')
        self.set_font('Arial', '', 15)
        # Line break
        self.ln(20)

    # Горизонтальная линия в ширину страницы
    def wline(self, y):
        self.line(self.l_margin, y, self.w - self.r_margin, y)

    def create_table(self, title: str, headings: tuple, data: list, w_for_cols = [], font_size = 15, left_margin = 0):
        # Отделяем таблицу от остального содержимого
        self.ln()
        # Устанавливаем заголовок
        self.set_font('Arial', 'I', 15)
        self.cell(self.w - self.l_margin - self.r_margin, 10, title, align="C")
        self.set_font('Arial', '', font_size)
        # на следующей строке
        self.ln()
            
        col_w = (self.w - (self.l_margin + self.r_margin)) // len(headings)
        col_h = 10

        # Заголовки столбцов таблицы
        if  (len(w_for_cols) == 0):
            if(left_margin != 0):
                self.cell(left_margin, 10)
            for i in range (len(headings)):
                self.cell(col_w, col_h, headings[i], 1)
        else:
            if(left_margin != 0):
                self.cell(left_margin, 10)
            for i in range (len(headings)):
                self.cell(w_for_cols[i], col_h, headings[i], 1, fill=True)
        self.ln()

        if (len(w_for_cols) == 0):
            for i, row in enumerate(data):
                if(left_margin != 0):
                    self.cell(left_margin, 10)
                for j, cell in enumerate(row):
                    self.cell(col_w, col_h, data[i][j], 1)
                self.ln()
        else:
            for i, row in enumerate(data):
                if(left_margin != 0):
                    self.cell(left_margin, 10)
                for j, cell in enumerate(row):
                    self.cell(w_for_cols[j], col_h, data[i][j], 1)
                self.ln()
        self.ln()

    def create_empty_table(self, title: str, label:str, widthes: tuple, left_margin = 0):
        if left_margin != 0:
            self.cell(left_margin, 10)
        self.cell(widthes[0], 10, title)
        self.cell(widthes[1], 10, label)
        self.ln()

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Страница ' + str(self.page_no()), 0, 0, 'C')
# endregion

def create_report(laptop, serial_number):  
    global title
    title = f"Отчёт о ноутбуке №{serial_number}"
    report = PDF()
    report.set_fill_color(128, 128, 128)
    report.add_page()
    report.wline(20)

    for photo in laptop:
        # Добавление фото в отчёт
        # report.image(photo["src"], x=10, y=20, w=100)

        photo_name = photo["src"].split('/')[-1]
        report.cell(50, 10, photo_name)
        report.ln()

        l_margin = 10

        photo_defects = photo["deffects"]
        for i, defect in enumerate(photo_defects):
            report.cell(l_margin)
            report.cell(100, 10, f"{i + 1}. {defect}: {len(photo_defects[defect])}")
            report.ln()

    conclusion = "Контроль качества пройден." if len(photo) == 0 else "Контроль качества не пройден."
    report.wline(report.get_y())
    report.cell(30, 10, conclusion)

    report.output(f'Отчёт о ноутбуке №{serial_number}.pdf', 'F')

create_report(0, "1267328712")