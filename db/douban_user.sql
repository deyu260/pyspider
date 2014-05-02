CREATE TABLE `douban_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `face` char(60) DEFAULT '',
  `display_name` char(60) DEFAULT '',
  `link_name` char(60) DEFAULT '',
  `location` char(60) DEFAULT '',
  `join_at` datetime NOT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5000 DEFAULT CHARSET=utf8;