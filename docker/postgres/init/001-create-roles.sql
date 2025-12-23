CREATE ROLE app_user LOGIN PASSWORD 'app_password';
CREATE ROLE liquibase_user LOGIN PASSWORD 'liquibase_password';

-- permisos básicos
GRANT CONNECT ON DATABASE postgres TO app_user;
GRANT CONNECT ON DATABASE postgres TO liquibase_user;
