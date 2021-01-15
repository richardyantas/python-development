DROP TABLE IF EXISTS commands CASCADE;
CREATE TABLE commands (
  id serial primary key,
  category varchar(25) not null,
  commandline varchar(50),
  description varchar(200)
);
