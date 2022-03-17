def search_by_ingredients(ingredients: [str], exclude: [str], offset: int, limit: int) -> str:
    sql = '''select * from (select *, lower(array_to_string(ingredients, ',', '*')) as r_string from recipe) as temp where '''
    for i in ingredients:
        sql += f'''r_string like '%%{i.lower()}%%' and '''
    for i in exclude:
        sql += f'''r_string not like '%%{i.lower()}%%' and '''
    sql = sql[:-4] + f'limit {limit} offset {offset};'
    return sql


def serach_by_name(name: str) -> str:
    sql = f'''select * from recipe where lower(name) like '%%{name.lower()}%%' limit 10;'''
    return sql
