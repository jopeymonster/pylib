# targets for webpage_link_crawler

# prop domains
""" 
format:
'DESIGNATION': 'FULL URL'    
"""    
PROPS = {
'DW':'https://www.derbywarehouse.com/',
'IC':'https://www.icewarehouse.com/',
'IW':'https://www.inlinewarehouse.com/',
'RB':'https://www.racquetballwarehouse.com/',
'RD':'https://www.ridingwarehouse.com/',
'RDT':'https://www.ridingwarehouse.com/trail.html',
'RDW':'https://www.ridingwarehouse.com/western.html',
'RDE':'https://www.ridingwarehouse.com/english.html',
'RW':'https://www.runningwarehouse.com/',
'RWM':'https://www.runningwarehouse.com/fpm.html',
'RWW':'https://www.runningwarehouse.com/fpw.html',
'RWX':'https://www.runningwarehouse.com/fpe.html',
'RA':'https://www.runningwarehouse.com.au/',
'SW':'https://www.skatewarehouse.com/',
'TK':'https://www.tacklewarehouse.com/',
'TO':'https://www.tennisonly.com.au/',
'TW':'https://www.tennis-warehouse.com/',
'TA':'https://www.totalpickleball.com.au/',
'RE':'https://www.runningwarehouse.eu/',
'TE':'https://www.tenniswarehouse-europe.com/',
'PBW':'https://www.pickleballwarehouse.com/',
'PA':'https://www.totalpadel.com/',
'XX':'Input exact URL',
'EX':'Quit'
}

# tag targets, is <header> tag
CLASS_HEADER = 'l-header'

# if available, WIP
CAT_DESC = {
'DW': 'catheader_info-catdesc',
'IC': 'catheader_info-catdesc',
'IW': 'catheader_info-catdesc',
'RB': 'catheader_info-catdesc',
'RD': 'catheader_info-catdesc',
'RW': 'catheader_info-catdesc',
'RA': 'catheader_info-catdesc',
'SW': 'catheader_info-catdesc',
'TK': 'header_container-content',
'TO': 'catheader_info-catdesc',
'TW': 'catheader_info-catdesc',
'TA': 'catheader_info-catdesc',
'RE': 'catheader_info-catdesc',
'TE': 'catheader_info-catdesc',
'PBW': 'catheader_info-catdesc',
'PA': 'catheader_info-catdesc',
}

# left menu
NAV = {
'SW':('mobile_content', 'l-content-menu'),
'TW':('mobile_content', 'l-content-menu'),
'TE':('mobile_content', 'l-content-menu'),
'TO':('mobile_content', 'l-content-menu'),
'TK':('mobile_content', 'l-content-menu'),
'RD':('mobile_content', 'l-content-menu'),
'RDT':('mobile_content', 'l-content-menu'),
'RDW':('mobile_content', 'l-content-menu'),
'RDE':('mobile_content', 'l-content-menu'),
'RW':('mobile_content', 'l-content-menu'),
'RWM':('mobile_content', 'l-content-menu'),
'RWW':('mobile_content', 'l-content-menu'),
'RWX':('mobile_content', 'l-content-menu'),
'RE':('mobile_content', 'l-content-menu'),
'IC':('mobile_content', 'l-content-menu'),
'IW':('mobile_content', 'l-content-menu'),
'DW':('mobile_content', 'l-content-menu'),
'RB':('mobile_content', 'l-content-menu'),
'PBW':('mobile_content', 'l-content-menu'),
'TA':('mobile_content', 'l-content-menu'),
'PA':('mobile_content', 'l-content-menu'),
}

