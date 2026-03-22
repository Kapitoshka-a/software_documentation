import argparse

from core.config import settings
from data_access import CsvFileDataSource, ImportRepository
from controllers import ImportController


def main() -> None:
    parser = argparse.ArgumentParser(description="Import CSV data into the database.")
    parser.add_argument("--csv", default=settings.CSV_PATH, help="Path to CSV file")
    args = parser.parse_args()

    for session in settings.get_sqlite_session():
        controller = ImportController(CsvFileDataSource(), ImportRepository(session))
        result = controller.import_from_csv(args.csv)
        print(result.model_dump())
        break


if __name__ == "__main__":
    settings.create_db_and_tables()
    main()
