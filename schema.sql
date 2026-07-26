DROP TABLE IF EXISTS farmers;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS inventory;

-- ==========================
-- FARMERS TABLE
-- ==========================

CREATE TABLE farmers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    mobile TEXT NOT NULL,

    village TEXT NOT NULL,

    district TEXT NOT NULL,

    land REAL NOT NULL,

    crop TEXT NOT NULL,

    subsidy TEXT NOT NULL,

    eligible INTEGER NOT NULL,

    issued INTEGER DEFAULT 0,

    balance INTEGER DEFAULT 0,

    status TEXT DEFAULT 'Pending',

    latitude REAL,

    longitude REAL

);

-- ==========================
-- HISTORY TABLE
-- ==========================

CREATE TABLE history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    farmer_id INTEGER NOT NULL,

    quantity INTEGER NOT NULL,

    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (farmer_id) REFERENCES farmers(id)

);

-- ==========================
-- INVENTORY TABLE
-- ==========================

CREATE TABLE inventory (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    item_name TEXT NOT NULL,

    total_stock INTEGER NOT NULL,

    available_stock INTEGER NOT NULL

);

-- ==========================
-- SAMPLE INVENTORY DATA
-- ==========================

INSERT INTO inventory (item_name, total_stock, available_stock)
VALUES
('Rice Seeds',1000,850),
('Wheat Seeds',800,600),
('DAP Fertilizer',500,320),
('Urea Fertilizer',1000,760),
('Organic Fertilizer',700,420),
('Pesticide',450,210),
('Drip Irrigation Kit',120,85),
('Sprayer Machine',75,40),
('Tractor Subsidy',50,18),
('Water Pump',100,52);