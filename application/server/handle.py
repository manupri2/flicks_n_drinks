from flask import jsonify







def build_movie_query(json_dict):
    query = "SELECT title, year, rating, "


    return


def query_data(query, conn):
    query_data = conn.execute(query)
    result = [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]
    return jsonify({'data': result})

