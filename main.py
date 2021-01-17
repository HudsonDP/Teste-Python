import collections
import requests as r
from bs4 import BeautifulSoup as BS4
import xlsxwriter as xls

URL = "https://gauchazh.clicrbs.com.br/esportes/tabelas/brasileirao"

def main():
    html = getHTML()
    table = getTable(html=html)
    export_xls(table)

def getHTML():
    response = r.get(URL)
    if response.status_code != 200: 
        print("ERRO 200")
    return response.text

def getTable(html):
    soup = BS4(html, "html.parser")
    team_table = soup.find("div", {"class":"team-table"}).find("tbody")
    stats_table = soup.find("div", {"class":"stats-table"}).find("tbody")
    teams = team_table.find_all("td")
    stats = stats_table.find_all("tr")
    teams_list = []
    full_table = []

    for team in teams:
        team_name = team.find("span", {"class":"team_name"})
        teams_list.append(team_name.text)

    for i in range(len(stats)):
        stat_team = stats[i].find_all("td")
        posicao = i+1
        valores = {
            "Posição":posicao,
            "Nome do Time":teams_list[i],
            "Numero de Pontos":stat_team[0].text,
            "Numero de Jogos":stat_team[1].text,
            "Numero de Vitorias":stat_team[2].text,
            "Numero de Derrotas":stat_team[3].text,
            "Numero de Empates":stat_team[4].text,
            "Gols Pró":stat_team[5].text,
            "Gols Contra":stat_team[6].text,
            "Saldo de Gols":stat_team[7].text,
            "Aproveitamento":stat_team[8].text,
        }
        full_table.append(valores)

    return full_table

def export_xls(full_table):
    workbook = xls.Workbook('Tabela Brasileirao.xlsx')
    worksheet = workbook.add_worksheet()

    col = 0
    row = 0
    header = full_table[0].keys()

    for header_name in header:
        worksheet.write(row, col, header_name)
        col +=1

    for i in range(len(full_table)):
        col = 0
        row += 1
        values = full_table[i].values()
        for table_values in values:
            worksheet.write(row, col, table_values)
            col += 1

    workbook.close()

if __name__ == "__main__":
    main()