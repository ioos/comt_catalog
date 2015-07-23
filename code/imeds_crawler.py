import os
import datetime
import sys
import netCDF4

def isimeds(path):
    imeds_bool = False
    if path.endswith(".imeds") or path.endswith(".IMEDS"):
        imeds_bool = True
        print path
    return imeds_bool
        
def alreadync(path):
    nc_bool = False
    if path.endswith(".imeds"):
        if os.path.exists(path.replace(".imeds", ".nc")):
            nc_bool = True
    elif path.endswith(".IMEDS"):
        if os.path.exists(path.replace(".IMEDS", ".nc")):
            nc_bool = True
    return nc_bool

def walk(path, saveto):
    for root, folders, files in os.walk(path):
        for i in files:
            if isimeds(i):
                pathtoimeds = os.path.join(root, i)
                pathtonewnc = os.path.join(saveto, i)
                if not alreadync(pathtoimeds):
                    print "Found an IMEDS file without an netcdf file..."
                    ### convert to netcdf here
                    bool = imeds2netcdf(pathtoimeds, pathtonewnc)
                    if bool:
                        print "...File created successfully"
                    else:
                        print "...There was an error in creating the netcdf file"
                
def imeds2netcdf(path, pathnc):
    try:
    # open imeds file
        f = open(path)
        
        # open new nc file
        if path.endswith(".imeds"):
            print pathnc.replace(".imeds", ".nc")
            nc = netCDF4.Dataset(pathnc.replace(".imeds", ".nc"), 'w')
            
        else:
            print pathnc.replace(".IMEDS", ".nc")
            nc = netCDF4.Dataset(pathnc.replace(".IMEDS", ".nc"), 'w')
            
        nc.featureType = "timeSeries"
        nc.Conventions = "CF-1.5"
        nc.__setattr__("CF:featureType", 'timeSeries')
        nc.date_created = ''
        nc.netcdf_author = ''
        nc.keywords = ''
        nc.history = 'Converted from standard imeds text file format to netcdf ragged array with imeds_crawler.py'
        nc.institution = ''
        nc.project = ''
        nc.creator_email = ''
        nc.creator_url = ''
        nc.creator_name = ''
        nc.summary = ''
        # create dimensions
        station = nc.createDimension('station', size=None) 
        obs = nc.createDimension('obs', size=None)
        name_strlen = nc.createDimension('name_strlen', size=100)
        # create variables
        station_name = nc.createVariable('station_name', 'S1', ('station', 'name_strlen',))
        station_name.long_name = "station name"
        station_name.standard_name = "station_name"
        station_name.cf_role = "timeseries_id"
        lat = nc.createVariable('lat', 'f4', ('station',))
        lat.long_name = "latitude"
        lat.standard_name = "latitude"
        lat.units = "degrees_north"
        lon = nc.createVariable('lon', 'f4', ('station',))
        lon.long_name = "longitude"
        lon.standard_name = "longitude"
        lon.units = "degrees_east"
        time = nc.createVariable('time', 'f8', ('obs',))
        time.standard_name = "time"
        time.units = 'days since 1970-01-01 00:00:00'
        row_size = nc.createVariable('row_size', 'i4', ('station',))
        row_size.long_name = "number of observations for this station"
        row_size.sample_dimension = "obs"
        # write to variables
        station_count = 0
        
        for i,line in enumerate(f):
            if i == 0:
                pass
            elif i == 1:
                currentline = line.strip("%")
                currentline = currentline.strip()
                list_colum = currentline.split()
                has_min, has_sec = False, False
                waterlevel_columnind = 1
                highwater_columnind = 1
                waveheight_columnind = 1
                waveperiod_columnind = 1
                wavedir_columnind = 1
                windspeed_columnind = 1
                winddir_columnind = 1
                list_columns = []
                units = dict()
                for l in list_colum:
                    if l.startswith("("):
                        indexdict = len(list_columns)
                        units[indexdict] = l.strip("()")
                    else: list_columns.append(l)
                length = len(list_columns)
                for ind, qq in enumerate(list_columns):
                    if qq == "year":
                        pass
                    elif qq == "month":
                        pass
                    elif qq == "day":
                        pass
                    elif qq == "hour":
                        pass
                    elif qq == "min":
                        has_min = True
                    elif qq == "sec":
                        has_sec = True
                    elif qq == "watlev":
                        waterlevel = nc.createVariable('watlev', 'f4', ('obs',), fill_value=-999.0)
                        waterlevel.coordinates = "time lat lon"
                        waterlevel_columnind = -1 - (length - ind)
                        try: 
                            waterlevel.units = units[ind + 1]
                        except: pass
                    elif qq == "hwm":
                        highwater = nc.createVariable('hwm', 'f4', ('obs',), fill_value=-999.0)
                        highwater.coordinates = "time lat lon"
                        highwater_columnind = -1 - (length - ind)
                        try: 
                            highwater.units = units[ind + 1]
                        except: pass
                    elif qq == "hs":
                        waveheight = nc.createVariable('hs', 'f4', ('obs',), fill_value=-999.0)
                        waveheight.coordinates = "time lat lon"
                        waveheight_columnind = -1 - (length - ind)
                        try: 
                            waveheight.units = units[ind + 1]
                        except: pass
                    elif qq == "tp":
                        waveperiod = nc.createVariable('tp', 'f4', ('obs',), fill_value=-999.0)
                        waveperiod.coordinates = "time lat lon"
                        waveperiod_columnind = -1 - (length - ind)
                        try: 
                            waveperiod.units = units[ind + 1]
                        except: pass
                    elif qq == "dir":
                        wavedir = nc.createVariable('wavedir', 'f4', ('obs',), fill_value=-999.0)
                        wavedir.coordinates = "time lat lon"
                        wavedir_columnind = -1 - (length - ind)
                        try: 
                            wavedir.units = units[ind + 1]
                        except: pass
                    elif qq == "wndSpd":
                        windspeed = nc.createVariable('wndspd', 'f4', ('obs',), fill_value=-999.0)
                        windspeed.coordinates = "time lat lon"
                        windspeed_columnind = -1 - (length - ind)
                        try: 
                            windspeed.units = units[ind + 1]
                        except: pass
                    elif qq == "wmdDir":
                        winddir = nc.createVariable('wnddir', 'f4', ('obs',), fill_value=-999.0)
                        winddir.coordinates = "time lat lon"
                        winddir_columnind = -1 - (length - ind)
                        try: 
                            winddir.units = units[ind + 1]
                        except: pass
                    else:
                        pass # actually pass
            elif i == 2:
                currentline = line.strip("%")
                currentline = currentline.strip()
                list_columns = currentline.split()
                if len(list_columns) > 0:
                    source = list_columns[0]
                    nc.source = source
                    head, tail = os.path.split(pathnc)
                    nc.title = "Imeds " + source + " " + tail
                if len(list_columns) > 1:
                    timezone = list_columns[1]
                    nc.timezone = timezone
                    time.timezone = timezone
                if len(list_columns) > 2:
                    datum = list_columns[2]
                    nc.datum = datum
            elif i == 3:
                currentline = line.strip("%")
                currentline = currentline.strip()
                list_columns = currentline.split()
                for i,l in enumerate(list_columns[0]):
                    station_name[station_count, i] = l
                lat[station_count], lon[station_count] = float(list_columns[1]), float(list_columns[2])
                time_count = 0
                running_count = 0
            else:
                currentline = line.strip("%")
                currentline = currentline.strip()
                list_columns = currentline.split()
                length2 = len(list_columns)
                if length2 == 3:
                    row_size[station_count] = time_count
                    station_count = station_count + 1
                    for i,l in enumerate(list_columns[0]):
                        station_name[station_count, i] = l
                    lat[station_count], lon[station_count] = float(list_columns[1]), float(list_columns[2])
                    
                    time_count = 0
                else:
                    # print list_columns.__str__()
                    if waterlevel_columnind < 0:
                        waterlevel[running_count] = list_columns[waterlevel_columnind + 1]
                    if highwater_columnind < 0:
                        highwater[running_count] = list_columns[highwater_columnind + 1]
                    if waveheight_columnind < 0:
                        waveheight[running_count] = list_columns[waveheight_columnind + 1]
                    if waveperiod_columnind < 0:
                        waveperiod[running_count] = list_columns[waveperiod_columnind + 1]
                    if wavedir_columnind < 0:
                        wavedir[running_count] = list_columns[wavedir_columnind + 1]
                    if windspeed_columnind < 0:
                        windspeed[running_count] = list_columns[windspeed_columnind + 1]
                    if winddir_columnind < 0:
                        winddir[running_count] = list_columns[winddir_columnind + 1]
                    
                    difference = length - length2
                    if has_sec:
                        if difference == 2:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]),)
                        elif difference == 1:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]), int(list_columns[4]),)
                        elif difference == 0:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]), int(list_columns[4]), int(list_columns[5]),)
                    elif has_min:
                        if difference == 1:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]),)
                        elif difference == 0:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]), int(list_columns[4]),)
                        elif difference == -1:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]), int(list_columns[4]), int(list_columns[5]),)
                    else:
                        if difference == 0:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]),)
                        elif difference == -1:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]), int(list_columns[4]),)
                        elif difference == -2:
                            curr_time = datetime.datetime(int(list_columns[0]), int(list_columns[1]), int(list_columns[2]), int(list_columns[3]), int(list_columns[4]), int(list_columns[5]),)
                    time[running_count] = netCDF4.date2num(curr_time, units = 'days since 1970-01-01 00:00:00', calendar='standard')
                    
                    time_count = time_count + 1
                    running_count = running_count + 1
                
        row_size[station_count] = time_count
        completed_bool = True
        nc.sync()
        nc.close()
        f.close()
    except:
        completed_bool = False
        
    finally:
        pass
    return completed_bool
        
    

if __name__ == "__main__":
    currentlocation = sys.argv[1]
    saveto = sys.argv[2]
    walk(currentlocation, saveto)
    
        
    
    
    
