#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: liuzhangpei
@contact: liuzhangpei@126.com
@site: http://www.livenowhy.com
@time: 17/3/27 10:21
@版本升级
"""

new_image_repository = """
CREATE TABLE `image_repository` (
  `image_uuid` varchar(64) NOT NULL,
  `team_uuid` varchar(64) NOT NULL,
  `repository` varchar(126) NOT NULL,
  `deleted` int(11) NOT NULL DEFAULT '0',
  `creation_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  `is_public` int(11) NOT NULL DEFAULT '0',
  `short_description` varchar(256) DEFAULT NULL,
  `detail` text,
  `download_num` int(11) NOT NULL DEFAULT '0',
  `enshrine_num` int(11) NOT NULL DEFAULT '0',
  `review_num` int(11) NOT NULL DEFAULT '0',
  `version` varchar(64) DEFAULT NULL,
  `latest_version` varchar(30) DEFAULT NULL,
  `pushed` int(11) NOT NULL DEFAULT '0',
  `is_code` int(11) NOT NULL DEFAULT '0',
  `logo` varchar(126) DEFAULT '',
  `src_type` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`image_uuid`,`repository`),
  KEY `ix_image_repository_team_uuid` (`team_uuid`),
  KEY `ix_image_repository_repository` (`repository`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

