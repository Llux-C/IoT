create database iot_app;

use iot_app;

create table device_info
(
    id          int unsigned auto_increment primary key,
    code        varchar(128) default '' not null,
    name        varchar(128) default '' not null,
    description text,
    create_time datetime     default CURRENT_TIMESTAMP not null,
    user		varchar(128) default '' not null
);

create table device_message
(
    id        int unsigned auto_increment	primary key,
    alert     int           default 0                 not null,
    clientId  varchar(128)  default ''                not null,
    info      varchar(128)  default ''                not null,
    lat		  float 		default 0.0000            not null,
    lng		  float			default 0.0000            not null,
    timestamp datetime      default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    value     int           default 0                 not null
)charset = utf8;

create table user_info
(
    id       int unsigned auto_increment	primary key,
    name     varchar(128) default '' not null,
    password varchar(128) default '' not null,
    email    varchar(128) default '' not null
);