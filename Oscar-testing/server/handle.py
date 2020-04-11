from flask import jsonify


def build_movie_query(json_dict):
    query = "SELECT Movie.tconst, Movie.title, Movie.year, Movie.rating,\n" \
            " GROUP_CONCAT(DISTINCT Genre.genreName ORDER BY Genre.genreName DESC) AS genres,\n" \
            " GROUP_CONCAT(DISTINCT People.name ORDER BY People.name DESC) AS crew\n" \
            " FROM Movie\n" \
            " INNER JOIN MovieCategory ON Movie.tconst = MovieCategory.tconst\n" \
            " INNER JOIN Genre ON MovieCategory.genreId = Genre.genreId\n" \
            " INNER JOIN Crew ON Movie.tconst = Crew.tconst\n" \
            " INNER JOIN People ON Crew.nconst = People.nconst\n"

    year = json_dict['year']
    rating = json_dict['rating']
    title = json_dict['title']

    filter_q = ""
    filters = []
    if title:
        title = "%%" + title + "%%"
        filters.append("Movie.title LIKE '%s'" % title)
    if year:
        filters.append("Movie.year = " + year)
    if rating:
        filters.append("Movie.rating >= " + rating)

    if filters:
        filter_q += " WHERE " + filters[0]

        if len(filters) > 1:
            for f in filters[1:]:
                filter_q += " AND " + f

    query += filter_q
    query += "\n GROUP BY Movie.title\n" \
             " LIMIT 100\n"
    return query


def query_data(query, conn):
    query_data = conn.execute(query)
    result = [dict(zip(tuple(query_data.keys()), i)) for i in query_data.cursor]
    return jsonify({'data': result})

