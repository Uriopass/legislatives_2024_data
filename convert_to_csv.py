import os
import bs4
import csv


def parse_html(html_file):
    text = html_file.read()
    soup = bs4.BeautifulSoup(text, 'html.parser')
    table = soup.find('table')
    head = table.find('thead')
    data = []
    for row in head.find_all('tr'):
        line = []
        for cell in row.find_all('th'):
            line.append(cell.text.strip())
        data.append(line)

    for row in table.find_all('tr'):
        line = []
        for cell in row.find_all('td'):
            line.append(cell.text.strip().replace(' ', '').replace(",", "."))
        if len(line) > 0:
            data.append(line)
    return data


def write_csv(csv_file, data):
    writer = csv.writer(csv_file, lineterminator='\n')
    writer.writerows(data)


if __name__ == '__main__':
    for file in os.walk('results_html'):
        for f in file[2]:
            if not f.endswith('.html'):
                continue
            with open('results_html/' + f, 'r', encoding='UTF-8') as html_file:
                data = parse_html(html_file)
                with open('results_csv/' + f.replace('.html', '.csv'), 'w', encoding='UTF-8') as csv_file:
                    write_csv(csv_file, data)
