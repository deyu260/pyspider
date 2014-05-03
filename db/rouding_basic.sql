# http://www.rouding.com/chuantongshougong/
CREATE TABLE `rouding_basic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` char(200) DEFAULT '',
  `category` char(20) DEFAULT '',
  `cover` char(100) DEFAULT '',
  `body` text DEFAULT '',
  `url` char(100) DEFAULT '',
  `join_at` datetime NOT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5000 DEFAULT CHARSET=utf8;