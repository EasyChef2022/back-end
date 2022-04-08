import recipe.models


def search_by_ingredients(ingredients: [str], exclude: [int], offset: int, limit: int) -> str:
    sql = '''select * from (select *, lower(array_to_string(ingredients, ',', '*')) as r_string from recipe) as temp where '''
    for i in ingredients:
        sql += f'''r_string like '%%{i.lower()}%%' and '''
    if len(exclude) > 0:
        sql += f'''id not in {str(exclude).replace('[', '(').replace(']', ')')} and '''
    sql = sql[:-4] + f'order by id asc limit {limit} offset {offset};'
    # print(sql)
    return sql


def search_by_name(name: str) -> str:
    sql = f'''select * from recipe where lower(name) like '%%{name.lower()}%%' limit 10;'''
    return sql


def sort_result(result: [recipe.models.Recipe], sort_by: str) -> [recipe.models.Recipe]:
    if sort_by == 'rating':
        return sorted(result, key=lambda x: x.rating, reverse=True)
    elif sort_by == 'complexity':
        return sorted(result, key=lambda x: len(x.ingredients), reverse=True)
    elif sort_by == 'time':
        return sorted(result, key=lambda x: x.cook_time, reverse=True)
    else:
        return sorted(result, key=lambda x: x.title)
