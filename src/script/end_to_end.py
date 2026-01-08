import openpyxl
import pandas

from src.script.bin.excel_parser import ExcelParser


class Main(ExcelParser):
    def __init__(self):
        super().__init__()

    def main(self) -> None:
        wbi = None
        self.check_args()
        new_raw_data = pandas.DataFrame()

        if self.p.dry_run:
            if self.p.import_file:
                err_data = self.approve_data(wbi)
                err_data.to_excel("errors_" + self.p.import_file)
                self.log.info(f"Errors exported to file errors_{self.p.import_file}. Count of errors {len(err_data)}")
            exit(0)
# continue
        if self.p.import_file:
            wbi = self.open_file(openpyxl.load_workbook, self.p.import_file)
            new_raw_data = self.get_raw_data(wbi)
            self.log.info(f"From import data file {self.p.import_file} received {len(new_raw_data)}")



        if self.p.raw_data and self.p.export_excel:
            self.log.info(f"From raw data file {self.p.raw_data} exported to final data {self.p.export_excel}")



        if self.p.dry_run and self.p.raw_data:
            self.log.info(f"Raw data content overview.")

if __name__ == "__main__":
    m = Main()
    m.main()
