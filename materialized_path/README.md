# DDL
```
CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `path` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_created` (`created`),
  KEY `idx_path` (`path`(768))
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

$ cat file.list | sort | python materialized.py
```

# SQL Sample

## SELECT all files without ORDER BY
```
mysql> SELECT id, path, filename, created FROM files WHERE filename IS NOT NULL;
+--------+------------------------+-----------------------------------------------------------------------------------+---------------------+
| id     | path                   | filename                                                                          | created             |
+--------+------------------------+-----------------------------------------------------------------------------------+---------------------+
|      2 | /                      | .autorelabel                                                                      | 2024-05-05 21:32:49 |
|      4 | /boot                  | config-5.14.0-362.13.1.el9_3.x86_64                                               | 2024-10-22 12:07:10 |
|      5 | /boot                  | initramfs-0-rescue-85910d4004fd41118b0848a7286b94ec.img                           | 2024-05-04 14:32:30 |
|      6 | /boot                  | initramfs-5.14.0-362.13.1.el9_3.x86_64.img                                        | 2024-04-11 12:21:03 |
|      7 | /boot                  | System.map-5.14.0-362.13.1.el9_3.x86_64                                           | 2024-05-13 18:07:46 |
|      8 | /boot                  | vmlinuz-0-rescue-85910d4004fd41118b0848a7286b94ec                                 | 2024-12-30 05:35:43 |
<snip>
+--------+------------------------+-----------------------------------------------------------------------------------+---------------------+
221242 rows in set (0.55 sec)
```

## SELECT all files ORDER BY path
```
mysql> SELECT id, path, filename, created FROM files WHERE filename IS NOT NULL ORDER BY path, filename;
+--------+----------+-------------------------------------------------------------------------------------------------+---------------------+
| id     | path     | filename                                                                                        | created             |
+--------+----------+-------------------------------------------------------------------------------------------------+---------------------+
|      2 | /        | .autorelabel                                                                                    | 2024-05-05 21:32:49 |
|     10 | /boot    | .vmlinuz-5.14.0-362.13.1.el9_3.x86_64.hmac                                                      | 2024-06-15 19:09:26 |
|      7 | /boot    | System.map-5.14.0-362.13.1.el9_3.x86_64                                                         | 2024-05-13 18:07:46 |
|      4 | /boot    | config-5.14.0-362.13.1.el9_3.x86_64                                                             | 2024-10-22 12:07:10 |
|      5 | /boot    | initramfs-0-rescue-85910d4004fd41118b0848a7286b94ec.img                                         | 2024-05-04 14:32:30 |
|      6 | /boot    | initramfs-5.14.0-362.13.1.el9_3.x86_64.img                                                      | 2024-04-11 12:21:03 |
|      8 | /boot    | vmlinuz-0-rescue-85910d4004fd41118b0848a7286b94ec                                               | 2024-12-30 05:35:43 |
|      9 | /boot    | vmlinuz-5.14.0-362.13.1.el9_3.x86_64                                                            | 2024-11-20 21:35:19 |
|    298 | /etc     | .pwd.lock                                                                                       | 2024-05-27 15:25:37 |
|    461 | /etc     | .updated                                                                                        | 2024-12-18 03:42:22 |
|     58 | /etc     | DIR_COLORS                                                                                      | 2024-06-20 08:36:08 |
|     59 | /etc     | DIR_COLORS.lightbgcolor                                                                         | 2024-08-19 22:31:52 |
|     89 | /etc     | GREP_COLORS                                                                                     | 2024-07-30 04:40:29 |
|     12 | /etc     | adjtime                                                                                         | 2024-09-13 01:38:06 |
|     13 | /etc     | aliases                                                                                         | 2024-08-30 11:06:41 |
|     14 | /etc     | anacrontab                                                                                      | 2024-03-20 02:39:09 |
<snip>
+--------+----------+-------------------------------------------------------------------------------------------------+---------------------+
221242 rows in set (4.38 sec)
```

## SELECT TOP recent created files
```
mysql> SELECT id, path, filename, created FROM files ORDER BY created DESC LIMIT 1000;
+--------+-------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------+---------------------+
| id     | path                                                                                                              | filename                                                           | created             |
+--------+-------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------+---------------------+
| 167083 | /usr/local/mysql/lib/plugin                                                                                       | component_test_status_var_service_reg_only.so                      | 2024-12-30 23:58:42 |
| 108639 | /proc/584/task/584/net                                                                                            | dev_mcast                                                          | 2024-12-30 23:54:29 |
| 102879 | /proc/477/task/477                                                                                                | gid_map                                                            | 2024-12-30 23:54:29 |
| 137291 | /sys/kernel/slab/pid                                                                                              | sanity_checks                                                      | 2024-12-30 23:52:59 |
|  64303 | /home/vagrant/src/mysql-8.4.0/mysql-test/t                                                                        | mysql_comments.test                                                | 2024-12-30 23:50:57 |
| 151594 | /usr/lib64/python3.9/encodings/__pycache__                                                                        | charmap.cpython-39.pyc                                             | 2024-12-30 23:50:33 |
|  23524 | /home/vagrant/src/mysql-8.4.0/bld/unittest/gunit/group_replication/CMakeFiles/group_replication_member_info-t.dir | flags.make                                                         | 2024-12-30 23:49:15 |
| 214657 | /usr/share/vim/vim82/keymap                                                                                       | russian-jcukenwin.vim                                              | 2024-12-30 23:48:07 |
| 129891 | /sys/devices/virtual/tty/tty44/power                                                                              | runtime_active_time                                                | 2024-12-30 23:47:08 |
| 164955 | /usr/lib/python3.9/site-packages/sepolgen/__pycache__                                                             | defaults.cpython-39.opt-1.pyc                                      | 2024-12-30 23:41:22 |
| 126336 | /sys/devices/platform/i8042/serio1/input/input4/capabilities                                                      | ff                                                                 | 2024-12-30 23:36:46 |
| 127196 | /sys/devices/system/cpu/cpu3/cache/index2                                                                         | uevent                                                             | 2024-12-30 23:33:53 |
|  99601 | /proc/4060/task/4060/net/stat                                                                                     | nf_conntrack                                                       | 2024-12-30 23:31:03 |
<snip>
+--------+-------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------+---------------------+
1000 rows in set (0.56 sec)
```

## SELECT parent directory paths of specific directory
```
mysql> SELECT id, path, filename, created FROM files WHERE path = '/sys/devices/kprobe/power' AND filename IS NULL;
+--------+---------------------------+----------+---------------------+
| id     | path                      | filename | created             |
+--------+---------------------------+----------+---------------------+
| 124031 | /sys/devices/kprobe/power | NULL     | 2024-05-03 09:46:37 |
+--------+---------------------------+----------+---------------------+
1 row in set (0.00 sec)

