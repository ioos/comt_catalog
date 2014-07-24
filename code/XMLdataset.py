# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 08:52:32 2012

@author: rsignell
"""
import ncml
import StringIO

institutions = {
                "bio":"BIO - Bedford Institute of Oceanography, inundation",
                "uf":"UF - University of Florida, inundation",
                "mdl":"MDL - NOAA/NWS/MDL, inundation",
                "umass":"UMASS - University of Massachusetts, inundation",
                "vims":"VIMS - Virginia Institute of Marine Science, inundation",
                "und":"UND - University of Notre Dame, inundation",
                "usf":"USF - University of South Florida, inundation",
                "lsu":"LSU - Louisiana State University, inundation",
               }

def XMLdataset(ncmlFile='c:/rps/xml/thredds/testbedapps_dev/00_dir.ncml',
    datasetName='Foo',
    runSummary='Foo',
    urlPath='foo1/foo2/foo3',
    datasetID='foo1:foo2:foo3',
    coverage_type='modelResult', #acrosby
    coverage_vars='',            #acrosby
    cdm_data_type=''):        #acrosby


    try:
        ncf = ncml.Dataset.NcmlDataset(ncmlFile)
        ncf.addDatasetAttribute('id',datasetID)
        ncf.addDatasetAttribute('cdm_data_type',cdm_data_type)
        ncf.addDatasetAttribute('title',datasetName)
        ncf.addDatasetAttribute('summary',runSummary)
        ncf.addDatasetAttribute('ncmlFile',ncmlFile)
#        ncf.addDatasetAttribute('institution', institutions[datasetID.split(".")[1]])
        
#        try:
#            for cvar in coverage_vars.split(','): 
#                ncf.addVariableAttribute(cvar, 'coverage_content_type', coverage_type)
#        except:
#            pass

        strFile = StringIO.StringIO()
        ncf.writeNcmlBack(strFile)
        xml = strFile.getvalue()
        newloc=urlPath+"/Output"
        xml = xml.replace("Output",newloc)
        urlPath = urlPath[1:]
        xml_header = '<dataset name="%s" ID="%s" urlPath="%s"> <serviceName>all</serviceName>' \
            % (datasetName,datasetID,urlPath)
        xml_trailer = '</dataset>'
        xml = xml_header + xml + xml_trailer
    except IOError,v:
        print "I/O Error: %s" % (v)
        xml=''
    return xml 
