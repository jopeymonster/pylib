"""py snippets"""

"""capture parameters"""
import re
def match_url(url):
  """Matches the given url against the regex."""
  match = re.match(r'\/\?(ccode|pcode)=(.*)', url)
  if match:
    return match.groups()
  else:
    return None

"""example"""
if __name__ == '__main__':
  url = '/?ccode=12345&pcode=54321'
  ccode, pcode = match_url(url)
  print(ccode, pcode)


"""regex target page capture parameter"""
import re
def match_url(url):
  """Matches the given url against the regex."""
  match = re.match(r'\/productvideo\.html\?pcode=(.*)|\/categoryvideo\.html\?pcode=(.*)', url)
  if match:
    return match.group(1)
  else:
    return None

"""example"""
if __name__ == '__main__':
  url = '/productvideo.html?pcode=12345'
  pcode = match_url(url)
  print(pcode)
