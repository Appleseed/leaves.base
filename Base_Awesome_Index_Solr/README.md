This repository contains solr configurations and a processor script written in python to populate the post index.

# Managing the Pre-Index
To configure the fields that Drupal indexes, go to the Configuration->Search and Metadata->Search API in the Admin panel.
From here, select the desired index.  In this view you can select the Fields tab and customize the fields that you want indexed.
If you want to index associated objects in Drupal, add them using the dropdown at the bottom of the screen.

The pre index utilizes dynamic fields for most content, however if there is a static field that needs to be added, the schema file is available under solr-conf/pre-conf/schema.xml.

To kick off indexing from Drupal, select the desired index under Configuration->Search and Metadata->Search API, then click the "Index Now" button.

Sometimes the "Index Now" button will be greyed out which indicates Drupal thinks the index is up to date.
If you need to reindex anyways, click the "Queue all items for reindexing" button then click "Index Now"

# Post-Index configuration
The schema for the post index is available under solr-conf/post-conf/schema.xml.
To add new fields, one must modify this schema file and adjust the processor script field mapping at processor/app/field\_config.py

# Pushing Updates to ZooKeeper
The solr configuration files for each collection are managed by ZooKeeper.  After making modifications you must push the updates to ZooKeeper and reload the collection.

To push changes to ZooKeeper, utilize the zkcli script found inside Solr distributions at server/scripts/cloud-scripts.

For example:
`/zkcli.sh -zkhost ss826806-1-zk-us-east-1-aws.measuredsearch.com:2181 -cmd upconfig -confname phyfinder -confdir solr-conf/post-conf`

To reload a collection, you can use the solr admin panel or issue the following curl command:
`curl http://ss826806-1-zk-us-east-1-aws.measuredsearch.com/solr/admin/collections?action=RELOAD&name=phyfinder`

# Running the Processor
The processor is configured to run automatically via cron.  However, instructions for running the Processor manually are available inside the processor folder.

