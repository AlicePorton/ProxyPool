def get_file_content(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def write_file_content(filepath, content):
    with open(filepath, 'w+') as f:
        f.write(content)


def get_table_content(table):
    if table.find('thead') is None:
        trs = table.find_all('tr')
        first_tr = trs[0]
        others_tr = trs[1:]
        titles = [th.get_text() for th in first_tr.find_all('th')]
        results = []
        for one_other in others_tr:
            temp = [t.get_text().replace('\n', '') for t in one_other.find_all('td')]
            per = {titles[k]: temp[k] for k in range(0, len(titles) - 1)}
            results.append(per)
        return results




