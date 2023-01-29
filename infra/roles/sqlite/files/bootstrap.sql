CREATE TABLE IF NOT EXISTS template (
	template_name TEXT PRIMARY KEY,
	user_id INT,
	name TEXT,
	email TEXT,
	address TEXT,
	payment_details TEXT,
	send_to TEXT,
	amount REAL,
	description TEXT
);
CREATE TABLE IF NOT EXISTS user (
	id INT PRIMARY KEY,
	name TEXT
);
