SET NOCOUNT ON
GO

USE master
GO
if exists (select * from sysdatabases where name='TwitterProject')
		drop database TwitterProject
GO

CREATE DATABASE TwitterProject;
GO

use TwitterProject
GO

DROP TABLE HASHTAGS;
DROP TABLE TWEETS;
DROP TABLE USERS;
DROP TABLE SEARCHES;
DROP TABLE RESEARCHERS;
DROP TABLE MENTIONS;
DROP TABLE PLACES;

CREATE TABLE RESEARCHERS (
    id              INT,
    full_name       VARCHAR(60) NOT NULL,
    profile         VARCHAR(500),
    PRIMARY KEY(id)
);

INSERT INTO RESEARCHERS VALUES (1, 'Gustavo Vasquez','Student at Tec');

CREATE TABLE SEARCHES (
    id              INT,
    description     VARCHAR(500),
    researcher_id   INT DEFAULT 101010,
    PRIMARY KEY(id),
    FOREIGN KEY (researcher_id) references RESEARCHERS(id) ON DELETE SET DEFAULT 
);

INSERT INTO SEARCHES VALUES (1, 'Tweets containing Black Lives Matter', 1);

CREATE TABLE USERS (
    id              BIGINT,
    "name"          VARCHAR(500),
    "description"   VARCHAR(500),
    verified        BIT,
    protected       BIT,
    "location"       VARCHAR(500),
    followers_count BIGINT,
    friends_count   BIGINT,
    created_date    VARCHAR(500),
    picture         VARCHAR(500),
    PRIMARY KEY(id)
);

CREATE TABLE TWEETS (
    id              BIGINT,
    "text"          VARCHAR(5000),
    "user"          BIGINT,
    created         VARCHAR(500),
    reply_to        VARCHAR(500),
    favorite_count  BIGINT,
    reply_count     BIGINT,
    retweet_count   BIGINT,
    is_quote        BIT,
    search_id       INT,
    media           VARCHAR(500),
    PRIMARY KEY(id),
    FOREIGN KEY("user") references USERS(id),
    FOREIGN KEY (search_id) references SEARCHES(id) ON DELETE CASCADE
);

CREATE TABLE HASHTAGS (
    tweet_id            BIGINT,
    hashtag             VARCHAR(280),
    index_beg           BIGINT,
    index_end           BIGINT,
    PRIMARY KEY(tweet_id, hashtag),
    FOREIGN KEY(tweet_id) references TWEETS(id) ON DELETE CASCADE
);


CREATE TABLE PLACES(
    tweet_id        BIGINT,
    id              VARCHAR(30),
    "type"          VARCHAR(500),
    "name"          VARCHAR(500),
    country         VARCHAR(500),
    latitude        FLOAT,
    longitude       FLOAT,
    PRIMARY KEY (id),
    FOREIGN KEY (tweet_id) references TWEETS(id) ON DELETE CASCADE 
);

select *
from Mentions;



