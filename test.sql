BEGIN;
ALTER TABLE `auth_user_groups` DROP FOREIGN KEY `user_id_refs_id_831107f1`;
ALTER TABLE `auth_user_user_permissions` DROP FOREIGN KEY `user_id_refs_id_f2045483`;
DROP TABLE `auth_user`;
DROP TABLE `auth_user_groups`;
DROP TABLE `auth_user_user_permissions`;
ALTER TABLE `auth_group_permissions` DROP FOREIGN KEY `group_id_refs_id_3cea63fe`;
DROP TABLE `auth_group`;
DROP TABLE `auth_group_permissions`;
DROP TABLE `auth_permission`;
CREATE TABLE `auth_permission` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `content_type_id` integer NOT NULL,
    `codename` varchar(100) NOT NULL,
    UNIQUE (`content_type_id`, `codename`)
)
;
ALTER TABLE `auth_permission` ADD CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
CREATE TABLE `auth_group_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `group_id` integer NOT NULL,
    `permission_id` integer NOT NULL,
    UNIQUE (`group_id`, `permission_id`)
)
;
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
CREATE TABLE `auth_group` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(80) NOT NULL UNIQUE
)
;
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
CREATE TABLE `auth_user_user_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `permission_id` integer NOT NULL,
    UNIQUE (`user_id`, `permission_id`)
)
;
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
CREATE TABLE `auth_user_groups` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `group_id` integer NOT NULL,
    UNIQUE (`user_id`, `group_id`)
)
;
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
CREATE TABLE `auth_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `username` varchar(30) NOT NULL UNIQUE,
    `first_name` varchar(30) NOT NULL,
    `last_name` varchar(30) NOT NULL,
    `email` varchar(75) NOT NULL,
    `password` varchar(128) NOT NULL,
    `is_staff` bool NOT NULL,
    `is_active` bool NOT NULL,
    `is_superuser` bool NOT NULL,
    `last_login` datetime NOT NULL,
    `date_joined` datetime NOT NULL
)
;
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `auth_message` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `message` longtext NOT NULL
)
;
ALTER TABLE `auth_message` ADD CONSTRAINT `user_id_refs_id_9af0b65a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `auth_permission_e4470c6e` ON `auth_permission` (`content_type_id`);
CREATE INDEX `auth_message_fbfc09f1` ON `auth_message` (`user_id`);
COMMIT;
