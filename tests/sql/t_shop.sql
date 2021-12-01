create table `t_shop` (
    `sid` varchar(16) not null,
    `name` varchar(16) not null default '',
    `phone` varchar(16) not null default '',
    `status` tinyint unsigned not null default 0,
    `time` timestamp not null default current_timestamp,
    primary key(`sid`),
    unique key `idx_name` (`name`),
    key `idx_phone` (`phone`),
    key `idx_status` (`status`),
    key `idx_time` (`time`)
) engine=InnoDB default charset=utf8;