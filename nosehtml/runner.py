import nose
import nosehtml
import StringIO

import os
folder      = os.path.expanduser("~/Libs/python/Reactive")
my_template = os.path.expanduser("~/Desktop/html/nose_template.html")
my_report   = os.path.expanduser("~/Desktop/report2.html")

if __name__ == '__main__':
    # create a new instance of the plugin class
    output = StringIO.StringIO()
    my_plugin = nosehtml.HtmlReport(alternative_stream=output)

    # the following call works with other nose plugins
    result = nose.run( argv=['-w', folder, 
                             "-v",
                             "--with-html-report",
                             "--html-template-file", my_template,
                             ],
                             #"--html-report-file", my_report], 
                       #testRunner=nose.core.TextTestRunner(output), 
                       plugins=[my_plugin])
    contents = output.getvalue()
    output.close()
    #print result, type(result)
    print "=" * 50
    print contents
