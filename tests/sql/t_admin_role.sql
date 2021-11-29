create table if not exists `t_admin_role` (
    `id` int unsigned not null auto_increment,
    `name` varchar(16) not null default '' comment '角色名称',
    `time` timestamp not null default current_timestamp comment '时间',
    primary key(`id`),
    key `idx_name` (`name`),
    key `idx_time` (`time`)
) engine=InnoDB default charset utf8 comment '管理员角色表';
