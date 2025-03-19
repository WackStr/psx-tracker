create table t_share_price(
	ID serial,
	COMPANY_SCRIPT varchar(10),
	MEASURED_ON TIMESTAMP,
	CREATED_ON TIMESTAMP,
	PRICE decimal,
	primary key (ID)
);