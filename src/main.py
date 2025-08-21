from views import main_info
from services import anylize_cashback

if __name__ == "__main__":
    #print(main_info("2018-05-20 15:30:00"))

    result_services = anylize_cashback(file_path="../data/operations.xlsx", year=2018, month=5)
    print(result_services)