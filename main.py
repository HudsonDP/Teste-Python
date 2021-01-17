import requests as r
from bs4 import BeautifulSoup as BS4

URL = "https://gauchazh.clicrbs.com.br/esportes/tabelas/brasileirao"

def main():
    html = getHTML()
    table = getTable(html=html)
    print(table)


def getHTML():
    response = r.get(URL)
    if response.status_code != 200: 
        print("ERRO 200")
    return response.text

def getTable(html):
    soup = BS4(html, "html.parser")
    team_table = soup.find("div", {"class":"team-table"}).find("tbody")
    teams = team_table.find_all("td")
    return teams



if __name__ == "__main__":
    main()