mysql> EXPLAIN SELECT id, path, filename, created FROM files WHERE path = '/sys/devices/kprobe/power' AND filename IS NULL;
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key      | key_len | ref   | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------------+
|  1 | SIMPLE      | files | NULL       | ref  | idx_path      | idx_path | 3074    | const |    6 |    10.00 | Using where |
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------------+
1 row in set, 1 warning (0.01 sec)
```

## SELECT child directory paths of specific directory
```
mysql> SELECT id, path, filename, created FROM files WHERE path LIKE '/etc/pki/%' AND filename IS NULL;
+-----+-------------------------------------+----------+---------------------+
| id  | path                                | filename | created             |
+-----+-------------------------------------+----------+---------------------+
| 238 | /etc/pki/ca-trust                   | NULL     | 2024-08-01 20:07:01 |
| 254 | /etc/pki/ca-trust/extracted         | NULL     | 2024-08-23 19:58:12 |
| 240 | /etc/pki/ca-trust/extracted/edk2    | NULL     | 2024-11-03 17:58:21 |
| 243 | /etc/pki/ca-trust/extracted/java    | NULL     | 2024-07-26 20:44:04 |
| 246 | /etc/pki/ca-trust/extracted/openssl | NULL     | 2024-10-16 21:30:40 |
| 249 | /etc/pki/ca-trust/extracted/pem     | NULL     | 2024-02-29 09:05:14 |
| 257 | /etc/pki/ca-trust/source            | NULL     | 2024-01-28 15:24:36 |
| 259 | /etc/pki/rpm-gpg                    | NULL     | 2024-06-27 07:56:51 |
| 263 | /etc/pki/tls                        | NULL     | 2024-01-11 18:26:35 |
+-----+-------------------------------------+----------+---------------------+
9 rows in set (0.00 sec)

