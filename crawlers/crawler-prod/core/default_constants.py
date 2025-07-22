# targets for webpage_link_crawler

# prop domains
""" 
format:
'DESIGNATION': 'FULL URL'    
"""    
PROPS = {
'BS':'https://books.toscrape.com/',
'QS':'https://quotes.toscrape.com/',
'EN':'https://www.espn.com/',
'DG':'https://data.gov/',
'YF':'https://finance.yahoo.com/',
'XX':'Input exact URL',
'EX':'Quit'
}

# tag targets, is <header> tag
CLASS_HEADER = 'l-header'

# if available, WIP
CAT_DESC = {
'EA': 'catheader_info-catdesc',
}

# left menu
NAV = {
'EA':('mobile_content', 'l-content-menu'),
}

# main view
CONTENT = {
# 'CONTENT_TOTAL_ID':'mobile_content',
# 'MAIN_CONTENT_ID':'main_content',
'EA':('mobile_content', 'l-content-area'),
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

# example dicts
NAVTAGS = {
'EA':('mobile_content', 'l-content-menu'),
}

NAVIDS = {
'EA':('mobile_content', 'l-content-menu'),
}

NAVCLASSES = {
'EA':('mobile_content', 'l-content-menu'),
}

CONT_TAGS = {
'EA':('mobile_content', 'l-content-area'),
}

CONT_IDS = {
'EA':('mobile_content', 'l-content-area'),
}

CONT_CLASSES = {
'EA':('mobile_content', 'l-content-area'),
}

