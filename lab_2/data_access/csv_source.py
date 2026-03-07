import csv
from typing import Mapping

from core.interfaces import CsvDataSourceInterface


class CsvFileDataSource(CsvDataSourceInterface):
    def read_rows(self, file_path: str) -> list[Mapping[str, str]]:
        with open(file_path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
