import facebook

user_long_token = "EAAHKwRuZAVNkBALXOlhx05bZCBhZCTfgWRmUodJlh9vY2ZB41n4S9lSEBf3JjIE9q1O59AFAvZCU9aiGTy30QFBZAxjQkJjgBTVT1QRTZCRX6ZBn5edonAD6FQCigcD4yb0vn02YIdYZB21SSVeia702qNaS2Wc1G08dqhMJHgRiqKgcCWgiyuh98"

graph = facebook.GraphAPI(access_token=user_long_token, version="3.0")
pages_data = graph.get_object("/me/accounts")

permanent_page_token = pages_data["data"][0]["access_token"]
page_id = pages_data["data"][0]["id"]

"""
print(pages_data)
{'data': [{'access_token': 'EAAPxxx',
   'category': 'Education',
   'category_list': [{'id': '2250', 'name': 'Education'}],
   'name': 'Coding with Dr Harris',
   'id': '103361561317782',
   'tasks': ['ANALYZE', 'ADVERTISE', 'MODERATE', 'CREATE_CONTENT', 'MANAGE']}],
 'paging': {'cursors': {'before': 'MTAzMzYxNTYxMzE3Nzgy',
   'after': 'MTAzMzYxNTYxMzE3Nzgy'}}}
   """