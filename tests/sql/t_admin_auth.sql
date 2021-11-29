create table if not exists `t_admin_auth` (
    `id` int unsigned not null auto_increment,
    `role` int unsigned not null default 0 comment '角色ID',
    `action` int unsigned not null default 0 comment '权限ID',
    `time` timestamp not null default current_timestamp comment '时间',
    primary key(`id`),
    key `idx_role` (`role`),
    key `idx_action` (`action`),
    key `idx_time` (`time`)
) engine=InnoDB default charset utf8 comment '角色权限表';
