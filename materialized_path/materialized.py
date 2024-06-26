import sys
import mysql.connector

# MySQL接続情報
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password',
    'database': 'materialized'
}

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # ディレクトリの登録
    directories_created = {}

    # ソート済みのファイルリストを STDIN から受け取る
    #    "/root/file1",
    #    "/root/file2",
    #    "/root/subdir/file3",
    #    "/root/subdir/subdir2/file4"
    for path in sys.stdin:
        path = path.strip()
        components = path.split('/')

        file_name = components[-1]
        if len(components) == 2:
            dir_path  = '/'
        else:
            dir_path  = '/'.join(components[0:-1])

        if dir_path not in directories_created:
            insert_file = """
            INSERT INTO files (path, filename, created)
            VALUES (%s, NULL, DATE_ADD('2024-01-01 00:00:00', INTERVAL floor(rand()*3600*24*365) SECOND))
            """
            cursor.execute(insert_file, (dir_path,))

            directories_created[dir_path] = cursor.lastrowid

        print("path: " + path + " file name: " + file_name)

        insert_file = """
        INSERT INTO files (path, filename, created)
        VALUES (%s, %s, DATE_ADD('2024-01-01 00:00:00', INTERVAL floor(rand()*3600*24*365) SECOND))
        """
        cursor.execute(insert_file, (dir_path, file_name))

    # トランザクションのコミット
    connection.commit()
    print("DONE")

except mysql.connector.Error as error:
    print(f'MySQLエラー: {error}')
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
