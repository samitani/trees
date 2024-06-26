# DDL
```
CREATE TABLE `directories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `parent_directory_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_name_parent_directory_id` (`name`,`parent_directory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `directory_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_directory_id_name` (`directory_id`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=221243 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

# LOAD DATA
```
$ head file.list
/boot/config-5.14.0-362.13.1.el9_3.x86_64
/boot/initramfs-0-rescue-85910d4004fd41118b0848a7286b94ec.img
/boot/initramfs-5.14.0-362.13.1.el9_3.x86_64.img
/boot/System.map-5.14.0-362.13.1.el9_3.x86_64
/boot/vmlinuz-0-rescue-85910d4004fd41118b0848a7286b94ec
/boot/vmlinuz-5.14.0-362.13.1.el9_3.x86_64
/boot/.vmlinuz-5.14.0-362.13.1.el9_3.x86_64.hmac
/etc/adjtime
/etc/aliases

$ cat file.list | sort | python adjacency_list.py
```

# SQL Sample

## SELECT all files
```
WITH RECURSIVE DirectoryPaths AS (
    -- 初期条件: ルートディレクトリのパスを取得
    SELECT d.id AS directory_id,
           d.name AS directory_name,
           d.name AS directory_path
    FROM directories d
    WHERE d.parent_directory_id IS NULL
    
    UNION ALL
    
    -- 再帰ステップ: 子ディレクトリを取得してパスを結合
    SELECT d.id AS directory_id,
           d.name AS directory_name,
           CONCAT(dp.directory_path, '/', d.name) AS directory_path
    FROM directories d
    JOIN DirectoryPaths dp ON d.parent_directory_id = dp.directory_id
)
-- 最終的にファイルのパスリストを生成
SELECT CONCAT(dp.directory_path, '/', f.name) AS file_path
FROM DirectoryPaths dp
JOIN files f ON dp.directory_id = f.directory_id;
```

## SELECT parent directory paths of specific directory
```
mysql> WITH RECURSIVE DirectoryPaths AS (
    ->     SELECT d.id AS directory_id,
    ->            d.parent_directory_id AS parent_directory_id,
    ->            d.name AS directory_name,
    ->            d.name AS directory_path
    ->     FROM directories d
    ->     WHERE d.id = 7901
    ->     UNION ALL
    ->     SELECT d.id AS directory_id,
    ->            d.parent_directory_id AS parent_directory_id,
    ->            d.name AS directory_name,
    ->            CONCAT(d.name, '/', dp.directory_path) AS directory_path
    ->     FROM directories d
    ->     JOIN DirectoryPaths dp ON dp.parent_directory_id = d.id
    -> )
    -> SELECT * FROM DirectoryPaths;
+--------------+---------------------+----------------+---------------------------+
| directory_id | parent_directory_id | directory_name | directory_path            |
+--------------+---------------------+----------------+---------------------------+
|         7901 |                7899 | power          | power                     |
|         7899 |                7896 | kprobe         | kprobe/power              |
|         7896 |                7753 | devices        | devices/kprobe/power      |
|         7753 |                   1 | sys            | sys/devices/kprobe/power  |
|            1 |                NULL |                | /sys/devices/kprobe/power |
+--------------+---------------------+----------------+---------------------------+
5 rows in set (0.00 sec)
```

## SELECT child directory paths of specific directory
```
mysql> WITH RECURSIVE DirectoryPaths AS (
    ->     SELECT d.id AS directory_id,
    ->            d.parent_directory_id AS parent_directory_id,
    ->            d.name AS directory_name,
    ->            d.name AS directory_path
    ->     FROM directories d
    ->     WHERE d.id = 48
    ->     UNION ALL
    ->     SELECT d.id AS directory_id,
    ->            d.parent_directory_id AS parent_directory_id,
    ->            d.name AS directory_name,
    ->            CONCAT(dp.directory_path, '/', d.name) AS directory_path
    ->     FROM directories d
    ->     JOIN DirectoryPaths dp ON d.parent_directory_id = dp.directory_id
    -> )
    -> SELECT * FROM DirectoryPaths;
+--------------+---------------------+----------------+--------------------------------+
| directory_id | parent_directory_id | directory_name | directory_path                 |
+--------------+---------------------+----------------+--------------------------------+
|           48 |                   3 | pki            | pki                            |
|           49 |                  48 | ca-trust       | pki/ca-trust                   |
|           56 |                  48 | rpm-gpg        | pki/rpm-gpg                    |
|           57 |                  48 | tls            | pki/tls                        |
|           50 |                  49 | extracted      | pki/ca-trust/extracted         |
|           55 |                  49 | source         | pki/ca-trust/source            |
|           51 |                  50 | edk2           | pki/ca-trust/extracted/edk2    |
|           52 |                  50 | java           | pki/ca-trust/extracted/java    |
|           53 |                  50 | openssl        | pki/ca-trust/extracted/openssl |
|           54 |                  50 | pem            | pki/ca-trust/extracted/pem     |
+--------------+---------------------+----------------+--------------------------------+
10 rows in set (0.04 sec)
```

## SELECT all file names under specific directory
```
WITH RECURSIVE DirectoryPaths AS (
    SELECT d.id AS directory_id,
           d.parent_directory_id AS parent_directory_id,
           d.name AS directory_name,
           d.name AS directory_path
    FROM directories d
    WHERE d.id = 48
    UNION ALL
    SELECT d.id AS directory_id,
           d.parent_directory_id AS parent_directory_id,
           d.name AS directory_name,
           CONCAT(dp.directory_path, '/', d.name) AS directory_path
    FROM directories d
    JOIN DirectoryPaths dp ON d.parent_directory_id = dp.directory_id
)
SELECT CONCAT(dp.directory_path, '/', f.name) AS file_path, f.id AS file_id, dp.directory_id
FROM DirectoryPaths dp
JOIN files f ON dp.directory_id = f.directory_id;
+----------------------------------------------------+---------+--------------+
| file_path                                          | file_id | directory_id |
+----------------------------------------------------+---------+--------------+
| pki/ca-trust/ca-legacy.conf                        |     195 |           49 |
| pki/ca-trust/README                                |     207 |           49 |
| pki/rpm-gpg/RPM-GPG-KEY-EPEL-9                     |     209 |           56 |
| pki/rpm-gpg/RPM-GPG-KEY-Rocky-9                    |     210 |           56 |
| pki/rpm-gpg/RPM-GPG-KEY-Rocky-9-Testing            |     211 |           56 |
| pki/tls/ct_log_list.cnf                            |     212 |           57 |
| pki/tls/openssl.cnf                                |     213 |           57 |
| pki/ca-trust/extracted/README                      |     206 |           50 |
| pki/ca-trust/source/README                         |     208 |           55 |
| pki/ca-trust/extracted/edk2/cacerts.bin            |     196 |           51 |
| pki/ca-trust/extracted/edk2/README                 |     197 |           51 |
| pki/ca-trust/extracted/java/cacerts                |     198 |           52 |
| pki/ca-trust/extracted/java/README                 |     199 |           52 |
| pki/ca-trust/extracted/openssl/ca-bundle.trust.crt |     200 |           53 |
| pki/ca-trust/extracted/openssl/README              |     201 |           53 |
| pki/ca-trust/extracted/pem/email-ca-bundle.pem     |     202 |           54 |
| pki/ca-trust/extracted/pem/objsign-ca-bundle.pem   |     203 |           54 |
| pki/ca-trust/extracted/pem/README                  |     204 |           54 |
| pki/ca-trust/extracted/pem/tls-ca-bundle.pem       |     205 |           54 |
+----------------------------------------------------+---------+--------------+
19 rows in set (0.08 sec)
```

## SELECT file names in specific directory
```
mysql> SELECT * FROM files WHERE directory_id = '7901';
+--------+------------------------+--------------+
| id     | name                   | directory_id |
+--------+------------------------+--------------+
| 116876 | autosuspend_delay_ms   |         7901 |
| 116877 | control                |         7901 |
| 116878 | runtime_active_time    |         7901 |
| 116879 | runtime_status         |         7901 |
| 116880 | runtime_suspended_time |         7901 |
+--------+------------------------+--------------+
5 rows in set (0.00 sec)
```

## UPDATE directory name
```
UPDATE directories SET name = 'new_name' WHERE id = 7901;
```

## DELETE directory recursively
```
WITH RECURSIVE DirectoryPaths AS (
    SELECT d.id AS directory_id,
           d.parent_directory_id AS parent_directory_id,
           d.name AS directory_name,
           d.name AS directory_path
    FROM directories d
    WHERE d.id = 48
    UNION ALL
    SELECT d.id AS directory_id,
           d.parent_directory_id AS parent_directory_id,
           d.name AS directory_name,
           CONCAT(dp.directory_path, '/', d.name) AS directory_path
    FROM directories d
    JOIN DirectoryPaths dp ON d.parent_directory_id = dp.directory_id
)
DELETE f FROM DirectoryPaths dp JOIN files f ON dp.directory_id = f.directory_id;
```
