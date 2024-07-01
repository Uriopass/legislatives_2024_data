import csv
import os
from xml.dom import minidom


def parseResults():
    results = {}
    for file in os.walk('results_csv'):
        for f in file[2]:
            if not f.endswith('.csv'):
                continue
            name = f.replace('.csv', '')

            data = []
            with open('results_csv/' + f, 'r', encoding='UTF-8') as csv_file:
                reader = csv.reader(csv_file, lineterminator='\n')
                reader.__next__()  # Skip the header
                for row in reader:
                    data.append(row)

            dpt, circo = name.split('_')
            name_like_in_the_svg = dpt.lower().zfill(3) + '-' + circo.zfill(2)

            if dpt == 'ZZ':
                name_like_in_the_svg = '999-' + circo.zfill(2)
            if dpt == 'ZX':
                name_like_in_the_svg = '977-01'

            results[name_like_in_the_svg] = data

    return results


def parseSVG():
    with open('circonscriptions.svg', 'r', encoding='UTF-8') as svg_file:
        return minidom.parse(svg_file)


if __name__ == '__main__':
    results = parseResults()

    svg = parseSVG()
    paths = svg.getElementsByTagName('path')
    for path in paths:
        id = path.getAttribute('id')
        data = results.get(id)
        if data is None:
            continue

        count_elus = 0
        for row in data:
            if row[5] == 'QUALIF T2':
                count_elus += 1
        if count_elus >= 3:
            path.setAttribute('style', 'fill: #FF0000;')

    with open('triangulaires.svg', 'w', encoding='UTF-8') as svg_file:
        xml = str(svg.toxml())
        xml = xml.replace('{{TITRE}}', 'Triangulaires')
        svg_file.write(xml)
