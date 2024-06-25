import sys
import mysql.connector

# MySQL接続情報
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password',
    'database': 'tree'
}

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # ディレクトリとファイルの登録
    directories_created = {}

    # ソート済みのファイルリストを STDIN から受け取る
    #    "/root/file1",
    #    "/root/file2",
    #    "/root/subdir/file3",
    #    "/root/subdir/subdir2/file4"
    for path in sys.stdin:
        path = path.strip()
        components = path.split('/')
        current_parent_id = None

        for i, component in enumerate(components[0:-1]):
            parent_id = current_parent_id
            current_path = '/'.join(components[0:i+1])

            if current_path not in directories_created:
                # ディレクトリをdirectoriesテーブルに挿入
                insert_directory = """
                INSERT INTO directories (name, parent_directory_id)
                VALUES (%s, %s)
                """
                cursor.execute(insert_directory, (component, parent_id))
                directories_created[current_path] = cursor.lastrowid

                current_parent_id = cursor.lastrowid
            else:
                current_parent_id = directories_created[current_path]

        # ファイルをfilesテーブルに挿入
        file_name = components[-1]
        directory_id = current_parent_id

        print("path: " + path + " file name: " + file_name + " parent_id: " + str(directory_id))

        insert_file = """
        INSERT INTO files (name, directory_id)
        VALUES (%s, %s)
        """
        cursor.execute(insert_file, (file_name, directory_id))

    # トランザクションのコミット
    connection.commit()
    print("DONE")

except mysql.connector.Error as error:
    print(f'MySQLエラー: {error}')
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
