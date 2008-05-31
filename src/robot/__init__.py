#  Copyright 2008 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


import sys
import os
import glob

if __name__ == '__main__':
    sys.stderr.write("Use 'runner' or 'rebot' for executing.\n")
    sys.exit(252)  # 252 == DATA_ERROR

import pythonpathsetter
from output import Output, SystemLogger
from conf import RobotSettings, RebotSettings
from running import TestSuite
from serializing import RobotTestOutput, RebotTestOutput, SplitIndexTestOutput
from errors import DataError, INFO_PRINTED, DATA_ERROR, FRAMEWORK_ERROR
from variables import init_global_variables
import utils

__version__ = utils.version


def run_from_cli(args, usage):
    options, datasources = _process_arguments(args, usage, 'Robot')
    try:
        suite = run(*datasources, **options)
    except DataError:
        _exit(DATA_ERROR, *utils.get_error_details())
    except KeyboardInterrupt:
        _exit(FRAMEWORK_ERROR, 'Test execution stopped by user')
    except:
        raise
        _exit(FRAMEWORK_ERROR, 'Unexpected error in test execution',
              '\n'.join(utils.get_error_details()))
    else:
        _exit(suite)


def rebot_from_cli(args, usage):
    options, datasources = _process_arguments(args, usage, 'Rebot')
    try: 
        suite = rebot(*datasources, **options)
    except DataError:
        _exit(DATA_ERROR, *utils.get_error_details())
    except KeyboardInterrupt:
        _exit(FRAMEWORK_ERROR, 'Log/report generation stopped by user')
    except:
        _exit(FRAMEWORK_ERROR, 'Unexpected error in log/report generation', 
              '\n'.join(utils.get_error_details()))
    else:
        _exit(suite)

           
def run(*datasources, **options):
    """Executes given Robot data sources with given options.
    
    Data sources are paths to files and directories, similarly as when running
    pybot/jybot from command line. Options are given as keywords arguments and
    their names are same as long command line options without hyphens.
    
    Examples:
    run('/path/to/tests.html')  
    run('/path/to/tests.html', '/path/to/tests2.html', log='mylog.html')
    
    Equivalent command line usage:
    pybot /path/to/tests.html 
    pybot --log mylog.html /path/to/tests.html /path/to/tests2.html
    """
    settings = RobotSettings(options)
    output = Output(settings)
    settings.report_errors(output.syslog)
    init_global_variables(settings, output.syslog)
    _syslog_start_info('Robot', datasources, settings, output.syslog)
    suite = TestSuite(datasources, settings, output.syslog)
    suite.run(output)
    output.syslog.info("Tests executed successfully. Statistics:\n%s"
                       % suite.get_stat_message())
    testoutput = RobotTestOutput(suite, output.syslog, settings)
    output.close1(suite)
    if settings.is_rebot_needed():
        datasources, settings = settings.get_rebot_datasources_and_settings()
        if settings['SplitOutputs'] > 0:
            testoutput = SplitIndexTestOutput(suite, datasources[0], settings)
        else:
            testoutput = RebotTestOutput(datasources, settings, output.syslog)
        testoutput.serialize(settings, output.syslog)
    output.close2()
    return suite


def rebot(*datasources, **options):
    """Creates reports/logs from given Robot output files with given options.
    
    Given input files are paths to Robot output files similarly as when running
    rebot from command line. Options are given as keywords arguments and
    their names are same as long command line options without hyphens.
    
    Examples:
    rebot('/path/to/output.xml')
    rebot('/path/out1.xml', '/path/out2.xml', report='myrep.html', log='NONE')
    
    Equivalent command line usage:
    rebot /path/to/output.xml
    rebot --report myrep.html --log NONE /path/out1.xml /path/out2.xml
    """
    settings = RebotSettings(options)
    syslog = SystemLogger(settings)
    settings.report_errors(syslog)
    _syslog_start_info('Rebot', datasources, settings, syslog)
    testoutput = RebotTestOutput(datasources, settings, syslog)
    testoutput.serialize(settings, syslog, 'Rebot')
    syslog.close()
    return testoutput.suite
    
    
def _syslog_start_info(who, sources, settings, syslog):
    syslog.info(utils.get_full_version(who))
    syslog.info('Settings:\n%s' % settings)
    syslog.info('Starting processing data source%s %s'
                % (utils.plural_or_not(sources), utils.seq2str(sources)))


def _process_arguments(cliargs, usage, who):
    ap = utils.ArgumentParser(usage)
    ppath = who == 'Robot' and 'pythonpath' or None
    try:
        opts, args = ap.parse_args(cliargs, argfile='argumentfile',
                                   unescape='escape', pythonpath=ppath)
    except DataError, err:
        _exit(DATA_ERROR, str(err))
    if opts['help']:
        _print_help(usage)
    if opts['version']:
        _print_version(who)
    return opts, _process_datasources(args, who)


def _process_datasources(sources, who):
    type_ = who == 'Robot' and 'Robot data source' or 'Robot output file'
    if len(sources) == 0:
        _exit(DATA_ERROR, 'No %ss given.' % type_)
    if utils.is_windows:
        temp = []
        for path in sources:
            paths = glob.glob(path)
            if len(paths) > 0:
                temp.extend(paths)
            else:
                temp.append(path)
        sources = temp
    for path in sources:
        if not (os.path.exists(path) or utils.is_url(path)):
            _exit(DATA_ERROR, "%s '%s' does not exist." % (type_, path))
    return sources


def _print_help(usage):
    indent = 26
    escapes = ', '.join(utils.argumentparser.get_escapes())
    escapes = utils.wrap('Available escapes: '+escapes, 80-indent, indent)
    print usage.replace('\\','') % {'ESCAPES': escapes, 'VERSION': utils.version}
    _exit(INFO_PRINTED)

    
def _print_version(who):
    print utils.get_full_version(who)
    _exit(INFO_PRINTED)
    

def _exit(rc_or_suite, error=None, details=None):
    """Exits with given rc or rc from given output. Syslogs error if given.
    
    Exit code is the number of failed critical tests or error number.
      0       - Tests executed and all critical tests passed
      1-250   - Tests executed but returned number of critical tests failed
                (250 means 250 or more failures)
      251     - Help or version info was printed
      252     - Invalid test data or command line arguments
      255     - Internal and unexpected error occurred in the framework itself
    """
    if utils.is_integer(rc_or_suite):
        rc = rc_or_suite
        if error is not None:
            from robot.output import SYSLOG
            if SYSLOG is None:
                SYSLOG = SystemLogger()
            if rc == DATA_ERROR:
                error += '\n\nTry --help for usage information.'
            SYSLOG.error(error)
            if details is not None:
                SYSLOG.info(details)
    else:
        rc = rc_or_suite.critical_stats.failed
        if rc > 250:
            rc = 250
    sys.exit(rc)
