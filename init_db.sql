drop table if exists "user" cascade;
drop table if exists message cascade;
drop table if exists chat cascade;

create table "user" (
    id serial primary key,
    username varchar(30),
    hashed_password varchar(100),
    unique (username)
);

create table chat (
    id serial primary key,
    user_id1 integer references "user"(id),
    user_id2 integer references "user"(id)
);

create table message (
    id serial primary key,
    user_id integer references "user"(id),
    chat_id integer references chat(id),
    content varchar(280),
    created timestamp
);
