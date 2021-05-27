drop database if exists iot_data;
create database iot_data;

grant all privileges on iot_data.* TO 'iot_user'@'%' identified by 'Cyberpunk2077_dso_wqff4tg8oxcvx';
flush privileges;

USE iot_data;

CREATE TABLE devices (
    device_id varchar(50) NOT NULL,
    status varchar(50) NOT NULL default 'active',
    location varchar(50),
    date datetime NOT NULL on update now(),
    PRIMARY KEY (device_id)
);

CREATE TABLE sensor_data (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    humidity float NOT NULL,
    temperature float NOT NULL,
    date timestamp NOT NULL default current_timestamp,
    device_id varchar(50) NOT NULL,
    FOREIGN KEY (device_id) references devices(device_id),
    PRIMARY key (id)
);