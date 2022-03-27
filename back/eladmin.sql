/*
MySQL Backup
Database: eladmin
Backup Time: 2021-02-04 11:45:49
*/

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `eladmin`.`alembic_version`;
DROP TABLE IF EXISTS `eladmin`.`sys_dept`;
DROP TABLE IF EXISTS `eladmin`.`sys_dict`;
DROP TABLE IF EXISTS `eladmin`.`sys_dict_detail`;
DROP TABLE IF EXISTS `eladmin`.`sys_job`;
DROP TABLE IF EXISTS `eladmin`.`sys_log`;
DROP TABLE IF EXISTS `eladmin`.`sys_menu`;
DROP TABLE IF EXISTS `eladmin`.`sys_role`;
DROP TABLE IF EXISTS `eladmin`.`sys_role_menus`;
DROP TABLE IF EXISTS `eladmin`.`sys_user`;
DROP TABLE IF EXISTS `eladmin`.`sys_users_jobs`;
DROP TABLE IF EXISTS `eladmin`.`sys_users_roles`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `sys_dept` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pid` bigint(20) DEFAULT NULL,
  `sub_count` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `dept_sort` int(11) DEFAULT NULL COMMENT '部门排序',
  `enabled` tinyint(1) DEFAULT NULL COMMENT '状态：1启用、0禁用',
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_dict` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_dict_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `dict_id` bigint(20) DEFAULT NULL,
  `label` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `dict_sort` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dict_id` (`dict_id`),
  CONSTRAINT `sys_dict_detail_ibfk_1` FOREIGN KEY (`dict_id`) REFERENCES `sys_dict` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_job` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `job_sort` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_log` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) DEFAULT NULL,
  `log_type` varchar(255) DEFAULT NULL,
  `method` varchar(255) DEFAULT NULL,
  `params` varchar(255) DEFAULT NULL,
  `request_ip` varchar(255) DEFAULT NULL,
  `time` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `browser` varchar(255) DEFAULT NULL,
  `system` varchar(255) DEFAULT NULL,
  `exception_detail` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `sys_menu` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pid` bigint(20) DEFAULT NULL,
  `sub_count` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `component` varchar(255) DEFAULT NULL,
  `menu_sort` int(11) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `i_frame` tinyint(1) DEFAULT NULL,
  `cache` tinyint(1) DEFAULT NULL,
  `hidden` tinyint(1) DEFAULT NULL,
  `permission` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_role` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `data_scope` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_role_menus` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `menu_id` bigint(20) DEFAULT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_id` (`menu_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `sys_role_menus_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `sys_menu` (`id`),
  CONSTRAINT `sys_role_menus_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `dept_id` bigint(20) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `nick_name` varchar(255) DEFAULT NULL,
  `gender` tinyint(1) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `avatar_name` varchar(255) DEFAULT NULL,
  `avatar_path` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `pwd_reset_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sys_users_dept_ibfk_1` (`dept_id`),
  CONSTRAINT `sys_users_dept_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `sys_dept` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_users_jobs` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL,
  `job_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sys_users_jobs_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `sys_job` (`id`),
  CONSTRAINT `sys_users_jobs_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
CREATE TABLE `sys_users_roles` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) DEFAULT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id` (`role_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sys_users_roles_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`),
  CONSTRAINT `sys_users_roles_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
