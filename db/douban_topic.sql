CREATE TABLE `douban_topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tid` char(20) DEFAULT '',
  `user_id` char(60) DEFAULT '',
  `group_id` char(60) DEFAULT '',
  `title` varchar(200) DEFAULT '',
  `content` text DEFAULT '',
  `join_at` datetime NOT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5000 DEFAULT CHARSET=utf8;