mysql> EXPLAIN SELECT id, path, filename, created FROM files WHERE path LIKE '/etc/pki/%' AND filename IS NULL;
+----+-------------+-------+------------+-------+---------------+----------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type  | possible_keys | key      | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+-------+---------------+----------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | files | NULL       | range | idx_path      | idx_path | 3074    | NULL |   28 |    10.00 | Using where |
+----+-------------+-------+------------+-------+---------------+----------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)
```

## SELECT all file names under specific directory
```
mysql> SELECT id, path, filename, created FROM files WHERE path LIKE '/etc/pki/%' AND filename IS NOT NULL;
+-----+-------------------------------------+-----------------------------+---------------------+
| id  | path                                | filename                    | created             |
+-----+-------------------------------------+-----------------------------+---------------------+
| 239 | /etc/pki/ca-trust                   | ca-legacy.conf              | 2024-09-19 20:27:52 |
| 256 | /etc/pki/ca-trust                   | README                      | 2024-02-22 23:40:18 |
| 255 | /etc/pki/ca-trust/extracted         | README                      | 2024-03-20 02:18:58 |
| 241 | /etc/pki/ca-trust/extracted/edk2    | cacerts.bin                 | 2024-01-21 04:28:08 |
| 242 | /etc/pki/ca-trust/extracted/edk2    | README                      | 2024-09-29 16:25:41 |
| 244 | /etc/pki/ca-trust/extracted/java    | cacerts                     | 2024-08-09 06:23:15 |
| 245 | /etc/pki/ca-trust/extracted/java    | README                      | 2024-04-27 17:44:05 |
| 247 | /etc/pki/ca-trust/extracted/openssl | ca-bundle.trust.crt         | 2024-01-02 06:21:09 |
| 248 | /etc/pki/ca-trust/extracted/openssl | README                      | 2024-08-19 15:13:44 |
| 250 | /etc/pki/ca-trust/extracted/pem     | email-ca-bundle.pem         | 2024-11-27 23:45:00 |
| 251 | /etc/pki/ca-trust/extracted/pem     | objsign-ca-bundle.pem       | 2024-01-22 19:29:21 |
| 252 | /etc/pki/ca-trust/extracted/pem     | README                      | 2024-07-27 02:11:44 |
| 253 | /etc/pki/ca-trust/extracted/pem     | tls-ca-bundle.pem           | 2024-09-02 00:30:41 |
| 258 | /etc/pki/ca-trust/source            | README                      | 2024-12-10 06:02:07 |
| 260 | /etc/pki/rpm-gpg                    | RPM-GPG-KEY-EPEL-9          | 2024-08-11 21:37:52 |
| 261 | /etc/pki/rpm-gpg                    | RPM-GPG-KEY-Rocky-9         | 2024-08-07 12:18:50 |
| 262 | /etc/pki/rpm-gpg                    | RPM-GPG-KEY-Rocky-9-Testing | 2024-03-01 20:40:37 |
| 264 | /etc/pki/tls                        | ct_log_list.cnf             | 2024-08-24 06:11:07 |
| 265 | /etc/pki/tls                        | openssl.cnf                 | 2024-02-23 23:35:52 |
+-----+-------------------------------------+-----------------------------+---------------------+
19 rows in set (0.00 sec)

mysql> EXPLAIN SELECT id, path, filename, created FROM files WHERE path LIKE '/etc/pki/%' AND filename IS NOT NULL;
+----+-------------+-------+------------+-------+---------------+----------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type  | possible_keys | key      | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+-------+---------------+----------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | files | NULL       | range | idx_path      | idx_path | 3074    | NULL |   28 |    90.00 | Using where |
+----+-------------+-------+------------+-------+---------------+----------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)
```

## SELECT file names in specific directory
```
mysql> SELECT id, path, filename, created FROM files WHERE path = '/sys/devices/virtual/tty/tty38/power';
+--------+--------------------------------------+------------------------+---------------------+
| id     | path                                 | filename               | created             |
+--------+--------------------------------------+------------------------+---------------------+
| 129825 | /sys/devices/virtual/tty/tty38/power | NULL                   | 2024-08-15 07:36:43 |
| 129826 | /sys/devices/virtual/tty/tty38/power | autosuspend_delay_ms   | 2024-05-20 16:08:40 |
| 129827 | /sys/devices/virtual/tty/tty38/power | control                | 2024-01-22 09:53:15 |
| 129828 | /sys/devices/virtual/tty/tty38/power | runtime_active_time    | 2024-02-20 01:00:13 |
| 129829 | /sys/devices/virtual/tty/tty38/power | runtime_status         | 2024-07-04 23:21:22 |
| 129830 | /sys/devices/virtual/tty/tty38/power | runtime_suspended_time | 2024-02-19 17:46:14 |
+--------+--------------------------------------+------------------------+---------------------+
6 rows in set (0.00 sec)

mysql> EXPLAIN SELECT id, path, filename, created FROM files WHERE path = '/sys/devices/virtual/tty/tty38/power';
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key      | key_len | ref   | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------------+
|  1 | SIMPLE      | files | NULL       | ref  | idx_path      | idx_path | 3074    | const |    6 |   100.00 | Using where |
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)
```

## UPDATE directory name
```
mysql> UPDATE files SET path = REGEXP_REPLACE(path, '/sys/devices/', '/sys/new_name/', 1, 1) WHERE path LIKE '/sys/devices/%';
```

## DELETE directory recursively
```
```
