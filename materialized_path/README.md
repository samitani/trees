# DDL
```
CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `path` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_created` (`created`)
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
