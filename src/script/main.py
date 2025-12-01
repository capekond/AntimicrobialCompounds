from src.script.excel_parser import ExcelParser


class Main(ExcelParser):
    def __init__(self):
        super().__init__()

    def main(self) -> None:
        self.get_args()
        wbi = self.check_args()
        if self.p.dry_run:
            # err_data = self.approve_data(wbi)
            # err_data.to_excel()
            # self.p.log(f"Errors exported to file {arg.p.dry_run_report}. Count of errors {len(err_data)}")
            exit(0)
        raw_data = self.get_raw_data(wbi)
        if self.p.ext == self.EXCEL_EXTENSION:
            raw_data.to_excel(self.p.export_raw)
        else:
            raw_data.to_csv(self.p.export_raw)
        self.log(f"Raw data exported to {self.p.export_raw}")
        self.log(f"Final data exported to file {self.p.export_excel}")
        pivot_data = self.get_final_content(raw_data)
        pivot_data.to_excel(self.p.export_excel)
        self.excel_final_formatting()


if __name__ == "__main__":
    m = Main()
    m.main()
