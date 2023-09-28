import logging

from src.kal_worker import KalWorker
from os import remove
from src.mirror import Mirror
from src.cal_setup import get_calendar_service


def reset_credentials(name:str):
    """Just deletes 'token.pickle'"""
    try:
        remove(f'credentials_data/{name}_token.pickle')
    except FileNotFoundError:
        return




def run_service(user:Mirror):
    print(f"Running service for {user.title}...")

    
    # reset_credentials(user.title) # pops up the Oauth flow again instead of using the refresh token
    worker = KalWorker(source_ics_calendar_url=user.source_ics_calendar_url,
                              google_calendar_id=user.google_calendar_id,
                              rules=user.rules
                              )
    worker.run(get_calendar_service(user.title))




from mirrors.my_mirrors import my_mirror

if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG,
                        handlers=[logging.FileHandler("log.log"), logging.StreamHandler()])

    run_service(my_mirror)




