# leaves.base
Initially started as utilities to download and transform "awesome" lists into usable JSON or CSV files for ingestion into other systems.
Now it has several other components of the leaves stack which are related to data processing the links from Wallabag into Cassandra/Solr for scaling
the application.

#For Windows
##	step 1:
###	pip install markdown-to-json
##step 2:
###	include below line to md_to_json script under Lib\site-packages\markdown_to_json\scripts
###	reload(sys)

###	sys.setdefaultencoding('utf8')

##step 3:
###	execute collect.awesome.md.csvpy as below to get *.md file
###	collect.awesome.md.csvpy "Driver Url" "file name without extenation"
###	example collect.awesome.md.csvpy "https://raw.githubusercontent.com/sindresorhus/awesome-nodejs/master/readme.md" "sindresorhus_list_lists"
