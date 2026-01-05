import argparse
import datetime
import os

import openpyxl
from sqlalchemy import true
from tabulate import tabulate
import logging

def logForLevel(self, message, *args, **kwargs):
    if self.isEnabledFor(45):
        self._log(45, message, args, **kwargs)
def logToRoot(message, *args, **kwargs):
    logging.log(45, message, *args, **kwargs)

class Arguments:

    def __init__(self):
        ts = int((datetime.datetime.now()).timestamp())
        self.EXCEL_EXTENSION = "xlsx"
        self.DEFAULT_EXPORT = os.path.join(os.getcwd(), f"export-{ts}.{self.EXCEL_EXTENSION}")
        self.DEFAULT_RAW_EXPORT = os.path.join(os.getcwd(), f"export_raw-{ts}.{self.EXCEL_EXTENSION}")
        self.DEFAULT_DRY_RUN = os.path.join(os.getcwd(), f"errors-{ts}.{self.EXCEL_EXTENSION}")
        self.SUPPORTED_EXTENSIONS = ["csv", self.EXCEL_EXTENSION]
        self.TYPES_ESSAY = ["MBC", "MIC"]
        self.p = self.get_args()
        logging.addLevelName(45, 'SHOW')
        logging.basicConfig(format='%(asctime)s %(levelname)s :%(message)s',level=logging.DEBUG if self.p.verbose else 45)
        setattr(logging, "SHOW", 45)
        setattr(logging.getLoggerClass(), 'show', logForLevel)
        setattr(logging, 'show', logToRoot)
        self.log = logging.getLogger(__name__)

    def get_args(self):
        parser = argparse.ArgumentParser()
        generic  = parser.add_argument_group('Generic arguments')
        inp = parser.add_argument_group('Input data')
        raw = parser.add_argument_group('Raw data file manipulation')
        final = parser.add_argument_group('Final data file manipulation')
        generic.add_argument("-v", "--verbose", action='store_true', help="Verbose output")
        generic.add_argument("-n", "--no_question", action='store_true', help="Disable approval question")
        generic.add_argument("-d", "--dry_run", action='store_true', help="Dry run: If present -I validate Excel import data. Optional argument is file name with dry run results. If present -R provide info of raw data file (counts group counts by timestamps), use with -v")
        inp.add_argument("-i", "--import_file", nargs='*', type=str, help="Imported Excel file with data sources. If missing, raw file data can be used. The file must have expected content. To check the content use parameter --dry_run. ")
        raw.add_argument("-r", "--raw_data", nargs='*', type=str, help=f"Exported data raw file. Default value file name example: {self.DEFAULT_RAW_EXPORT}  Supported file extension: {', '.join(self.SUPPORTED_EXTENSIONS)}. If the file already exists, data will be add with new timestamp")
        raw.add_argument("-rl", "--raw_data_list", action='store_true', help="If present, the items with timestamp following -md -mj will be handled as list. If missing -md -mj accept only 2 value as boundaries form ... to. The rounding i.e  2025.12 could be used")
        raw.add_argument("-rd", "--raw_data_delete", type=str, help="From given raw file, delete records with timestamps from the list or in range (depend on -rl set")
        raw.add_argument("-rj", "--raw_data_join", type=str, help="From given raw file, join records with timestamps from the list or in range (depend on -rl set). Actual timestamp as is used for joined data")
        raw.add_argument("-rg", "--raw_data_get", type=str, help="Set specific scope for --export_excel from the list or in range (depend on -rl set).")
        final.add_argument("-e", "--export_excel", nargs='*', help=f"Exported final excel file. Default value example: {self.DEFAULT_EXPORT}")
        final.add_argument("-s", "--sheets", nargs='+', type=str, help="Source worksheets. If missing all worksheets will be used in given range --raw_data [--raw_data_get]")
        final.add_argument("-t", "--type_essay", nargs='+', help="MIC and / or MBC, sheets in export file ")
        return parser.parse_args()

    def check_args(self):
        if self.p.import_file:
            self.p.import_file = self.p.import_file[0]
            wbi = openpyxl.load_workbook(self.p.import_file)
            sheet_ok_manes = []
            self.p.sheets = self.p.sheets if self.p.sheets else wbi.sheetnames
            for sheet_name in self.p.sheets:
                try:
                    rs = wbi[str(sheet_name)].max_row
                    sheet_ok_manes.append(sheet_name)
                    self.log.info(f"Worksheet '{sheet_name}' has {rs} rows.")
                except KeyError:
                    self.log.info(f"Worksheet '{sheet_name}' not exists. It is excluded")
                self.p.sheets = sheet_ok_manes

        if self.p.raw_data is not None:
            s = self.p.raw_data[0] if self.p.raw_data else self.DEFAULT_RAW_EXPORT
            if not (s[s.rfind(".") + 1:] in self.SUPPORTED_EXTENSIONS):
                self.p.raw_data = s + "." + self.EXCEL_EXTENSION
                self.p.ext = self.EXCEL_EXTENSION
                self.log.info(f"Wrong extension for raw export file. File name was changed to {self.p.raw_data} ")
            else:
                self.p.ext = s[s.rfind(".") + 1:]
                self.p.raw_data = s

        if self.p.export_excel is not None:
            self.p.export_excel = self.p.export_excel[0] if self.p.export_excel else self.DEFAULT_EXPORT
            self.p.type_essay = self.p.type_essay if self.p.type_essay else [*self.TYPES_ESSAY]
            self.p.type_essay = [t.upper() for t in self.p.type_essay]
            if not (self.p.type_essay[0] in self.TYPES_ESSAY or sorted(self.p.type_essay) == self.TYPES_ESSAY):
                self.log.critical(f"{self.p.type_essay} is not in supported list {self.TYPES_ESSAY}")
                exit(1)

        self.log.info("List of variables:\n" + tabulate((dict(vars(self.p))).items(), headers=["Variable", "Value"], tablefmt="grid"))
        if (not self.p.no_question) and (not input("Do you like to proceed the task? [Y/n]") == "Y"):
            self.log.info("Script terminated by user.")
            exit(0)

    def save_file(self, save_function, file_path: str):
        try:
            save_function(file_path)
        except Exception as e:
            self.log.warning(f"Error saving file to '{file_path}': {e}")
            exit(1)

    def open_file(self, open_function, file_path: str):
        try:
            wbi = open_function(file_path)
        except FileNotFoundError as e:
            self.log.error(e)
            exit(1)
        except PermissionError as e:
            self.log.error(e)
            exit(1)
        return wbi