# DDL
```
CREATE TABLE `directories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `parent_directory_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name_parent_directory_id` (`name`,`parent_directory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `directory_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_created` (`created`),
  UNIQUE KEY `idx_directory_id_name` (`directory_id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
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

## SELECT all files without ORDER BY
```
mysql> WITH RECURSIVE DirectoryPaths AS (
    ->     -- 初期条件: ルートディレクトリのパスを取得
    ->     SELECT d.id AS directory_id,
    ->            d.name AS directory_name,
    ->            d.name AS directory_path
    ->     FROM directories d
    ->     WHERE d.parent_directory_id IS NULL
    ->     UNION ALL
    ->     -- 再帰ステップ: 子ディレクトリを取得してパスを結合
    ->     SELECT d.id AS directory_id,
    ->            d.name AS directory_name,
    ->            CONCAT(dp.directory_path, '/', d.name) AS directory_path
    ->     FROM directories d
    ->     JOIN DirectoryPaths dp ON d.parent_directory_id = dp.directory_id
    -> )
    -> -- 最終的にファイルのパスリストを生成
    -> SELECT f.id, CONCAT(dp.directory_path, '/', f.name) AS file_path, f.created
    -> FROM DirectoryPaths dp
    -> JOIN files f ON dp.directory_id = f.directory_id;
+--------+-------------------------------------------------------------------+---------------------+
| id     | file_path                                                         | created             |
+--------+-------------------------------------------------------------------+---------------------+
|      1 | /.autorelabel                                                     | 2024-01-28 07:37:10 |
|      8 | /boot/.vmlinuz-5.14.0-362.13.1.el9_3.x86_64.hmac                  | 2024-04-15 02:08:02 |
|      5 | /boot/System.map-5.14.0-362.13.1.el9_3.x86_64                     | 2024-04-08 00:29:18 |
|      2 | /boot/config-5.14.0-362.13.1.el9_3.x86_64                         | 2024-01-17 04:02:07 |
|      3 | /boot/initramfs-0-rescue-85910d4004fd41118b0848a7286b94ec.img     | 2024-12-29 21:19:08 |
|      4 | /boot/initramfs-5.14.0-362.13.1.el9_3.x86_64.img                  | 2024-11-06 22:29:20 |
|      6 | /boot/vmlinuz-0-rescue-85910d4004fd41118b0848a7286b94ec           | 2024-10-14 06:58:31 |
|      7 | /boot/vmlinuz-5.14.0-362.13.1.el9_3.x86_64                        | 2024-02-17 09:24:43 |
|    245 | /etc/.pwd.lock                                                    | 2024-03-17 03:17:57 |
|    382 | /etc/.updated                                                     | 2024-07-22 12:19:34 |
|     43 | /etc/DIR_COLORS                                                   | 2024-01-17 22:48:11 |
|     44 | /etc/DIR_COLORS.lightbgcolor                                      | 2024-07-15 10:44:03 |
|     69 | /etc/GREP_COLORS                                                  | 2024-03-25 01:44:49 |
<snip>
+--------+-------------------------------------------------------------------+---------------------+
221242 rows in set (2.37 sec)
```

## SELECT all files ORDER BY path
```
mysql> WITH RECURSIVE DirectoryPaths AS (
    ->     SELECT d.id AS directory_id,
    ->            d.name AS directory_name,
    ->            d.name AS directory_path
    ->     FROM directories d
    ->     WHERE d.parent_directory_id IS NULL
    ->     UNION ALL
    ->     SELECT d.id AS directory_id,
    ->            d.name AS directory_name,
    ->            CONCAT(dp.directory_path, '/', d.name) AS directory_path
    ->     FROM directories d
    ->     JOIN DirectoryPaths dp ON d.parent_directory_id = dp.directory_id
    -> )
    -> SELECT CONCAT(dp.directory_path, '/', f.name) AS file_path, created
    -> FROM DirectoryPaths dp
    -> JOIN files f ON dp.directory_id = f.directory_id ORDER BY file_path;
+-------------------------------------------------------------------------------------------+---------------------+
| file_path                                                                                 | created             |
+-------------------------------------------------------------------------------------------+---------------------+
| /.autorelabel                                                                             | 2024-01-28 07:37:10 |
| /boot/.vmlinuz-5.14.0-362.13.1.el9_3.x86_64.hmac                                          | 2024-04-15 02:08:02 |
| /boot/System.map-5.14.0-362.13.1.el9_3.x86_64                                             | 2024-04-08 00:29:18 |
| /boot/config-5.14.0-362.13.1.el9_3.x86_64                                                 | 2024-01-17 04:02:07 |
| /boot/initramfs-0-rescue-85910d4004fd41118b0848a7286b94ec.img                             | 2024-12-29 21:19:08 |
| /boot/initramfs-5.14.0-362.13.1.el9_3.x86_64.img                                          | 2024-11-06 22:29:20 |
| /boot/vmlinuz-0-rescue-85910d4004fd41118b0848a7286b94ec                                   | 2024-10-14 06:58:31 |
| /boot/vmlinuz-5.14.0-362.13.1.el9_3.x86_64                                                | 2024-02-17 09:24:43 |
| /etc/.pwd.lock                                                                            | 2024-03-17 03:17:57 |
| /etc/.updated                                                                             | 2024-07-22 12:19:34 |
| /etc/DIR_COLORS                                                                           | 2024-01-17 22:48:11 |
| /etc/DIR_COLORS.lightbgcolor                                                              | 2024-07-15 10:44:03 |
| /etc/GREP_COLORS                                                                          | 2024-03-25 01:44:49 |
| /etc/NetworkManager/NetworkManager.conf                                                   | 2024-06-27 17:29:31 |
```

## SELECT TOP recent created files
```
mysql> WITH RECURSIVE DirectoryPaths AS (
    ->     SELECT d.id AS directory_id,
    ->            d.parent_directory_id AS parent_directory_id,
    ->            d.name AS directory_name,
    ->            d.name AS directory_path,
    ->            f.created AS created,
    ->            f.name AS filename
    ->     FROM directories d, (SELECT name, created, directory_id FROM files ORDER BY created DESC LIMIT 1000) f
    ->     WHERE d.id = f.directory_id
    ->     UNION ALL
    ->     SELECT d.id AS directory_id,
    ->            d.parent_directory_id AS parent_directory_id,
    ->            d.name AS directory_name,
    ->            CONCAT(d.name, '/', dp.directory_path) AS directory_path,
    ->            dp.created AS created,
    ->            dp.filename AS filename
    ->     FROM directories d
    ->     JOIN DirectoryPaths dp ON dp.parent_directory_id = d.id
    -> )
    -> SELECT * FROM DirectoryPaths WHERE directory_path LIKE '/%';
+--------------+---------------------+----------------+------------------------------------+---------------------+---------------------------------------------------------------------+
| directory_id | parent_directory_id | directory_name | directory_path                     | created             | filename                                                            |
+--------------+---------------------+----------------+------------------------------------+---------------------+---------------------------------------------------------------------+
|            1 |                NULL |                | /boot                              | 2024-12-29 21:19:08 | initramfs-0-rescue-85910d4004fd41118b0848a7286b94ec.img             |
|            1 |                NULL |                | /proc/248                          | 2024-12-30 23:54:29 | sessionid                                                           |
|            1 |                NULL |                | /proc/45                           | 2024-12-30 22:50:47 | cmdline                                                             |
|            1 |                NULL |                | /proc/2                            | 2024-12-30 22:16:52 | sessionid                                                           |
|            1 |                NULL |                | /proc/6                            | 2024-12-30 20:37:46 | timers                                                              |
|            1 |                NULL |                | /proc/1056                         | 2024-12-30 19:01:52 | wchan                                                               |
|            1 |                NULL |                | /proc/32                           | 2024-12-30 18:40:05 | stat                                                                |
|            1 |                NULL |                | /proc/14                           | 2024-12-30 18:32:57 | personality                                                         |
|            1 |                NULL |                | /proc/582                          | 2024-12-30 18:11:03 | oom_adj                                                             |
|            1 |                NULL |                | /proc/16                           | 2024-12-30 17:50:48 | status                                                              |
|            1 |                NULL |                | /proc/36                           | 2024-12-30 16:39:41 | setgroups                                                           |
|            1 |                NULL |                | /proc/478                          | 2024-12-30 16:38:36 | statm                                                               |
|            1 |                NULL |                | /proc/76                           | 2024-12-30 14:56:55 | schedstat                                                           |
|            1 |                NULL |                | /proc/721                          | 2024-12-30 14:42:20 | ksm_merging_pages                                                   |
|            1 |                NULL |                | /proc/582                          | 2024-12-30 13:41:27 | coredump_filter                                                     |
|            1 |                NULL |                | /proc/74                           | 2024-12-30 12:27:31 | timerslack_ns                                                       |
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
