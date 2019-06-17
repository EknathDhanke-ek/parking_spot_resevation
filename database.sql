-- Table: parking_spots_tbl

DROP TABLE IF EXISTS parking_spots_tbl;
CREATE TABLE parking_spots_tbl
(
  parking_spot_id_pk serial NOT NULL,
  latitute numeric NOT NULL,
  longitute numeric NOT NULL,
  is_available numeric NOT NULL,
  parking_fee int NOT NULL,
  CONSTRAINT parking_spots_tbl_pkey PRIMARY KEY (parking_spot_id_pk)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE parking_spots_tbl
  OWNER TO postgres;
GRANT ALL ON TABLE parking_spots_tbl TO postgres;

----------------------------------------------------------------------

-- Table: user_tbl

DROP TABLE IF EXISTS user_tbl;
CREATE TABLE user_tbl
(
  user_id_pk serial NOT NULL,
  f_name text NOT NULL,
  l_anme text NOT NULL,
  address text NOT NULL,
  gender text NOT NULL,
  contact_no int NOT NULL,
  CONSTRAINT user_tbl_pkey PRIMARY KEY (user_id_pk)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE user_tbl
  OWNER TO postgres;
GRANT ALL ON TABLE user_tbl TO postgres;

---------------------------------------------------------------------------


-- Table: user_parking_reservation_tbl

DROP TABLE IF EXISTS user_parking_reservation_tbl;
CREATE TABLE user_parking_reservation_tbl
(
  user_parking_id_pk serial NOT NULL,
  user_id_fk int not null,
  parking_spot_id_fk int not null,
  is_paid boolean,
  CONSTRAINT user_prking_reservation_tbl_pkey PRIMARY KEY (user_parking_id_pk),
  CONSTRAINT user_parking_reservation_tbl_user_id_fkey FOREIGN KEY (user_id_fk)
      REFERENCES user_tbl (user_id_pk) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT user_parking_reservation_tbl_parking_spot_id_fkey FOREIGN KEY (parking_spot_id_fk)
     REFERENCES parking_spots_tbl (parking_spot_id_pk) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE user_parking_reservation_tbl
  OWNER TO postgres;
GRANT ALL ON TABLE user_parking_reservation_tbl TO postgres;



--- Insertion
insert into user_tbl(f_name, l_anme, address, gender, contact_no) values('eknath', 'd', 'Pune', 'Male', 90967);
insert into parking_spots_tbl(latitute, longitute, is_available, parking_fee) values(12.56, 17.67, True, 20);

