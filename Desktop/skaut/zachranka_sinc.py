import io
from config import PASSWORD, USERNAME
import pandas as pd
import requests
from bs4 import BeautifulSoup

LOGIN_ACTION_URL = "https://cms.zachranka.app/cs/xadmin/dashboard/login"
DATA_URL = "https://cms.zachranka.app/cs/xadmin/xzachranka/message/index"

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

get_login = session.get(LOGIN_ACTION_URL, headers=headers)
soup = BeautifulSoup(get_login.text, "html.parser")
csrf_input = soup.find("input", {"name": "YII_CSRF_TOKEN"})

if csrf_input:
  csrf_token = csrf_input["value"]
  payload = {
      "YII_CSRF_TOKEN": csrf_token,
      "LoginForm[username]": USERNAME,
      "LoginForm[password]": PASSWORD,
      "yt0": "Přihlásit se",
  }
  session.post(LOGIN_ACTION_URL, data=payload, headers=headers)
  data_response = session.get(DATA_URL, headers=headers)

  if "login" not in data_response.url and data_response.status_code == 200:
    tables = pd.read_html(io.StringIO(data_response.text))
    if tables:
      df = tables[0]
      # Uložení přímo na tvou plochu
      df.to_csv(
          "/Users/tobiaspejsar/Desktop/zpravy_zachranka.csv",
          index=False,
          encoding="utf-8-sig",
      )
      print("Úspěšně staženo a uloženo na Plochu.")
    else:
      print("Tabulka nebyla nalezena.")
  else:
    print("Přihlášení se nezdařilo.")
else:
  print("CSRF token nebyl nalezen.")
