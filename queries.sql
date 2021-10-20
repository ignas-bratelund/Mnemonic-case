Create table if not exists mnemonic.account(
id int auto_increment Primary Key,
name Varchar(255) not null,
availableCash double not null
);

create table if not exists mnemonic.transaction(
id int auto_increment Primary key,
registeredTime long not null,
executedTime long,
success boolean not null,
cashAmount double not null,
sourceAccount int not null,
destinationAccount int not null,
Foreign key (sourceAccount)
	references account(id)
    on delete cascade,
Foreign key (destinationAccount)
	references account(id)
    on delete cascade
);

Insert into account(name, availableCash) values(
'Account1',
1000
);

Insert into account(name, availableCash) values(
'Account2',
100
);

Insert into account(name, availableCash) values(
'Account3',
50
);

Insert into transaction(registeredTime, executedTime, success, cashAmount, SourceAccount, destinationAccount) values(
1634474556250,
1634474556250,
1,
100,
1,
2
);
