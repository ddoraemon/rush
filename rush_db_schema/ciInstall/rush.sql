####CREATE DATABASE /*!32312 IF NOT EXISTS*/ rush /*!40100 DEFAULT CHARACTER SET utf8 */;

####USE rush;

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE rushset (
  id int(11) unsigned NOT NULL AUTO_INCREMENT,
  rush_name varchar(255) DEFAULT NULL,
  is_finish int(11) DEFAULT 0,
  rush_count int(11) DEFAULT 0,
  started_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (id),
  UNIQUE KEY rush_name (rush_name)
) ENGINE=InnoDB   DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

CREATE TABLE members (
  id int(11) unsigned NOT NULL AUTO_INCREMENT,
  phone varchar(255) DEFAULT NULL,
  rushset_id int(11) DEFAULT 0,
  is_rush_secceed int(11) DEFAULT 0,
  updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_at timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (id),
  UNIQUE KEY id (id)
) ENGINE=InnoDB   DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


