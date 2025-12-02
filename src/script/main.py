import pandas

from src.script.excel_parser import ExcelParser


class Main(ExcelParser):
    def __init__(self):
        super().__init__()

    def main(self) -> None:
        raw_data = pandas.DataFrame()
        self.get_args()
        wbi = self.check_args()
        # dry run ------------------------------------------------
        if self.p.dry_run:
            err_data = self.approve_data(wbi)
            err_data.to_excel(self.p.dry_run_file)
            self.log(f"Errors exported to file {self.p.dry_run_file}. Count of errors {len(err_data)}")
        # raw data ------------------------------------------------
        if self.p.export_raw or self.p.export_raw_file or self.p.export_excel or self.p.export_excel_file:
            raw_data = self.get_raw_data(wbi)
        if self.p.export_excel:
            self.p.export_raw_file = self.p.export_raw_file if self.p.export_raw_file else self.DEFAULT_RAW_EXPORT
            if self.p.ext == self.EXCEL_EXTENSION:
                raw_data.to_excel(self.p.export_raw_file)
            else:
                raw_data.to_csv(self.p.export_raw_file)
            self.log(f"Raw data exported to {self.p.export_raw_file}")
        # final data ------------------------------------------------
        if self.p.export_excel or self.p.export_excel_file:
            self.p.export_excel_file = self.p.export_excel_file if self.p.export_excel_file else self.DEFAULT_EXPORT
            pivot_data = self.get_final_content(raw_data)
            pivot_data.to_excel(self.p.export_excel_file)
            self.excel_final_formatting()
            self.log(f"Final data exported to file {self.p.export_excel_file}")


if __name__ == "__main__":
    m = Main()
    m.main()
