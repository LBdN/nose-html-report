import logging
import os
import traceback
from nose.plugins import Plugin

import jinja2 as jinja
from collections import namedtuple

TestReport = namedtuple("TestReport", ['name', 'kind', 'text'])

log = logging.getLogger('nose.plugins.htmlreport')

from path import path
module_path      = path(os.path.dirname(__file__))
html_path        = module_path / 'html'
default_template = html_path / "nose_template.html"


class HtmlReport(Plugin):
    name = 'html-report'
    env_opt = 'NOSE_HTMLREPORT'

    def help(self):
        return "Output HTML report of test status into reportfile (specifiable with --html-report-file"

    def add_options(self, parser, env=os.environ):
        Plugin.add_options(self, parser, env)
        parser.add_option( "--html",
                             action="store_true",
                             default=env.get(self.env_opt),
                             dest="htmlreport",
                             help="output the results as an bootstrap based document")
        parser.add_option("--html-report-file",
                             action="store",
                             default="nose_report.html",
                             dest="report_file",
                             help="File to output HTML report to")
        parser.add_option("--html-template-file",
                             action="store",
                             default="nose_template.html",
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
        if not options.htmlreport: 
            return
        #==
        self.enabled       = True
        self.report_path   = options.report_file
        self.template_path = options.template_file
        self.open_browser  = options.open_browser

    def begin(self):
        """start the report"""
        #load the template_path into a template
        self.env      = jinja.Environment(loader = jinja.FileSystemLoader(html_path))
        self.template = self.env.get_template(self.template_path)
        self.context  = {'tests': []}

    def addSuccess(self, test):
        t= TestReport(
            name = test.id(),
            kind = "Success",
            text = "")
        self.context['tests'].append(t)


    def addError(self, test, err):
        exctype, value, tb = err
        t= TestReport(
            name = test.id(),
            kind = "Error",
            text =  ''.join(traceback.format_exception(exctype, value, tb)))
        self.context['tests'].append(t)
            
    def addFailure(self, test, err):
        exctype, value, tb = err
        t= TestReport(
            name = test.id(),
            kind = "Failure",
            text =  ''.join(traceback.format_exception(exctype, value, tb)))
        self.context['tests'].append(t)

    def finalize(self, result):
        """ Write out report as serialized html """
        html = self.template.render(self.context)
        self.stream.writeln(html)

    def setOutputStream(self, stream):
        # grab for own use
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
