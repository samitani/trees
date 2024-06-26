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

## SELECT all files
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
```

## SELECT parent directory paths of specific directory
```
```

## SELECT child directory paths of specific directory
```
```

## SELECT all file names under specific directory
```
```

## SELECT file names in specific directory
```
```

## UPDATE directory name
```
```

## DELETE directory recursively
```
```
