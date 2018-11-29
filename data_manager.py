# SQL query file

import connection
from datetime import datetime
from psycopg2 import sql


@connection.connection_handler
def show_questions(cursor):
    query = """SELECT id, vote_number, title, submission_time FROM question;"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def show_questions_by_order(cursor, direction, order_type):
    if order_type == "time":
        if direction == "desc":
            cursor.execute('''
                            SELECT id, vote_number, title, submission_time FROM question
                            ORDER BY submission_time DESC;
                            ''')
            details = cursor.fetchall()
            return details
        elif direction == "asc" or direction == None:
            cursor.execute('''
                            SELECT id, vote_number, title, submission_time FROM question
                            ORDER BY submission_time;
                            ''')
            details = cursor.fetchall()
            return details

    elif order_type == "vote_numbers":
        if direction == "desc":
            cursor.execute('''
                            SELECT id, vote_number, title, submission_time FROM question
                            ORDER BY vote_number DESC;
                            ''')
            details = cursor.fetchall()
            return details
        elif direction == "asc":
            cursor.execute('''
                            SELECT id, vote_number, title, submission_time FROM question
                            ORDER BY vote_number DESC;
                            ''')
            details = cursor.fetchall()
            return details

@connection.connection_handler
def get_question_details(cursor, id):
    cursor.execute('''
                    SELECT vote_number, title, message, id FROM question
                    WHERE id = %(id)s;
                    ''',
                   {'id': id})
    details = cursor.fetchone()
    return details


@connection.connection_handler
def get_answer_details(cursor, id):
    cursor.execute('''
                    SELECT vote_number, message, id FROM answer
                    WHERE question_id = %(id)s;
                    ''',
                   {'id': id})
    details = cursor.fetchall()
    return details


@connection.connection_handler
def get_the_answer(cursor, id):
    cursor.execute('''
                    SELECT message, id, question_id FROM answer
                    WHERE id = %(id)s
                    ''',
                   {'id': id})
    details = cursor.fetchone()
    return details


@connection.connection_handler
def change_vote_number(cursor, vote, id):
    if vote == "Vote up":
        vote_num = 1
    if vote == "Vote down":
        vote_num = -1
    cursor.execute('''
                    UPDATE question
                    SET vote_number = vote_number + %(vote_num)s
                    WHERE id = %(id)s;
                    ''',
                   {'id': id, 'vote_num': vote_num})


@connection.connection_handler
def get_current_answer_details(cursor, id, new_message):
    cursor.execute('''
                    UPDATE answer
                    SET message = %(new_message)s
                    WHERE id = %(id)s;
                    ''',
                   {'id': id, 'new_message': new_message})


@connection.connection_handler
def add_new_question(cursor, usr_input):
    query = """ INSERT INTO question (submission_time, title, message, image, user_id)
                VALUES ( %(submission_time)s, %(title)s, %(message)s, %(image)s, %(user_id)s);"""
    cursor.execute(query,usr_input)


@connection.connection_handler
def edit_question(cursor, usr_input):
    query="""UPDATE question
             SET title = %(title)s,
                message=%(message)s,
                image=%(image)s
             WHERE id=%(id)s;"""
    cursor.execute(query, usr_input)


@connection.connection_handler
def delete_row(cursor, table_name, question_id):
    query=sql.SQL("""DELETE FROM {}
                     WHERE question_id= %(question_id)s;""").format(sql.Identifier(table_name))
    params= {"question_id" : int(question_id)}
    cursor.execute(query, params)


@connection.connection_handler
def delete_question(cursor, id):
    query = """DELETE FROM question
               WHERE id = %(id)s;"""
    params = {"id": int(id)}
    cursor.execute(query, params)


@connection.connection_handler
def add_answer(cursor, new_answer):
    query = ''' INSERT INTO answer(submission_time, question_id, message, user_id)
               VALUES (%(submission_time)s, %(question_id)s, %(message)s, %(user_id)s);'''
    cursor.execute(query, new_answer)


@connection.connection_handler
def search_question(cursor, search_parameter):
    cursor.execute('''
                    SELECT id, vote_number, title, submission_time 
                    FROM question
                    WHERE title iLIKE %(search_parameter)s;
                    ''',
                   {"search_parameter": '%'+search_parameter +'%'})
    search_result = cursor.fetchall()
    return search_result


@connection.connection_handler
def get_comments(cursor, question_id):
    cursor.execute('''
                   SELECT message,submission_time FROM comment
                   WHERE question_id = %(question_id)s;
                   ''',
                   {"question_id": question_id})
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def add_comment(cursor, usr_input):
    query = """INSERT INTO comment (question_id, message, submission_time, edited_count, user_id)
                VALUES (%(question_id)s, %(message)s, %(submission_time)s, %(edited_count)s, %(user_id)s);"""
    cursor.execute(query, usr_input)


@connection.connection_handler
def get_question_tags(cursor, question_id):
    cursor.execute('''
                    SELECT name
                    FROM tag
                    INNER JOIN question_tag ON tag.id = question_tag.tag_id
                    WHERE question_id = %(question_id)s;
                    ''',
                   {'question_id': question_id})
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def get_all_tags(cursor):
    cursor.execute('''
                    SELECT name
                    FROM tag;''')
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def create_new_tag(cursor, new_tag_name):
    cursor.execute('''
                    INSERT INTO tag (name)
                    VALUES (%(new_tag_name)s);
                    ''',
                   {'new_tag_name': new_tag_name})


@connection.connection_handler
def fetch_tag_id_by_tag_name(cursor, tag_name):
    cursor.execute('''
                    SELECT id
                    FROM tag
                    WHERE name = %(tag_name)s;
                    ''',
                   {"tag_name": tag_name})
    tag_id = cursor.fetchone()
    return tag_id


@connection.connection_handler
def add_tag_to_current_question(cursor, question_id, tag_id):
    cursor.execute('''
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES (%(question_id)s, %(tag_id)s);
                    ''',
                   {"question_id": question_id, "tag_id": tag_id})


@connection.connection_handler
def register_user(cursor, usr_input):
    query = sql.SQL(''' INSERT INTO {} (first_name, last_name, email, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s) ''').format(sql.Identifier("user"))
    cursor.execute(query, usr_input)


@connection.connection_handler
def get_user_data(cursor):
    cursor.execute('''
                   SELECT * FROM "user";
                   ''')
    details = cursor.fetchall()
    return details


@connection.connection_handler
def get_login_data_from_email(cursor, email):
    query='''SELECT * FROM "user"
             WHERE email=(%(email)s);
           '''
    params= {"email":email}
    cursor.execute(query, params)
    return cursor.fetchone()
