import logging
import os

from nose.plugins import Plugin

import jinja2 as jinja

log = logging.getLogger('nose.plugins.htmlreport')

class HtmlReport(Plugin):
    name = 'html report'

    def help(self):
        return "Output HTML report of test status into reportfile (specifiable with --html-report-file"

    def add_options(self, parser, env=os.environ):
        Plugin.add_options(self, parser, env)
        parser.add_option("--html-report-file", action="store", default="nose_report.html", dest="report_file", help="File to output HTML report to")
        parser.add_option("--html-template-file", action="store", default="nose_template.html", dest="template_file", help="jinja template used to output HTML ")
    
    def configure(self, options, config):
        Plugin.configure(self, options, config)
        self.conf          = config
        self.report_path   = options.report_file
        self.template_path = options.template_file

    def begin(self):
        """start the report"""
        #load the template_path into a template
        self.env      = jinja.Environment(loader = jinja.FileSystemLoader('/path/to/templates'))
        self.template = self.env.get_template(self.template_path)
        self.context  = {}

    def addSuccess(self, test):
        assert False #TODO

    def addError(self, test, err):
        assert False #TODO
            
    def addFailure(self, test, err):
        assert False #TODO

    def finalize(self, result):
        """ Write out report as serialized html """
        self.template.render(self.context)
