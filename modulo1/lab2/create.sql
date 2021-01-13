DROP TABLE IF EXISTS commands CASCADE;
CREATE TABLE commands (
  id serial primary key,
  category varchar(25),
  commandline varchar(20),
  description varchar(50) not null
);
