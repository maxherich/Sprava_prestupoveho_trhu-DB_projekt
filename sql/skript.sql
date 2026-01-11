-- vytvoreni databaze
create database d;
use d;

-- vytvoreni tabulky majitel
create table majitel(
	id int primary key auto_increment,
    jmeno varchar(30) not null,
    prijmeni varchar(30) not null,
    email varchar(30) not null,
    rozpocet float not null check (rozpocet >= 0),
    aktivni bool not null
);
-- vytvoreni tabulky liga
create table liga(
	id int primary key auto_increment,
    nazev varchar(30) not null,
    zeme varchar(30) not null,
    uroven enum('1. liga', '2. liga', '3. liga') not null
);

-- vytvoreni tabulky klub
create table klub(
	id int primary key auto_increment,
    nazev varchar(30) not null,
    liga_id int not null,
    foreign key (liga_id) references liga(id),
    majitel_id int not null,
    foreign key(majitel_id) references majitel(id)
);

-- vytvoreni tabulky hrac
create table hrac(
	id int primary key auto_increment,
    jmeno varchar(30) not null,
    prijmeni varchar(30) not null,
    cislo_dresu int check(cislo_dresu > 0 and cislo_dresu < 100) not null,
    pozice enum('brankar', 'obrance', 'zaloznik', 'utocnik') not null,
    klub_id int not null,
    foreign key (klub_id) references klub(id)
);

-- vytvoreni tabulky prestup
create table prestup(
	id int primary key auto_increment,
    hrac_id int not null,
    foreign key(hrac_id) references hrac(id),
    kupujici_klub_id int not null,
    foreign key(kupujici_klub_id) references klub(id),
    datum date not null,
    cena float not null
);

-- vytvoreni procedury pro transakci prestupu
delimiter //
create procedure nakup_hrace (kupujici_klub_id int, hrac_id int, cena int)
begin	
	start transaction;
    update hrac set hrac.klub_id = kupujici_klub_id where hrac.id = hrac_id;
    update majitel set rozpocet = (rozpocet-cena) where majitel.id = (select majitel_id from klub where klub.id = kupujici_klub_id);
    update majitel set rozpocet = (rozpocet+cena) where majitel.id = (select majitel_id from klub where klub.id = (select klub_id from hrac where hrac.id = hrac_id));
    commit;
end//
delimiter ;

-- vytvoreni view pro seznam hracu
create view hraci_tymu
as
select hrac.id, jmeno, prijmeni, cislo_dresu, pozice, klub.nazev
from hrac
inner join klub on hrac.klub_id = klub.id
order by hrac.klub_id, cislo_dresu;

-- vytvoreni view pro seznam aktivnich majitelu
create view seznam_aktivnich_majitelu
as
select majitel.id, jmeno, prijmeni, email, rozpocet, klub.nazev
from majitel
inner join klub on klub.majitel_id = majitel.id
order by rozpocet desc;

create view seznam_prestupu
as
select hrac.jmeno as jmeno, hrac.prijmeni as prijmeni, klub.nazev as klub, datum, cena
from prestup
inner join hrac on prestup.hrac_id = hrac.id
inner join klub on prestup.kupujici_klub_id = klub.id
order by datum desc;