# main view
CONTENT = {
# 'CONTENT_TOTAL_ID':'mobile_content',
# 'MAIN_CONTENT_ID':'main_content',
'SW':('mobile_content', 'l-content-area'),
'TW':('mobile_content', 'l-content-area'),
'TE':('mobile_content', 'l-content-area'),
'TO':('mobile_content', 'l-content-area'),
'TK':('mobile_content', 'l-content-area'),
'RD':('mobile_content', 'l-content-area'),
'RDT':('mobile_content', 'l-content-area'),
'RDW':('mobile_content', 'l-content-area'),
'RDE':('mobile_content', 'l-content-area'),
'RW':('mobile_content', 'l-content-area'),
'RWM':('mobile_content', 'l-content-area'),
'RWW':('mobile_content', 'l-content-area'),
'RWX':('mobile_content', 'l-content-area'),
'RE':('mobile_content', 'l-content-area'),
'IC':('mobile_content', 'l-content-area'),
'IW':('mobile_content', 'l-content-area'),
'DW':('mobile_content', 'l-content-area'),
'RB':('mobile_content', 'l-content-area'),
'PBW':('mobile_content', 'l-content-area'),
'TA':('mobile_content', 'l-content-area'),
'PA':('mobile_content', 'l-content-area'),
}


# standard html tags
STDTAGS = {
'STDTAG_NAV':'nav',
'STDTAG_ASIDE':'aside',
'STDTAG_ARTICLE':'article',
'STDTAG_DETAILS':'details',
'STDTAG_FIGCAPTION':'figcaption',
'STDTAG_FIGURE':'figure',
'STDTAG_FOOTER':'footer',
'STDTAG_FORM':'form',
'STDTAG_HEADER':'header',
'STDTAG_MAIN':'main',
'STDTAG_MARK':'mark',
'STDTAG_SECTION':'section',
'STDTAG_SUMMARY':'summary',
'STDTAG_TIME':'time'
}

# SP specific dicts
NAVTAGS = {
'SW':('mobile_content', 'l-content-menu'),
'TW':('mobile_content', 'l-content-menu'),
'TE':('mobile_content', 'l-content-menu'),
'TO':('mobile_content', 'l-content-menu'),
'TK':('mobile_content', 'l-content-menu'),
'RD':('mobile_content', 'l-content-menu'),
'RDT':('mobile_content', 'l-content-menu'),
'RDW':('mobile_content', 'l-content-menu'),
'RDE':('mobile_content', 'l-content-menu'),
'RW':('mobile_content', 'l-content-menu'),
'RWM':('mobile_content', 'l-content-menu'),
'RWW':('mobile_content', 'l-content-menu'),
'RWX':('mobile_content', 'l-content-menu'),
'RE':('mobile_content', 'l-content-menu'),
'IC':('mobile_content', 'l-content-menu'),
'IW':('mobile_content', 'l-content-menu'),
'DW':('mobile_content', 'l-content-menu'),
'RB':('mobile_content', 'l-content-menu'),
'PBW':('mobile_content', 'l-content-menu'),
'TA':('mobile_content', 'l-content-menu'),
'PA':('mobile_content', 'l-content-menu'),
}

NAVIDS = {
'SW':('mobile_content', 'l-content-menu'),
'TW':('mobile_content', 'l-content-menu'),
'TE':('mobile_content', 'l-content-menu'),
'TO':('mobile_content', 'l-content-menu'),
'TK':('mobile_content', 'l-content-menu'),
'RD':('mobile_content', 'l-content-menu'),
'RDT':('mobile_content', 'l-content-menu'),
'RDW':('mobile_content', 'l-content-menu'),
'RDE':('mobile_content', 'l-content-menu'),
'RW':('mobile_content', 'l-content-menu'),
'RWM':('mobile_content', 'l-content-menu'),
'RWW':('mobile_content', 'l-content-menu'),
'RWX':('mobile_content', 'l-content-menu'),
'RE':('mobile_content', 'l-content-menu'),
'IC':('mobile_content', 'l-content-menu'),
'IW':('mobile_content', 'l-content-menu'),
'DW':('mobile_content', 'l-content-menu'),
'RB':('mobile_content', 'l-content-menu'),
'PBW':('mobile_content', 'l-content-menu'),
'TA':('mobile_content', 'l-content-menu'),
'PA':('mobile_content', 'l-content-menu'),
}

