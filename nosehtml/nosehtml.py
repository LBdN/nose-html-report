import os
import traceback
import jinja2 as jinja

from nose.plugins import Plugin


#A few named tuple to package the result
from collections import namedtuple, defaultdict
TestReport   = namedtuple("TestReport", ['name', 'mod_name', 'kind', 'text'])
ImportReport = namedtuple("ImportReport", ['name', 'fp', 'tests'])

#setting a few default path, with the ever so useful path.py
from path import path
module_path      = path(os.path.dirname(__file__))
html_path        = module_path / 'html'
default_template = "nose_template.html"


class HtmlReport(Plugin):
    name = 'html-report'
    env_opt = 'NOSE_HTMLREPORT'

#    def __init__(self,template_path=None):
        #Plugin.__init__(self)
        ##==
        #self.html_path     = None
        #self.template_path = None
        #if template_path:
            #self.html_path, self.template_path = os.path.split(os.path.abspath(template_path))


    def help(self):
        return "Output HTML report of test status into reportfile (specifiable with --html-report-file"

    def options(self, parser, env=os.environ):
        Plugin.options(self, parser, env)
        parser.add_option("--html-report-file",
                             action="store",
                             #default="nose_report.html",
                             dest="report_file",
                             help="File to output HTML report to")
        parser.add_option("--html-template-file",
                             action="store",
                             default= html_path / default_template,
                             dest="template_file",
                             help="jinja template used to output HTML ")
        parser.add_option("--html-open-browser",
                             action="store_true",
                             default=False,
                             dest="open_browser",
                             help="open browser on test run (works only on linux, for now)")
    
    def configure(self, options, config):
        Plugin.configure(self, options, config)
        #==
        if not self.enabled: 
            return
        #==
        self.report_path   = options.report_file
        if options.template_file:
            self.html_path, self.template_path = os.path.split(options.template_file)
        self.open_browser  = options.open_browser

    def begin(self):
        """start the report"""
        #load the template_path into a template
        self.env      = jinja.Environment(loader = jinja.FileSystemLoader(self.html_path))
        try:
            self.template = self.env.get_template(self.template_path)
        except:
            import pdb;pdb.set_trace()
        self.context  = {'imports': [], 'tests': []}

    def addSuccess(self, test):
        t= TestReport(
            name     = test.id(),
            mod_name = test.address()[1],
            kind     = "Success",
            text     = "")
        self.context['tests'].append(t)

    def addError(self, test, err):
        exctype, value, tb = err
        t= TestReport(
            name     = test.id(),
            mod_name = test.address()[1],
            kind     = "Error",
            text     = ''.join(traceback.format_exception(exctype, value, tb)))
        self.context['tests'].append(t)

    def addFailure(self, test, err):
        exctype, value, tb = err
        t= TestReport(
            name     = test.id(),
            mod_name = test.address()[1],
            kind     = "Failure",
            text     = ''.join(traceback.format_exception(exctype, value, tb)))
        self.context['tests'].append(t)

    def finalize(self, result):
        """ Write out report as serialized html """
        #== 
        # we need a bit of postprocessing to group the test per module
        # it could likely be better, but it does the job and I don't
        # performance/speed is critical here.
        mod_dict = defaultdict(list)
        for t in self.context["tests"]:
            mod_dict[t.mod_name].append(t)
        for k,v in mod_dict.iteritems():
            report = ImportReport(name=k, fp=None, tests=v)
            self.context['imports'].append(report)
        del self.context['tests']
        #== 
        html = self.template.render(self.context)
        self.stream.write(html)
        self.stream.close()

    def setOutputStream(self, stream):
        # grab for own use
        if self.report_path: 
            self.stream =  open(self.report_path, "a")
        else:
            self.stream = stream        
        # return dummy stream
        class dummy:
            def write(self, *arg):
                pass
            def writeln(self, *arg):
                pass
            def flush(self, *arg):
                pass
        d = dummy()
        return d
