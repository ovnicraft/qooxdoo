#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
#  qooxdoo - the new era of web development
#
#  http://qooxdoo.org
#
#  Copyright:
#    2006-2008 1&1 Internet AG, Germany, http://www.1und1.de
#
#  License:
#    LGPL: http://www.gnu.org/licenses/lgpl.html
#    EPL: http://www.eclipse.org/org/documents/epl-v10.php
#    See the LICENSE file in the project's top-level directory for details.
#
#  Authors:
#    * Sebastian Werner (wpbasti)
#    * Thomas Herchenroeder (thron7)
#
################################################################################

##
#<h2>Module Description</h2>
#<pre>
# NAME
#  genjson.py -- generate json struct, to prepare for generation of demo apps
#
# SYNTAX
#  genjson.py [<copy_target>]
#
#    <copy_target>  -- directory to copy demo .js files to, e.g. 'source/script'
#
# DESCRIPTION
#  - scans for html files of demos (in source/demo)                                                      
#  - creates corresponding entry in JSON jobs file                                                     
#  - copys corresponding .js file in 'script' dir (from source/class/..., for                            
#    the 'View Source' function in DemoBrowser)                                                          
#
#</pre>
##

import sys, os, re, types, shutil

fJSON = "demo.json"


def htmlfiles(rootpath):
    dirwalker = os.walk(rootpath)

    for (path, dirlist, filelist) in dirwalker:
        for filename in filelist:
            if not re.search(r'.*\.html$', filename):
                continue

            yield os.path.join(path,filename)


def main():
    c = {}
    if len(sys.argv)>1:
        c['js_target'] = sys.argv[1]

    source = ""
    build  = ""

    JSON = open(fJSON,"w")
    JSON.write('{\n')

    jsontmplf = open(os.path.join('tool','json.tmpl'),"rU")
    json_tmpl = jsontmplf.read()

    for html in htmlfiles(os.path.join('source','demo')):
        fileH = open(html,"rU")
        selected = False
        for line in fileH:
            if re.search(r'demobrowser\.demo',line):
                selected = True
                break
        if not selected:
            continue
        fileH.seek(0)  # rewind
        category = html.split(os.sep)[2]
        name     = (html.split(os.sep)[3]).split(".")[0]

        print ">>> Processing: %s.%s..." % (category, name)

        # build classname
        clazz  = "demobrowser.demo.%s.%s" % (category,name)
        source = source + ' "source-%s",' % clazz
        build  = build + ' "build-%s",' % clazz

        # copy js source file
        if ('js_target' in c and len(c['js_target']) > 0):
            try:
                os.makedirs(c['js_target'])
            except OSError:
                pass
            shutil.copyfile('source/class/%s.js' % clazz.replace('.','/'), "%s/%s.src.js" % (c['js_target'],clazz))

        # concat all
        currcont = json_tmpl.replace('XXX',clazz)
        JSON.write("%s," % currcont[:-1])
        JSON.write("\n\n\n")

    JSON.write("""  "source" : {
        "run" : [
         %s]
      },\n\n""" % source[:-1] ) 

    JSON.write("""  "build" : {
        "run" : [
         %s]
      }\n}""" % build[:-1] ) 

    JSON.close()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print
    print "  * Keyboard Interrupt"
    sys.exit(1)