NAVCLASSES = {
'SW':('mobile_content', 'l-content-menu'),
'TW':('mobile_content', 'l-content-menu'),
'TE':('mobile_content', 'l-content-menu'),
'TO':('mobile_content', 'l-content-menu'),
'TK':('mobile_content', 'l-content-menu'),
'RD':('mobile_content', 'l-content-menu'),
'RDT':('mobile_content', 'l-content-menu'),
'RDW':('mobile_content', 'l-content-menu'),
'RDE':('mobile_content', 'l-content-menu'),
'RW':('mobile_content', 'l-content-menu'),
'RWM':('mobile_content', 'l-content-menu'),
'RWW':('mobile_content', 'l-content-menu'),
'RWX':('mobile_content', 'l-content-menu'),
'RE':('mobile_content', 'l-content-menu'),
'IC':('mobile_content', 'l-content-menu'),
'IW':('mobile_content', 'l-content-menu'),
'DW':('mobile_content', 'l-content-menu'),
'RB':('mobile_content', 'l-content-menu'),
'PBW':('mobile_content', 'l-content-menu'),
'TA':('mobile_content', 'l-content-menu'),
'PA':('mobile_content', 'l-content-menu'),
}

CONT_TAGS = {
'SW':('mobile_content', 'l-content-area'),
'TW':('mobile_content', 'l-content-area'),
'TE':('mobile_content', 'l-content-area'),
'TO':('mobile_content', 'l-content-area'),
'TK':('mobile_content', 'l-content-area'),
'RD':('mobile_content', 'l-content-area'),
'RDT':('mobile_content', 'l-content-area'),
'RDW':('mobile_content', 'l-content-area'),
'RDE':('mobile_content', 'l-content-area'),
'RW':('mobile_content', 'l-content-area'),
'RWM':('mobile_content', 'l-content-area'),
'RWW':('mobile_content', 'l-content-area'),
'RWX':('mobile_content', 'l-content-area'),
'RE':('mobile_content', 'l-content-area'),
'IC':('mobile_content', 'l-content-area'),
'IW':('mobile_content', 'l-content-area'),
'DW':('mobile_content', 'l-content-area'),
'RB':('mobile_content', 'l-content-area'),
'PBW':('mobile_content', 'l-content-area'),
'TA':('mobile_content', 'l-content-area'),
'PA':('mobile_content', 'l-content-area'),
}

CONT_IDS = {
'SW':('mobile_content', 'l-content-area'),
'TW':('mobile_content', 'l-content-area'),
'TE':('mobile_content', 'l-content-area'),
'TO':('mobile_content', 'l-content-area'),
'TK':('mobile_content', 'l-content-area'),
'RD':('mobile_content', 'l-content-area'),
'RDT':('mobile_content', 'l-content-area'),
'RDW':('mobile_content', 'l-content-area'),
'RDE':('mobile_content', 'l-content-area'),
'RW':('mobile_content', 'l-content-area'),
'RWM':('mobile_content', 'l-content-area'),
'RWW':('mobile_content', 'l-content-area'),
'RWX':('mobile_content', 'l-content-area'),
'RE':('mobile_content', 'l-content-area'),
'IC':('mobile_content', 'l-content-area'),
'IW':('mobile_content', 'l-content-area'),
'DW':('mobile_content', 'l-content-area'),
'RB':('mobile_content', 'l-content-area'),
'PBW':('mobile_content', 'l-content-area'),
'TA':('mobile_content', 'l-content-area'),
'PA':('mobile_content', 'l-content-area'),
}

CONT_CLASSES = {
'SW':('mobile_content', 'l-content-area'),
'TW':('mobile_content', 'l-content-area'),
'TE':('mobile_content', 'l-content-area'),
'TO':('mobile_content', 'l-content-area'),
'TK':('mobile_content', 'l-content-area'),
'RD':('mobile_content', 'l-content-area'),
'RDT':('mobile_content', 'l-content-area'),
'RDW':('mobile_content', 'l-content-area'),
'RDE':('mobile_content', 'l-content-area'),
'RW':('mobile_content', 'l-content-area'),
'RWM':('mobile_content', 'l-content-area'),
'RWW':('mobile_content', 'l-content-area'),
'RWX':('mobile_content', 'l-content-area'),
'RE':('mobile_content', 'l-content-area'),
'IC':('mobile_content', 'l-content-area'),
'IW':('mobile_content', 'l-content-area'),
'DW':('mobile_content', 'l-content-area'),
'RB':('mobile_content', 'l-content-area'),
'PBW':('mobile_content', 'l-content-area'),
'TA':('mobile_content', 'l-content-area'),
'PA':('mobile_content', 'l-content-area'),
}

