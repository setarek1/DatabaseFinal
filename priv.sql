CREATE USER 'admin'@'%';
# Privileges for `admin`@`%`

GRANT ALL PRIVILEGES ON *.* TO `admin`@`%` IDENTIFIED BY PASSWORD '*4ACFE3202A5FF5CF467898FC58AAB1D615029441' WITH GRANT OPTION;

GRANT ALL PRIVILEGES ON `project`.* TO `admin`@`%`;

CREATE USER 'report'@'%';
# Privileges for `report`@`%`

GRANT SELECT, SHOW VIEW ON *.* TO `report`@`%` IDENTIFIED BY PASSWORD '*8E2B5A8BF835E14935C5C7F3ADE1022CE13A371F';

GRANT ALL PRIVILEGES ON `project`.* TO `report`@`%`;

-- # Privileges for `root`@`127.0.0.1`

-- GRANT ALL PRIVILEGES ON *.* TO `root`@`127.0.0.1` WITH GRANT OPTION;


-- # Privileges for `root`@`::1`

-- GRANT ALL PRIVILEGES ON *.* TO `root`@`::1` WITH GRANT OPTION;


-- # Privileges for `root`@`localhost`

-- GRANT ALL PRIVILEGES ON *.* TO `root`@`localhost` WITH GRANT OPTION;

-- GRANT PROXY ON ''@'%' TO 'root'@'localhost' WITH GRANT OPTION;

CREATE USER 'usermanager'@'%';
# Privileges for `usermanager`@`%`

GRANT USAGE ON *.* TO `usermanager`@`%` IDENTIFIED BY PASSWORD '*98040B9209BEB5D64BEB08EE33957010C17DE1AF';

GRANT ALL PRIVILEGES ON `project`.* TO `usermanager`@`%`;

GRANT DELETE, CREATE, DROP, INDEX, ALTER, CREATE VIEW, SHOW VIEW, TRIGGER, DELETE HISTORY ON `project`.`user` TO `usermanager`@`%` WITH GRANT OPTION;