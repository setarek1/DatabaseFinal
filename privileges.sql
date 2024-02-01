-- DROP USER 'admin'@'localhost';
-- DROP USER 'report'@'localhost';
-- DROP USER 'usermanager'@'localhost';

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
CREATE USER 'report'@'localhost' IDENTIFIED BY 'report';
CREATE USER 'usermanager'@'localhost' IDENTIFIED BY 'usermanager';

GRANT ALL PRIVILEGES ON projSchema.* TO 'admin'@'localhost';

GRANT SELECT ON projSchema.user TO 'report'@'localhost';
GRANT SELECT ON projSchema.transaction TO 'report'@'localhost';
GRANT SELECT ON projSchema.wallet TO 'report'@'localhost';
GRANT SELECT ON projSchema.currencymarket TO 'report'@'localhost';


GRANT ALL PRIVILEGES ON projSchema.user TO 'usermanager'@'localhost';