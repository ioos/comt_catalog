Script to grab ISO metadata from specified thredds catalogs using [ncISO](http://www.ngdc.noaa.gov/eds/tds/).  I used version 2.3 in stand alone mode.
```
cd $HOME/jar
wget -o %HOME/jar/nciso-2.3.jar http://www.ngdc.noaa.gov/eds/tds/downloads/ncISO-2.3.jar
cd $HOME/comt_catalog/nciso
 ./do_nciso_comt1_summary  >& comt1_summary.log &
```
