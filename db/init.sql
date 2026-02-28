CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    tenure INT,
    monthlycharges DOUBLE PRECISION,
    totalcharges DOUBLE PRECISION,

    contract VARCHAR(50),
    internetservice VARCHAR(50),
    paymentmethod VARCHAR(80),

    techsupport VARCHAR(30),
    onlinesecurity VARCHAR(30),
    onlinebackup VARCHAR(30),
    deviceprotection VARCHAR(30),
    streamingtv VARCHAR(30),
    streamingmovies VARCHAR(30),

    paperlessbilling VARCHAR(10),
    partner VARCHAR(10),
    dependents VARCHAR(10),
    gender VARCHAR(10),

    churn_probability DOUBLE PRECISION,
    risk_level VARCHAR(20),
    created_at TIMESTAMP
);