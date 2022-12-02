import sqlite3 as sq

definitions_files = open("defenitions.txt", "r", encoding="UTF8")
lines = definitions_files.readlines()
definition_length = len(lines)


#Изменение статистику
def update_data(user_id, is_correct, ticket):
    base = sq.connect('database.db')
    cursor = base.cursor()
    table_name = "user" + str(user_id)
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(table_name))
    if cursor.fetchone()[0] == 0:
        #Если пользователь зашел в первый раз, то создаем таблицу, которую заполняем нулями
        cursor.execute("CREATE TABLE {}(ticket TEXT UNIQUE, correct_points INT, total_points INT)".format(table_name))
        base.commit()
        i = 0
        for line in lines:
            definition, path, new_ticket = line.split(" & ")
            new_ticket = new_ticket.replace('\n', '')
            cursor.execute(
                "INSERT OR IGNORE INTO {}(ticket, correct_points, total_points) VALUES('{}', 0, 0);".format(table_name,
                                                                                                            new_ticket))

            base.commit()
    #Меняем статистику конкретного билета, в зависимости от отвтета
    cursor.execute("SELECT * FROM {} WHERE ticket = '{}'".format(table_name, ticket))
    records = cursor.fetchone()
    right_answers = int(records[1])
    total_answers = int(records[2]) + 1
    if is_correct:
        right_answers += 1
    data = (table_name, right_answers, total_answers, ticket)
    cursor.execute('''UPDATE {} SET
     correct_points = {}, total_points
      = {} WHERE ticket = "{}" '''.format(table_name, right_answers, total_answers, ticket))
    base.commit()
    base.close()


#Возвращаем полную статистку для конктретного пользователя
def get_statistics(user_id):
    base = sq.connect('database.db')
    cursor = base.cursor()
    table_name = "user" + str(user_id)
    output = ""
    cursor.execute("SELECT * FROM {}".format(table_name))
    records = cursor.fetchall()
    for line in records:
        ticket = line[0]
        right_answers = line[1]
        total_answers = line[2]
        try:
            percentage = right_answers / total_answers * 100
        except ZeroDivisionError:
            percentage = 100
        percentage = str(percentage) + '.'
        percentage = percentage[0: percentage.find('.')]
        output = output + "{}: {} % \n".format(ticket, percentage)
    base.close()
    return output
