IOOS Coastal and Ocean Modeling Testbed (COMT) Catalog
================

THREDDS catalogs for <http://comt.sura.org/thredds>. 


The CF compliant catalogs for harvesting by NGDC are automatically generated by scripts:
https://github.com/ioos/comt_catalog/blob/master/code/buildcatalog_comt1_archive.py
https://github.com/ioos/comt_catalog/blob/master/code/buildcatalog_comt2_current.py

which read a [google drive spreadsheet](https://docs.google.com/spreadsheet/ccc?key=0AmAEVaW9GoHedFZHU3Z4c1pyMkozWmJxSUlGSDk3eVE&usp=drive_web#gid=0) and are run thusly:
```
ssh testbed@comt.sura.org
cd /home/testbed/comt_catalog/code
python buildcatalog_comt1_archive.py
python buildcatalog_comt2_current.py
sudo /etc/init.d/tomcat_thredds restart
```
which writes the files
```
/home/testbed/comt_catalog/catalogs/comt_1_archive_summary.xml
/home/testbed/comt_catalog/catalogs/comt_2_current.xml
```
which is then pushed to github, and softlinked to 
```
/var/www/thredds_instance/content/thredds/comt_1_archive_summary.xml
/var/www/thredds_instance/content/thredds/comt_current.xml

```
where the THREDDS Data Server reads it.

