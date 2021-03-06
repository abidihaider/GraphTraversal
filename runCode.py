import os
import argparse
import time
import datetime
import re
from collections import OrderedDict
from Graph import Graph
import itertools



def main():
    siteConfig = OrderedDict() 
    ######################################
    # define the site configuration
    ######################################

    option = OrderedDict()
    name = "HRPS"
    option["Name"]      = name
    option["Link"]      = ["Bronte", "WhiteOaks"]
    option["Type"]      = ["Dispatch", "Prime", "Core"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Prime": 1008, "Dispatch": 1640 + 1304, "DSRCore": 5200, "GeoPrime": 10000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Bronte"
    option["Name"]      = name
    option["Link"]      = ["Lakeshore", "HRPS"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()    
    name = "WhiteOaks"
    option["Name"]      = name
    option["Link"]      = ["HRPS", "MiltonWT"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Lakeshore"
    option["Name"]      = name
    option["Link"]      = ["Waterdown", "Bronte"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Waterdown"
    option["Name"]      = name
    option["Link"]      = ["BurlingtonFire", "Rattlesnake" , "Lakeshore"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "BurlingtonFire"
    option["Name"]      = name
    option["Link"]      = ["Waterdown"]
    option["Type"]      = ["Dispatch"]
    option["Zone"]      = 1
    option["Site"]      = 0
    option["Bandwidth"] = {"Dispatch": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Rattlesnake"
    option["Name"]      = name
    option["Link"]      = ["MiltonFire", "Brookville" , "Waterdown", "MiltonWT"]
    #option["Link"]      = ["MiltonFire", "Brookville" , "Waterdown", "Ghost"]
    option["Type"]      = ["Subsite", "GeoPrime"]
    option["Zone"]      = 1
    option["Site"]      = 1
    option["Bandwidth"] = {"Subsite": 2000, "Prime": 1008 , "GeoPrime": 10000}
    siteConfig[name] = option

    # for testing
    #option = OrderedDict()
    #name = "Ghost"
    #option["Name"]      = name
    #option["Link"]      = ["MiltonWT", "Rattlesnake"]
    #option["Type"]      = ["Subsite"]
    #option["Zone"]      = 1
    #option["Site"]      = 1
    #option["Bandwidth"] = {"Subsite": 0}
    #siteConfig[name] = option

    option = OrderedDict()
    name = "MiltonWT"
    option["Name"]      = name
    option["Link"]      = ["WhiteOaks", "Rattlesnake" , "Speyside"]
    #option["Link"]      = ["WhiteOaks", "Ghost", "Speyside"]
    option["Type"]      = ["Subsite", "Prime"]
    option["Zone"]      = 1
    option["Site"]      = 2
    option["Bandwidth"] = {'Subsite': 352, "Prime": 2000}
    siteConfig[name] = option


    option = OrderedDict()
    name = "MiltonFire"
    option["Name"]      = name
    option["Link"]      = ["Rattlesnake"]
    option["Type"]      = ["Dispatch"]
    option["Zone"]      = 1
    option["Site"]      = 0
    option["Bandwidth"] = {"Dispatch": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Brookville"
    option["Name"]      = name
    option["Link"]      = ["Acton", "Rattlesnake"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 2
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Acton"
    option["Name"]      = name
    option["Link"]      = ["Georgetown", "Brookville"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 2
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Georgetown"
    option["Name"]      = name
    option["Link"]      = ["HHFire", "Speyside" , "Acton"]
    option["Type"]      = ["Subsite", "DSRCore"]
    option["Bandwidth"] = {'Subsite': 688, "DSRCore": 5200}
    option["Zone"]      = 1
    option["Site"]      = 2
    siteConfig[name] = option

    option = OrderedDict()
    name = "HHFire"
    option["Name"]      = name
    option["Link"]      = ["Georgetown"]
    option["Type"]      = ["Dispatch"]
    option["Zone"]      = 1
    option["Site"]      = 0
    option["Bandwidth"] = {"Dispatch": 2000}
    siteConfig[name] = option

    option = OrderedDict()
    name = "Speyside"
    option["Name"]      = name
    option["Link"]      = ["MiltonWT", "Georgetown"]
    option["Type"]      = ["Subsite"]
    option["Zone"]      = 1
    option["Site"]      = 2
    option["Bandwidth"] = {"Subsite": 2000}
    siteConfig[name] = option

    ##########################
    # Construct the graph
    ##########################
    siteGraph = getGraph(siteConfig)    
    print(siteGraph)

   
    ##########################
    # Run the test
    ##########################
    runTest(siteConfig, siteGraph)



def runTest(siteConfig, siteGraph):
    "This function is designed to run the bandwidth loading tests"

    ####################
    # MetaInformation
    ####################

    # First list a list of unique 'Site' numbers that are avaliable in the network
    uniqueSite = []
    for key in siteConfig:
        uniqueSite.append(siteConfig[key]["Site"])
        pass
    uniqueSite = list(set(uniqueSite))

    # first find the unique zones in the graph
    uniqueZone = []
    for key in siteConfig:
        uniqueZone.append(siteConfig[key]["Zone"])
        pass
    uniqueZone = list(set(uniqueZone))


   
    print '---------------------------------------------------------'
    print 'SUT to PUT loading\n'

    # for each site number, find all the Prime and GeoPrime sites
    uniquePrimeSite = {}
    for siteNum in uniqueSite:
        uniquePrimeSite[siteNum] = []
        for key in siteConfig:
            if('Prime' in siteConfig[key]['Type'] and siteConfig[key]['Site'] == siteNum):
                uniquePrimeSite[siteNum].append(key)
                pass
            if('GeoPrime' in siteConfig[key]['Type'] and siteConfig[key]['Site'] == siteNum):
                uniquePrimeSite[siteNum].append(key)
                pass

            pass
        pass

    # delete any site number that has not Prime or GeoPrime location
    # this is due to fact that 'Dispatch' locations have a site number designation of 0
    keysToDelete = []
    for key in uniquePrimeSite:
        #print key, uniquePrimeSite[key], len(uniquePrimeSite[key])
        if(len(uniquePrimeSite[key]) == 0):
            keysToDelete.append(key)
            pass
        pass
    for key in keysToDelete:
        del uniquePrimeSite[key]

    # Debug Output
    print "Unique prime sites", uniquePrimeSite

    # for each Prime/GeoPrime site, find all the loading senarios for SUT to PUT graphs
    # Store this information for later use
    SUT_to_PUT_loading = {}
    for siteNum in uniquePrimeSite:
        if(len(uniquePrimeSite[siteNum]) == 0):
            continue

        for site in uniquePrimeSite[siteNum]:
            print "Testing SUT to PUT loading", siteNum, site
            SUT_to_PUT_loading[site] = runSubSiteToPrimeTest(site, siteConfig, siteGraph)
            pass
        pass

    print '---------------------------------------------------------'

    ##################################
    # This is PUT to CUT loading senairo
    # Basic idea: create all combinations of Prime/GeoPrime at can be active for all site numbers
    # Similarly, create all combinations of core/DSR that can be active in a given zone
    # then compute the loading for all senarios
    # this is creating the correct input format for itertool to create the 
    # cartesian product of prime/GeoPrime sites

    print '---------------------------------------------------------'
    print 'PUT to CUT loading\n'

    primeSiteList = []
    for siteNum in uniquePrimeSite:
        primeSiteList.append(uniquePrimeSite[siteNum])
        pass

    ## Debug output
    print "Prime Site list: ", primeSiteList
    #activePrimeSiteCombinations = itertools.product(*primeSiteList)
    #for currActivePrime in itertools.product(*primeSiteList):
    #    print "Prime Iter Site list: ", currActivePrime

    # for each zone, find the list of Cores/DSR cores
    uniqueZoneSite = {}
    for zoneNum in uniqueZone:
        uniqueZoneSite[zoneNum] = []
        for key in siteConfig:
            if('Core' in siteConfig[key]['Type'] and siteConfig[key]['Zone'] == zoneNum):
                uniqueZoneSite[zoneNum].append(key)
                pass
            if('DSRCore' in siteConfig[key]['Type'] and siteConfig[key]['Zone'] == zoneNum):
                uniqueZoneSite[zoneNum].append(key)
                pass

            pass
        pass

    # debug output
    print "Active core/DSR Core", uniqueZoneSite

    # For each zone in the graph
    # loop over all Core/DSRCore
    # compute the loading for each Prime/GeoPrime senairo
    PUT_TO_CUT_loading = {}
    for zoneNum in uniqueZoneSite:
        for activeCore in uniqueZoneSite[zoneNum]:
            PUT_TO_CUT_loading[activeCore] = {}
            for currActivePrime in itertools.product(*primeSiteList):
                print 'Running PUT to CUT Loading', activeCore, currActivePrime
                PUT_TO_CUT_loading[activeCore][currActivePrime] = runPrimeToCoreTest(activeCore, currActivePrime, siteConfig, siteGraph)
                pass
            pass
        pass
    print '---------------------------------------------------------'


    ##################################
    # This is DUT to CUT loading senairo
    # For each core, compute the loading senario for where all dispatch sites talk to an active core/DSR
    DUT_TO_CUT_loading = {}
    print '---------------------------------------------------------'
    print 'DUT to CUT loading\n'

    for zoneNum in uniqueZoneSite:
        for activeCore in uniqueZoneSite[zoneNum]:
            print "Testing active Core:",activeCore
            DUT_TO_CUT_loading[activeCore] = runDispatchToCoreTest(activeCore, siteConfig, siteGraph)
            pass
        pass
    print '---------------------------------------------------------'

    ######################################
    # Compute the GeoPrime -> Prime loading

    print '---------------------------------------------------------'
    print 'GeoPrime to Prime loading\n'


    # for each site number, find all the Prime and GeoPrime sites
    primeToGeoPrimeList = {}
    for siteNum in uniqueSite:
        primeKey = None
        geoPrimeKey = None
        for key in siteConfig:
            if('Prime' in siteConfig[key]['Type'] and siteConfig[key]['Site'] == siteNum):
                primeKey = key
                pass
            if('GeoPrime' in siteConfig[key]['Type'] and siteConfig[key]['Site'] == siteNum):
                geoPrimeKey = key
                pass
            pass
        if(primeKey is not None and geoPrimeKey is not None):
            primeToGeoPrimeList[primeKey] = geoPrimeKey
            pass
        pass

    print primeToGeoPrimeList

    PUT_TO_GPUT_loading = {}

    for site in primeToGeoPrimeList:
        print "Testing active prime:", site, 'GeoPrime:' ,primeToGeoPrimeList[site]
        PUT_TO_GPUT_loading[site] = runPrimeToGeoPrimeTest(site, primeToGeoPrimeList[site], siteConfig, siteGraph)
        # save a copy going the other way        
        PUT_TO_GPUT_loading[primeToGeoPrimeList[site]] = runPrimeToGeoPrimeTest(site, primeToGeoPrimeList[site], siteConfig, siteGraph)
        pass
    print '---------------------------------------------------------'


    # Compute the DSR -> Core Loading
    print '---------------------------------------------------------'
    print 'Core to DSR Core loading\n'


    # for each site number, find all the Prime and GeoPrime sites
    coreToDSRCoreList = {}
    for zoneNum in uniqueZone:
        coreKey = None
        DSRCoreKey = None
        for key in siteConfig:
            if('Core' in siteConfig[key]['Type'] and siteConfig[key]['Zone'] == zoneNum):
                coreKey = key
                pass
            if('DSRCore' in siteConfig[key]['Type'] and siteConfig[key]['Zone'] == zoneNum):
                DSRCoreKey = key
                pass
            pass
        if(coreKey is not None and DSRCoreKey is not None):
            coreToDSRCoreList[coreKey] = DSRCoreKey
            pass
        pass

    CUT_TO_DCUT_loading = {}

    for site in coreToDSRCoreList:
        print "Testing active Core:", site, 'DSRCore:' ,coreToDSRCoreList[site]
        CUT_TO_DCUT_loading[site] = runCoreToDSRCoreTest(site, coreToDSRCoreList[site], siteConfig, siteGraph)
        # save a copy going the other way
        CUT_TO_DCUT_loading[coreToDSRCoreList[site]] = runCoreToDSRCoreTest(site, coreToDSRCoreList[site], siteConfig, siteGraph)
        pass
    print '---------------------------------------------------------'
    
    # Sum all possible scenarios and find the worst case loading for each node
    # loop over each zone
    for zoneNum in uniqueZone:
        print "Curr Zone", zoneNum
        # pick an active core or DSR core
        for activeCore in uniqueZoneSite[zoneNum]:
            print "Active Core:", activeCore
            # pick an active prime/geoprime for each site
            for currActivePrimes in itertools.product(*primeSiteList):
                print "Active PrimeList:", currActivePrimes


                # get the datastructure of bw loading
                TotalBwLoad = getBwMap(siteConfig)

                # add Core - DSR Core loading
                if activeCore in CUT_TO_DCUT_loading:
                    TotalBwLoad = addBwLoad(TotalBwLoad, CUT_TO_DCUT_loading[activeCore], siteConfig)
                    pass

                # add GeoPrime - Prime loading
                for activePrime in currActivePrimes:
                    if activePrime in PUT_TO_GPUT_loading:
                        TotalBwLoad = addBwLoad(TotalBwLoad, PUT_TO_GPUT_loading[activePrime], siteConfig)
                        pass

                # DUT to active core
                TotalBwLoad = addBwLoad(TotalBwLoad, DUT_TO_CUT_loading[activeCore], siteConfig)

                # SUT to active prime
                for activePrime in currActivePrimes:
                    TotalBwLoad = addBwLoad(TotalBwLoad, SUT_to_PUT_loading[activePrime], siteConfig)

                # add active prime to active core
                TotalBwLoad = addBwLoad(TotalBwLoad, PUT_TO_CUT_loading[activeCore][currActivePrimes], siteConfig)


                TotalBwLoad = cleanUpBWMatrix(TotalBwLoad, siteConfig)

                # print for debugging
                for key in siteConfig:
                    for keyprime in siteConfig:
                        if(TotalBwLoad[key][keyprime] == 0):
                            continue
                        print key, keyprime, TotalBwLoad[key][keyprime]
                        pass
                    pass
                print '********************'
                            
                pass
            pass
        pass
        

    # TODO: 1 point failure scenarios
    # TODO: Find max loading for each path, and tell which combination of active core and prime lead to that
    # TODO: Allow for a physical site to be in multiple zones
    ########################################
    # Long term future list
    # GUI? :P


def runCoreToDSRCoreTest(activeCore, activeDSR, siteConfig, siteGraph):
    "This function computes the loading from active core site in a zone to active DSRCore location"

    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)

    # load the network for all dispatch to active core
    bwLoad = computeLoading([activeCore], activeDSR, bwLoad, 'DSRCore', siteConfig, siteGraph)
    
    return bwLoad


def runPrimeToGeoPrimeTest(activePrime, activeGeoPrime, siteConfig, siteGraph):
    "This function computes the loading from active prime site in a site to activeGeoPrime location"

    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)

    # load the network for all dispatch to active core
    bwLoad = computeLoading([activePrime], activeGeoPrime, bwLoad, 'GeoPrime', siteConfig, siteGraph)
    
    return bwLoad



def runDispatchToCoreTest(activeCore, siteConfig, siteGraph):
    "This function computes the loading from all dispatch site in a zone to activeCore location"

    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)

    # get the dispatch sites in the same zone
    dispatchList = []
    for key in siteConfig:
        # skip any location that is not a dispatch
        if("Dispatch" not in siteConfig[key]['Type']):
            continue

        # skip any location that is not in the same zone 
        if(siteConfig[key]['Zone'] != siteConfig[activeCore]['Zone']):
            continue

        dispatchList.append(key)
        pass

    # load the network for all dispatch to active core
    bwLoad = computeLoading(dispatchList, activeCore, bwLoad, 'Dispatch', siteConfig, siteGraph)
    
    return bwLoad


def runPrimeToCoreTest(activeCore, currActivePrime, siteConfig, siteGraph):
    " This function computes the loading for active prime/geoprime locations to active cores in a zone"

    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)

    bwLoad = computeLoading(currActivePrime, activeCore, bwLoad, 'Prime', siteConfig, siteGraph)
    return bwLoad



def runSubSiteToPrimeTest(primeSiteName, siteConfig, siteGraph):
    " This function computes the loading for active subsite locations to active primes in a site"    
    
    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)

    # subsite -> prime test
    # first get the list of all subsites
    subsiteList = []
    for key in siteConfig:
        # skip any location that is not a subsite
        if("Subsite" not in siteConfig[key]['Type']):
            continue

        # skip any location that is not in the same site 
        if(siteConfig[key]['Site'] != siteConfig[primeSiteName]['Site']):
            continue

        subsiteList.append(key)
        pass

    bwLoad = computeLoading(subsiteList, primeSiteName, bwLoad, 'Subsite', siteConfig, siteGraph)
    return bwLoad


def computeLoading(fromSiteList, toSite, bwLoad, BandwidthOption, siteConfig, siteGraph):
    "This function computes the loading on the network, when all sites in the fromSiteList"
    "communicates to the toSite. The bandwidth for each site is choosen by the BandwidthOption input variable"

    # find the shortest path from each fromSite to toSite
    for fromSite in fromSiteList:
        #print 'Path from', fromSite, toSite
        pathList = siteGraph.find_shortest_path(fromSite, toSite)

        # if there is one path, pick that path, otherwise poll the user to pick one
        if(len(pathList) == 1):
            path = pathList[0]
        else:
            print pathList
            xString = input("Pick your path: ")
            x = int(xString)
            path = pathList[x]
            pass

        # for each edge in the path, load the line with the bandwidth 
        bwSite = siteConfig[fromSite]['Bandwidth'][BandwidthOption]
        for i in range(0, len(path)-1):
            bwLoad[path[i]][path[i+1]] += bwSite
            #print "loading", path[i], path[i+1], bwSite
            pass
        pass

    # print for debugging
    #for key in siteConfig:
    #    for keyprime in siteConfig:
    #        if(bwLoad[key][keyprime] == 0):
    #            continue
    #        print key, keyprime, bwLoad[key][keyprime]
    #        pass
    #    pass
    return bwLoad


def getBwMap(siteConfig):
    "define the struture to store graph bandwidth loading"    
    bwLoad = {}
    for key in siteConfig:
        bwLoad[key] = {}
        for keyprime in siteConfig:
            bwLoad[key][keyprime] = 0
            pass
        pass
    return bwLoad


def addBwLoad(BW1, BW2, siteConfig):
    "Add two BW loading scenario"    
    # get the datastructure of bw loading
    bwLoad = getBwMap(siteConfig)
    for key in bwLoad:
        for keyprime in bwLoad[key]:
            bwLoad[key][keyprime] = BW1[key][keyprime] + BW2[key][keyprime]
            pass
        pass
    return bwLoad


def cleanUpBWMatrix(BW, siteConfig):
    'Clean the matrix by adding the off diagonal terms' 
    bwLoad = getBwMap(siteConfig)
    # compute the transpose
    for key in bwLoad:
        for keyprime in bwLoad[key]:
            bwLoad[key][keyprime] = BW[keyprime][key]
            pass
        pass

    # sum matrix
    for key in bwLoad:
        for keyprime in bwLoad[key]:
            bwLoad[key][keyprime] =  bwLoad[key][keyprime] + BW[key][keyprime]
            pass
        pass

    # divide the diagonal terms by 2 to remove the double counting
    for key in bwLoad:
        bwLoad[key][key] =  bwLoad[key][key]/2
        pass

    # clean the lower off diagonal term
    i = 0
    for key in bwLoad:
        j = 0
        for keyprime in bwLoad[key]:
            if(j <= i):
                j = j + 1
                continue
            bwLoad[key][keyprime] = 0
            j = j + 1            
            pass
        i = i + 1
        pass

    return bwLoad


def getGraph(siteConfig):
    " This helper function creates the graph network for the site"
    graphDef = {}
    for key in siteConfig:
        graphDef[siteConfig[key]['Name']] = siteConfig[key]['Link']
        pass
    return Graph(graphDef)




if __name__ == "__main__":
    start_time = time.time()
    main()
    ex_time = time.time() - start_time
    print "Execution time ",str(datetime.timedelta(seconds=ex_time))
