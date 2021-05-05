DROP KEYSPACE IF EXISTS test;
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true;

CREATE TABLE test.users
(
    id         uuid,
    username   text,
    email      text,
    first_name text,
    gender     text,
    last_name  text,
    solr_query text,
    PRIMARY KEY (id, username)
);

CREATE INDEX users_gender ON test.users (gender);
CREATE CUSTOM INDEX test_users_solr_query_index ON test.users (solr_query) USING 'com.datastax.bdp.search.solr.Cql3SolrSecondaryIndex';
CREATE CUSTOM INDEX ln_prefix ON test.users (last_name) USING 'org.apache.cassandra.index.sasi.SASIIndex';
CREATE CUSTOM INDEX fn_prefix ON test.users (first_name) USING 'org.apache.cassandra.index.sasi.SASIIndex';
