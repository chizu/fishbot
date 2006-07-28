#!/usr/bin/python
"""!s - Regular expression substitution,
optionally uses the full Perl regexp engine.
Usage: !s/<select>/<replace>/<options>"""
import re,sys,os,string,difflib
import fishapi

perl = False

def bang(pipein, arguments, event):
    # This regexp is to split correctly on only unescaped / slashes like
    # 'asjdf/as[ad/c]df/as\/df' needs.
    # Returns ['asjdf', 'as[ad/c]df', 'as\\/df']
    unescaped_slash = re.compile(r"(?<!\\)(?<!\[)/(?!.?\])")
    if len(unescaped_slash.split(arguments)) == 4:
        # Assumed to start with s/
        (pattern, repl, options) = unescaped_slash.split(arguments)[1:]
        # Number of lines to search
        if re.search('([1-9])', options):
            lines = int(re.search('([1-9])', options).group(0)) + 1
        else:
            lines = 2
        # Search globally, or just the user executing the command
        if 'g' in options:
            search_domain = string.join([i[4] for i in fishapi.backend.last(event.target(), lines)[1:]], "\n")
        else:
            search_domain = string.join([i[4] for i in fishapi.backend.last(event.source(), lines)[1:]], "\n")
        print search_domain
        # Build the perl command
        if perl:
            perl_command = 'perl';
            perl_command += " -e '$pattern = \"%s\";'" % pattern
            perl_command += " -e '$repl = \"%s\";'" % repl
            #perl_command += " -e '$options = \"%s\";'" % options
            perl_command += " -e '$result = \"%s\";'" % search_domain
            perl_command += " -e '$result =~ s/$pattern/$repl/g;'"
            perl_command += " -e 'print $result;'"
            # Return only changed lines
            print perl_command
            result = os.popen(perl_command).readlines()
            returned = []
            for n in range(len(result)):
                if result[n] != search_domain[n]:
                    returned.append(result[n])
            return (returned, None)
        # Without perl, do some simple stuff anyways with python
        else:
            try:
                return ("%s meant to say: %s" % (fishapi.getnick(event.source()), re.sub(pattern, repl, search_domain)), None)
            except:
                raise
    return ("Invalid regular expression (check for missing /'s)", None)
