import pandas as pd

from views import main_info
from services import anylize_cashback
from reports import spending_by_category

if __name__ == "__main__":
    #print(main_info("2018-05-20 15:30:00"))

    result_services = anylize_cashback(file_path="../data/operations.xlsx", year=2018, month=5)
    print(result_services)

    df = pd.read_excel("..//data/operations.xlsx", sheet_name="Отчет по операциям")
    result_report = spending_by_category(df, "Ж/д билеты", "2018-05-20")