create table `t_user` (
    `id` int unsigned not null auto_increment,
    `name` varchar(16) not null default '',
    `phone` varchar(16) not null default '',
    `money` decimal(10,2) not null default 0,
    `birth` date,
    `gender` tinyint unsigned not null default 0,
    `status` tinyint unsigned not null default 0,
    `brief` text null,
    `time` timestamp not null default current_timestamp,
    primary key(`id`),
    unique key `idx_name` (`name`),
    key `idx_phone` (`phone`),
    key `idx_status` (`status`),
    key `idx_time` (`time`)
) engine=InnoDB auto_increment=1 default charset=utf8mb4;