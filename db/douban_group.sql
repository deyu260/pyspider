CREATE TABLE `douban_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gid` char(20) DEFAULT '',
  `face` char(60) DEFAULT '',
  `name` char(60) DEFAULT '',
  `leader` char(60) DEFAULT '',
  `content` text DEFAULT '',
  `join_at` datetime NOT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5000 DEFAULT CHARSET=utf8;