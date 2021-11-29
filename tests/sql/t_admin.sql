create table if not exists `t_admin` (
    `id` int unsigned not null auto_increment,
    `username` varchar(16) not null default '' comment '用户名',
    `phone` varchar(16) not null default '' comment '手机号',
    `password` varchar(64) not null default '' comment '密码',
    `role` int unsigned not null default 0 comment '角色ID',
    `type` tinyint unsigned not null default 0 comment '类型:0=管理员,1=超级管理员',
    `lock` tinyint unsigned not null default 0 comment '锁定:0=未锁定,1=已锁定',
    `time` timestamp not null default current_timestamp comment '注册时间',
    primary key(`id`),
    unique key `idx_username` (`username`),
    key `idx_phone` (`phone`),
    key `idx_role` (`role`),
    key `idx_type` (`type`),
    key `idx_time` (`time`)
) engine=InnoDB default charset utf8 comment '管理员表';
