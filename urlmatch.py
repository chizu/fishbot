"""
Packages: text.regular_expressions;networking.internet
"""

""" vagueurl.py -- regular expression to match informal URLs in plain text.

    This doesn't do and exact job (it doesn't parse the complete syntax
    of URLs) but it should find URLs that at least start right.
    It looks for the start of an address then gobbles up as many legal URL
    characters as it can find.

    Glyn Webster <glyn@ninz.org.nz> 1999-04-27
"""

import re

pattern = r'''
  ( ( \w | - | % )+ @  #  email address prefix (e.g. "glyn@")
  | \w+ ://            #  or protocol prefix (e.g. "http://")
  | news:              #  or "news:" prefix (special case: no "//")
  | mailto:            #
  | www \.             #  lazy typists leave off common prefixes
  | ftp \.
  )                    #  then
  [^\\{}|[\]^<>"'\s]*  #  the rest are any characters allowed in a URL.
  [^\\{}|[\]^<>"'\s.,;?:!]
                       #  it mustn't end in a punctuation mark or this would
                       #  match this wrong: "Www.w3.org, ftp.simtel.net."
'''

regex = re.compile(pattern, re.IGNORECASE | re.VERBOSE)

def regular(url):
  """ Add an appropiate prefix to an informal URL.
  """
  if re.match(r"\w+:", url):           #Has prefix already, leave it alone.
    return url
  else:
    if re.match(r"(\w|-|%)+@", url):   #Starts like an email address.
      return "mailto:" + url
    elif url[:3] == 'ftp':             #Starts like an FTP address.
      return "ftp://" + url
    else:                              #Assume it's a WWW address.
      return "http://" + url