BEGIN;
LOCK TABLES `eladmin`.`alembic_version` WRITE;
DELETE FROM `eladmin`.`alembic_version`;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_dept` WRITE;
DELETE FROM `eladmin`.`sys_dept`;
INSERT INTO `eladmin`.`sys_dept` (`id`,`pid`,`sub_count`,`name`,`dept_sort`,`enabled`,`create_time`,`update_time`) VALUES (1, 0, 2, '华北分部', 1, 1, '2021-01-29 09:24:20', '2021-02-04 08:57:00'),(2, 1, 0, '运维部', 2, 1, '2021-01-29 09:24:54', '2021-01-29 09:24:56'),(3, 1, 0, '开发部', 3, 0, '2021-01-30 11:22:04', '2021-01-30 11:22:07'),(4, 0, 1, '华南分部', 4, 1, '2021-01-30 15:52:59', '2021-02-04 10:53:08'),(17, 4, 0, 'UI部门', 11, 1, '2021-02-04 10:53:08', '2021-02-04 10:53:08');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_dict` WRITE;
DELETE FROM `eladmin`.`sys_dict`;
INSERT INTO `eladmin`.`sys_dict` (`id`,`name`,`description`,`create_time`,`update_time`) VALUES (1, 'job_status', '岗位状态', '2021-01-29 11:46:37', '2021-01-29 11:46:37'),(2, 'dept_status', '部门状态', '2021-01-29 11:46:37', '2021-01-29 14:47:37'),(3, 'user_status', '用户状态', '2021-01-29 14:47:37', '2021-01-29 14:47:37');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_dict_detail` WRITE;
DELETE FROM `eladmin`.`sys_dict_detail`;
INSERT INTO `eladmin`.`sys_dict_detail` (`id`,`dict_id`,`label`,`value`,`dict_sort`,`create_time`,`update_time`) VALUES (1, 1, '启用', '1', 1, '2021-01-29 15:29:48', '2021-01-30 21:24:21'),(2, 1, '停用', '0', 2, '2021-01-29 15:33:04', '2021-01-30 21:24:21'),(3, 2, '启用', 'true', 1, '2021-01-30 11:18:21', '2021-01-30 11:18:21'),(4, 2, '停用', 'flase', 2, '2021-01-30 11:18:21', '2021-01-30 11:18:21'),(5, 3, '激活', 'true', 1, '2021-01-30 20:11:34', '2021-01-30 20:11:34'),(6, 3, '禁用', 'false', 2, '2021-01-30 20:11:34', '2021-02-02 21:11:32');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_job` WRITE;
DELETE FROM `eladmin`.`sys_job`;
INSERT INTO `eladmin`.`sys_job` (`id`,`name`,`enabled`,`job_sort`,`create_time`,`update_time`) VALUES (1, '全栈开发', 1, 1, '2021-01-29 09:25:18', '2021-01-29 09:25:20'),(2, '人事专员', 1, 4, '2021-01-30 09:12:13', '2021-01-30 09:32:30'),(3, '产品经理', 0, 5, '2021-01-30 09:12:13', '2021-02-02 23:17:55'),(4, '软件测试', 1, 2, '2021-01-30 09:12:13', '2021-01-30 09:12:13');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_log` WRITE;
DELETE FROM `eladmin`.`sys_log`;
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_menu` WRITE;
DELETE FROM `eladmin`.`sys_menu`;
INSERT INTO `eladmin`.`sys_menu` (`id`,`pid`,`sub_count`,`type`,`title`,`name`,`component`,`menu_sort`,`icon`,`path`,`i_frame`,`cache`,`hidden`,`permission`,`create_time`,`update_time`) VALUES (1, 0, 6, 0, '系统管理', 'System', 'Layout', 1, 'system', '/system', 0, 0, 0, NULL, '2021-01-29 09:18:24', '2021-01-29 09:51:41'),(2, 1, 3, 1, '菜单管理', 'Menu', 'system/menu/index', 4, 'menu', 'menu', 0, 0, 0, 'menu:list', '2021-01-29 09:19:38', '2021-01-29 11:46:37'),(3, 1, 3, 1, '用户管理', 'User', 'system/user/index', 3, 'peoples', 'user', 0, 0, 0, 'user:list', '2021-01-29 09:51:41', '2021-02-02 23:17:55'),(4, 1, 3, 1, '部门管理', '部门管理', 'system/dept/index', 4, 'dept', 'dept', 0, 0, 0, 'dept:list', '2021-01-29 09:51:41', '2021-02-03 09:21:31'),(5, 1, 2, 1, '岗位管理', '岗位管理', 'system/job/index', 5, 'Steve-Jobs', 'job', 0, 0, 0, 'job:list', '2021-01-29 09:51:41', '2021-02-03 09:21:31'),(6, 1, 3, 1, '角色管理', 'Role', 'system/role/index', 6, 'role', 'role', 0, 0, 0, 'role:list', '2021-01-29 09:51:41', '2021-02-03 09:21:31'),(7, 1, 3, 1, '字典管理', 'Dict', 'system/dict/index', 7, 'dictionary', 'dict', 0, 0, 0, 'dict:list', '2021-01-29 09:51:41', '2021-02-03 09:21:31'),(8, 2, 0, 2, '新增菜单', NULL, NULL, 11, NULL, NULL, 0, 0, 0, 'menu:add', '2021-01-29 11:46:37', '2021-01-29 11:46:37'),(9, 2, 0, 2, '编辑菜单', NULL, NULL, 12, NULL, NULL, 0, 0, 0, 'menu:edit', '2021-01-29 11:46:37', '2021-01-29 11:46:37'),(10, 2, 0, 2, '删除菜单', NULL, NULL, 13, NULL, NULL, 0, 0, 0, 'menu:add', '2021-01-29 11:46:37', '2021-01-29 11:46:37'),(11, 3, 0, 2, '添加用户', NULL, NULL, 31, NULL, NULL, 0, 0, 0, 'user:add', '2021-02-02 23:17:55', '2021-02-02 23:17:55'),(12, 3, 0, 2, '编辑用户', NULL, NULL, 32, NULL, NULL, 0, 0, 0, 'user:edit', '2021-02-02 23:17:55', '2021-02-02 23:17:55'),(13, 3, 0, 2, '删除用户', NULL, NULL, 33, NULL, NULL, 0, 0, 0, 'user:del', '2021-02-02 23:17:55', '2021-02-02 23:17:55'),(14, 4, 0, 2, '添加部门', NULL, NULL, 41, NULL, NULL, 0, 0, 0, 'dept:add', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(15, 4, 0, 2, '编辑部门', NULL, NULL, 42, NULL, NULL, 0, 0, 0, 'dept:edit', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(16, 4, 0, 2, '删除部门', NULL, NULL, 43, NULL, NULL, 0, 0, 0, 'dept:del', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(17, 5, 0, 2, '新增岗位', NULL, NULL, 51, NULL, NULL, 0, 0, 0, 'job:add', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(18, 5, 0, 2, '编辑岗位', NULL, NULL, 53, NULL, NULL, 0, 0, 0, 'job:edit', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(19, 6, 0, 2, '添加角色', NULL, NULL, 61, NULL, NULL, 0, 0, 0, 'role:add', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(20, 6, 0, 2, '编辑角色', NULL, NULL, 63, NULL, NULL, 0, 0, 0, 'role:edit', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(21, 6, 0, 2, '删除角色', NULL, NULL, 62, NULL, NULL, 0, 0, 0, 'role:del', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(22, 7, 0, 2, '新增字典', NULL, NULL, 71, NULL, NULL, 0, 0, 0, 'dict:add', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(23, 7, 0, 2, '编辑字典', NULL, NULL, 72, NULL, NULL, 0, 0, 0, 'dict:edit', '2021-02-03 09:21:31', '2021-02-03 09:21:31'),(24, 7, 0, 2, '删除字典', NULL, NULL, 73, NULL, NULL, 0, 0, 0, 'dict:del', '2021-02-03 09:21:31', '2021-02-03 09:21:31');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_role` WRITE;
DELETE FROM `eladmin`.`sys_role`;
INSERT INTO `eladmin`.`sys_role` (`id`,`name`,`level`,`description`,`data_scope`,`create_time`,`update_time`) VALUES (1, '超级管理员', 2, '-', '本部', '2021-01-29 09:25:59', '2021-01-29 09:26:01'),(2, '普通用户2', 2, '这一个测试用户', '全部', '2021-01-30 10:03:24', '2021-01-30 10:06:21');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_role_menus` WRITE;
DELETE FROM `eladmin`.`sys_role_menus`;
INSERT INTO `eladmin`.`sys_role_menus` (`id`,`menu_id`,`role_id`) VALUES (1, 1, 1),(2, 2, 1),(3, 3, 1),(50, 1, 2),(51, 2, 2),(52, 8, 2),(53, 24, 2),(54, 23, 2),(55, 22, 2),(56, 7, 2),(57, 19, 2),(58, 20, 2),(59, 21, 2),(60, 6, 2);
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_user` WRITE;
DELETE FROM `eladmin`.`sys_user`;
INSERT INTO `eladmin`.`sys_user` (`id`,`dept_id`,`username`,`nick_name`,`gender`,`email`,`phone`,`avatar_name`,`avatar_path`,`password`,`is_admin`,`enabled`,`pwd_reset_time`,`create_time`,`update_time`) VALUES (1, 17, 'admin', 'admin', 0, 'admin@admin.com', '13512726061', NULL, NULL, '$2b$12$c6I3/6HIS6FuZl.40G.HOOuBucBqG1BUZmnw9TfZlqassU7zQP/Y.', 1, 1, '2021-01-29 09:21:56', '2021-01-29 09:21:59', '2021-02-04 10:55:02'),(2, 3, 'didiplus', 'didiplus', 0, 'didiplus@admin.com', '13512726061', NULL, NULL, '$2b$12$c6I3/6HIS6FuZl.40G.HOOuBucBqG1BUZmnw9TfZlqassU7zQP/Y.', NULL, 1, NULL, '2021-01-31 20:26:18', '2021-02-03 15:09:11'),(3, 3, 'test222', 'test222', 0, 'test222@admin.com', '13512725062', NULL, NULL, '$2b$12$9sm55LxusqkNblz/UmSoh..jcq8mz1dZoJ9B1SW6wSYRVrPrplvbe', NULL, 1, NULL, '2021-02-02 21:11:32', '2021-02-04 09:52:00');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_users_jobs` WRITE;
DELETE FROM `eladmin`.`sys_users_jobs`;
INSERT INTO `eladmin`.`sys_users_jobs` (`id`,`user_id`,`job_id`) VALUES (6, 3, 1),(7, 3, 4),(8, 3, 2),(11, 2, 1),(12, 2, 2),(13, 1, 1),(14, 1, 4),(15, 1, 2);
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `eladmin`.`sys_users_roles` WRITE;
DELETE FROM `eladmin`.`sys_users_roles`;
INSERT INTO `eladmin`.`sys_users_roles` (`id`,`user_id`,`role_id`) VALUES (12, 3, 1),(13, 3, 2),(16, 2, 2),(17, 1, 1),(18, 1, 2);
UNLOCK TABLES;
COMMIT;
