DROP TABLE IF EXISTS customer_data;

CREATE TABLE customer_data (
    time datetime NOT NULL,
    consumption FLOAT(53) NOT NULL,
    export FLOAT(53) NOT NULL,
    import FLOAT(53) NOT NULL,
    self_consumption FLOAT(53) NOT NULL,
    system_production FLOAT(53) NOT NULL
);