

# Robot Framework 2.6 Preview Releases #

**NOTE:** [Robot Framework 2.6](ReleaseNotes26.md) final was released on Tuesday 2011-07-26. These pre-release notes are kept in a separate page as a reference.

Robot Framework 2.6 is a new major release with loads of bigger
and smaller enhancements and bug fixes. Before the final release there
will be some alpha, beta, and release candidate releases in order

  * to make the already implemented features available to users,
  * to get feedback about the new features and enhancements, and
  * to allow users to test the new version on their environments.

Please submit possible bugs you encounter with the preview releases to
the [issue tracker](http://code.google.com/p/robotframework/issues/list)
and send general comments and questions to the [mailing lists](MailingLists.md).

## Downloads and installation ##

The latest pre-release is always available on the
[download page](http://code.google.com/p/robotframework/downloads/list).

You can follow the normal [installation instructions](Installation.md)
when installing RF 2.6 releases. If you have an earlier Robot version installed
it should be safe to install over it. Removing the old version first is always
safer, though, and should always be done if installation fails or running
tests always fails mysteriously.

## Compatibility with RIDE and Mabot ##

Robot Framework 2.6 should be fully compatible with the earlier
[RIDE](http://code.google.com/p/robotframework-ride/) and
[Mabot](http://code.google.com/p/robotframework-mabot/) releases.

## Compatibility with outputs generated with RF 2.5 ##

Robot Framework 2.6 can read and process outputs generated by
2.5.x. releases. This allows testing the enhanced log and report (see
below) also without executing tests using 2.6. All you need to do is
getting the output file (such as `ouput.xml`) and generating logs and
reports based on it with `rebot`.

**NOTE:**
> Processing split outputs (generated when using `--splitoutputs` option)
> is not supported in relase candidate 1 or earlier.

## Compatibility with IronPython ##

Unfortunately Robot Framework 2.6.0 does not work with IronPython.
You can use Robot Framework 2.5.7 with IronPython until we manage
work around the incompatibilities.

# Most important enhancements and new features #

## Better log file performance ##

The biggest enhancement in this release is making the performance
of the log files better when the amount of test cases and test data
increases ([issue 360](https://code.google.com/p/robotframework/issues/detail?id=360)).

This enhancement is implemented so that when you open the log file it is
not loaded into the browsers memory fully but generated dynamically using
Javascript (and wonderful [jQuery](http://jquery.com/)) as you drill down to
more details. This both makes the log files' size on a disk much smaller
(in one case a log file that used to be 120MB is now 9MB) and also reduces
browsers' memory consumption dramatically (the earlier log file performed
flawlessly on a browser).

Creating the log files dynamically allows also interesting enhancements
in the future. Ideas we have had include test cases search and setting
log level. In RF 2.6 the log files should look pretty much like the ones
we all have got used to in previous releases, though.

We are highly interested in feedback related the new log files. We are
especially looking forward for comments about the performance with large
test data sets but let us also know if something in the logs does not work
as well as it used to. You can add comments to [issue 360](https://code.google.com/p/robotframework/issues/detail?id=360) directly or send
them to the [mailing lists](MailingLists.md).

## Transparent log splitting ##

A common problem when the amount of test cases increases is that log
files gets too big. They do not open nicely into browsers anymore and
if they are on a remote machine downloading them takes too much time.

In RF 2.5 and earlier this problem was solved with a functionality to
split both log files and output files (`--splitoutputs` option) from a
predefined level. This
[functionality was removed](#Splitting_outputs_is_not_supported_anymore.md)
early during 2.6 development because it never worked that well and it
was incompatible with the new log generation system discussed above.

Although the new logs are orders of magnitude smaller than
earlier, some log splitting functionality was still needed with very
large test suites. The new approach introduced in RF 2.6 (beta 3) is
splitting the log into smaller files that can be loaded dynamically
when needed. This approach has two huge benefits:

  * Main log file size stays small (log from Robot Framework's own acceptance tests with 2000+ tests is only 1.6 MB).
  * Because the data is loaded dynamically, users do not see any difference compared to the situation where logs are not split.

The main drawback is that the overall size taken by the log file
increases. In practice this should not matter too much because not all
the data needs to be loaded into a browser, disk space is pretty cheap,
and the logs in 2.6 are otherwise so small compared to the old logs.

Another drawback is that copying log files or otherwise manipulating
them after the execution gets a bit more complicated because you have
lot of small files. Technically data from each test is written into a
separate Javascript file and the number of files grows when the number
of tests grows. The files have name in format `'log-42.js'` where `'log'`
changes depending on the actual name of the log file and `'42'` is a
growing index.

The new mechanism is transparent for users viewing the log file but it
still needs to be enabled with `--splitlog` option when tests are run
or results post-processed with `rebot`.

## Enhanced and better performing report ##

In RF 2.6 also report files are generated dynamically and are thus
smaller and have better performance than earlier. In addition to that,
reports have also got some new functionality.

The smaller size (in one case from 9MB to 0.4MB) and faster opening
time are due to reports not showing test cases automatically but instead
having an easy way to select what you actually want to see. Old test details
by suite and test details by tag tables have been removed and replaced
with dynamically generated tables that show the same information ([issue 849](https://code.google.com/p/robotframework/issues/detail?id=849)).
In addition to these views being accessible from the statistics table
like the removed tables in earlier releases, you also have drop-down menus
where you can select which suite or tag to show.

A totally new functionality in reports is having a view where
all tests or all critical tests can be seen ([issue 863](https://code.google.com/p/robotframework/issues/detail?id=863)). Tests in these
views are sorted so that failed tests are first (similarly as when viewing
tests by tag) so it is very easy to see all failed or all failed critical
tests in one place. These views are also accessible from the statistics table.

We are also highly interested in comments about the new reports. Both comments
about the new features and about the performance are appreciated and can be
submitted to relevant issues or sent to the [mailing lists](MailingLists.md).

**TODO:** Add a screenshot here when we have taken one for the User Guide.

## Keyword teardown functionality ##

Robot Framework has always had test and suite level setups and teardowns,
but nowadays also individual user keywords can have their own teardowns
([issue 711](https://code.google.com/p/robotframework/issues/detail?id=711)). The mechanism of this new feature is very simple, the keyword
teardown is executed both when the keyword passes and when it fails.

Keyword teardowns allows, for example, splitting a large test teardown
into more fine-grained teardowns that are executed closer to the activity
that needs to be cleaned up. Another good use case is with test templates
(a new feature in [RF 2.5](ReleaseNotes25.md)) where
the system should be in a known state after every repeated step.

Using keyword teardown and test templates is illustrated by the example
below. It shows a different approach to create invalid login cases from the
[SeleniumLibrary demo](http://code.google.com/p/robotframework-seleniumlibrary/wiki/Demo):

```
    ***Settings***
    Test Setup       Open login page
    Test Template    Login with invalid credentials should fail
    Test Teardown    Close browser
    Resource         common_resource.txt

    ***Test Cases***
    Invalid login
        ${VALID USER}    invalid
        invalid          ${VALID PASSWORD}
        invalid          invalid
        ${VALID USER}    ${EMPTY}
        ${EMPTY}         ${VALID PASSWORD}
        ${EMPTY}         ${EMPTY}

    ***Keywords***
    Login with invalid credentials should fail
        [Arguments]    ${username}    ${password}
        Input user name    ${username}
        Input password     ${password}
        Submit credentials
        Welcome page should be open
        [Teardown]    Navigate to login page
```

Notice that keyword teardown functionality is currently not supported
by [RIDE](http://code.google.com/p/robotframework-ride/).

## New logging APIs and other logging enhancements ##

Robot Framework 2.6 has its own Python API for logging
(`robot.api.logger` module) ([issue 339](https://code.google.com/p/robotframework/issues/detail?id=339)) and it also supports Python's
standard [logging](http://docs.python.org/library/logging.html) module
([issue 455](https://code.google.com/p/robotframework/issues/detail?id=455)). These APIs make both make logging cleaner than using the
standard output and also provide nice functionality such as accurate
timestamps. They are explained more thoroughly, and with examples, in
the
[User Guide](http://robotframework.googlecode.com/hg/doc/userguide/RobotFrameworkUserGuide.html#public-logging-api).

Another logging related enhancement is that libraries can embed
accurate timestamp into the messages logged through stdout/stderr
([issue 456](https://code.google.com/p/robotframework/issues/detail?id=456)). Python based libraries are probably better of using the
new logging APIs, but this enhancement adds timestamp support also for
Java based libraries as well as for libraries that utilize the
[remote interface](RemoteLibrary.md).


# Backwards incompatible changes #

## Viewing logs and reports requires a modern browser ##

Logs and reports nowadays use Javascript and CSS styles that only work
well in modern browsers. Firefox 3.5, IE 8, or equivalent is required,
but newer browsers are recommended. Most notable IE 6 and IE 7
are not supported at all.

Newer browsers, such as Firefox 4 and Google Chrome 12, have blazingly
fast Javascript engines and they can easily view even very large log
files. Upgrading your browser may thus be a good idea even if you can open
logs and reports with your old browser.

If your company policy prevents you from upgrading IE or using
alternative browsers, you can always keep on using older Robot
Framework versions.

## Splitting outputs is not supported anymore ##

The earlier explained big
[log file performance enhancements](#Better_log_file_performance.md)
unfortunately completely broke the old output splitting functionality
([issue 861](https://code.google.com/p/robotframework/issues/detail?id=861)). Fixing splitting so that it would work like it worked
earlier would have been a really big task.

Outputs have been split mainly to make log files smaller by splitting
them into pieces that should not grow too big. Because the old
approach never worked too well (see e.g. [issue 386](https://code.google.com/p/robotframework/issues/detail?id=386) and [issue 862](https://code.google.com/p/robotframework/issues/detail?id=862)), a
decision was made to rather implement new
[log splitting approach](#Transparent_log_splitting.md).

In RF 2.6 using `--splitoutputs` option gives you a warning and in RF
2.7 the option will be removed altogether. New `--splitlog` option
should be used instead.

## Summary reports were removed ##

As explained above, reports in Robot Framework 2.6
[do not have tests open when you open them](#Enhanced_and_better_performing_report.md)
and in practice they look a lot like the old summary reports. Because reports
are generated dynamically, their size is also very small.

Because summary reports did not provide any value anymore they were
removed ([issue 864](https://code.google.com/p/robotframework/issues/detail?id=864)).

## `testdoc.py` tool does not work ##

Unfortunatley [testdoc.py tool](http://code.google.com/p/robotframework/wiki/TestDataDocumentationTool) is not compatible with RF 2.6 ([issue 908](https://code.google.com/p/robotframework/issues/detail?id=908)). Hopefully this useful tool can be fixed already in 2.6.1.

## Many internal APIs have changed ##

There are lot of internal changes in a big release like this and some of the changes may affect libraries or tools that are dependent on the internal APIs. The most important changes are listed in [issue 907](https://code.google.com/p/robotframework/issues/detail?id=907).

## Other backwards incompatible changes ##

All potentially backwards incompatible issues are
[labeled with `bwic` label in the issue tracker](http://code.google.com/p/robotframework/issues/list?can=1&q=target%3D2.6+label%3Dbwic).
Why these changes may cause problems will be explained thoroughly
later when these release notes are improved.

# Deprecated features #

There are not too many deprecated features in this release, but the ones that
have been deprecated are
[labeled with `depr` label in the issue tracker](http://code.google.com/p/robotframework/issues/list?can=1&q=target%3D2.6+label%3Ddepr).
Why these features were deprecated will be explained thoroughly
later when these release notes are improved.


# Acknowledgements #

Very big thanks to the
[JSXGraph](http://sourceforge.net/projects/jsxgraph)
project for creating and releasing the
[JSXCompressor](http://jsxgraph.uni-bayreuth.de/wp/2009/09/29/jsxcompressor-zlib-compressed-javascript-code)
module.
One reason new logs and reports are so small is that all larger
strings are compressed using the [zlib](http://zlib.org) algorithm
and then uncompressed on-demand in the browser using this great module.

Special thanks to Alfred Wassermann for making JSXCompressor available
also under the Apache 2 license so that it was easier for us to
include it.

Big thanks also to all [jQuery](http://jquery.com/) developers for
making Javascript development a joy.

Thanks to Imran for providing a great patch to [issue 897](https://code.google.com/p/robotframework/issues/detail?id=897) and for actively
testing the preview releases. Thanks also to all others who have tested
alphas, betas, and release candidates!

# Robot Framework 2.6 Alpha 1 #

The first RF 2.6 pre-release was releases on 2011-06-13. List of all
issues included into it can be found below. We are eagerly waiting for
comments!!

| **ID** | **Type** | **Priority** | **Summary** |
|:-------|:---------|:-------------|:------------|
| [Issue 360](https://code.google.com/p/robotframework/issues/detail?id=360) | Enhancement | Critical     | Possibility to view log file without loading it into memory fully |
| [Issue 861](https://code.google.com/p/robotframework/issues/detail?id=861) | Defect   | High         | Splitting outputs is not compatible with new logs and must be removed |
| [Issue 339](https://code.google.com/p/robotframework/issues/detail?id=339) | Enhancement | High         | Provide logging facility for developers of Robot Framework Extension Libraries |
| [Issue 711](https://code.google.com/p/robotframework/issues/detail?id=711) | Enhancement | High         | Keyword teardown functionality |
| [Issue 849](https://code.google.com/p/robotframework/issues/detail?id=849) | Enhancement | High         | It should be possible to select tests that are shown in report to make its size smaller |
| [Issue 863](https://code.google.com/p/robotframework/issues/detail?id=863) | Enhancement | High         | Not always easy to see all failed tests and all failed critical tests in report |
| [Issue 822](https://code.google.com/p/robotframework/issues/detail?id=822) | Defect   | Medium       | Cannot import two libraries with same name using physical path |
| [Issue 827](https://code.google.com/p/robotframework/issues/detail?id=827) | Defect   | Medium       | Dynamic keywords ignored if getting documentation or arguments fails |
| [Issue 832](https://code.google.com/p/robotframework/issues/detail?id=832) | Defect   | Medium       | Execution crashes if listener method `message` fails repeatingly |
| [Issue 860](https://code.google.com/p/robotframework/issues/detail?id=860) | Defect   | Medium       | Dry-run mode fails if embedded arguments contain dynamically set variables |
| [Issue 109](https://code.google.com/p/robotframework/issues/detail?id=109) | Enhancement | Medium       | `Should (Not) Be Equal As Numbers` and `Convert To Number` should take precision as an optional argument |
| [Issue 455](https://code.google.com/p/robotframework/issues/detail?id=455) | Enhancement | Medium       | Support for Python standard `logging` module |
| [Issue 736](https://code.google.com/p/robotframework/issues/detail?id=736) | Enhancement | Medium       | Uncatchable syntax errors should be turned into normal failures when possible |
| [Issue 767](https://code.google.com/p/robotframework/issues/detail?id=767) | Enhancement | Medium       | avoid callling sys.exit() when running Robot from a test-driver |
| [Issue 807](https://code.google.com/p/robotframework/issues/detail?id=807) | Enhancement | Medium       | It should be possible to disable Remote servers' `Stop Remote Server` keyword |
| [Issue 808](https://code.google.com/p/robotframework/issues/detail?id=808) | Enhancement | Medium       | `Should (Not) Be Equal As Integers` and `Convert To Integer` should accept also hex, octal and binary numbers |
| [Issue 821](https://code.google.com/p/robotframework/issues/detail?id=821) | Enhancement | Medium       | Remove `critical` attribute from opening `<test>` tag in XML |
| [Issue 829](https://code.google.com/p/robotframework/issues/detail?id=829) | Enhancement | Medium       | Add option to disable output.xml |
| [Issue 835](https://code.google.com/p/robotframework/issues/detail?id=835) | Enhancement | Medium       | Integer variables should accept `0b` (binary), `0o`, (octal) and `0x` (hex) prefixes like `${0xFF}` |
| [Issue 836](https://code.google.com/p/robotframework/issues/detail?id=836) | Enhancement | Medium       | `Convert To Binary/Octal/Hex` keywords to `BuiltIn` library |
| [Issue 859](https://code.google.com/p/robotframework/issues/detail?id=859) | Enhancement | Medium       | Additional listener attributes to differentiate suite/test setup/teardown from other keywords. |
| [Issue 844](https://code.google.com/p/robotframework/issues/detail?id=844) | Enhancement | Medium       | Possibility to get variable value with default value to be used when it does not exist (`Get Variable Value` keyword) |
| [Issue 506](https://code.google.com/p/robotframework/issues/detail?id=506) | Enhancement | Low          | Remove `deprecated_absolute` argument from `List Directory` keywords |
| [Issue 507](https://code.google.com/p/robotframework/issues/detail?id=507) | Enhancement | Low          | Remove the deprecated `Create File With Encoding` keyword |
| [Issue 680](https://code.google.com/p/robotframework/issues/detail?id=680) | Enhancement | Low          | Allow accessing JVM properties in test data using format %{property.name} |
| [Issue 733](https://code.google.com/p/robotframework/issues/detail?id=733) | Enhancement | Low          | Deprecate old screenshot taking keywords and remove deprecated `log_file_directory` argument and `Set Screenshot Directories` keyword |
| [Issue 834](https://code.google.com/p/robotframework/issues/detail?id=834) | Enhancement | Low          | Integer variables like `${42}` should create `int` type not `long` |
| [Issue 846](https://code.google.com/p/robotframework/issues/detail?id=846) | Enhancement | Low          | Tag stat links should be serialized to XML |
| [Issue 813](https://code.google.com/p/robotframework/issues/detail?id=813) | Documentation | Low          | Document that Python libraries can messages to console using `sys.__stdout__`  |
| [Issue 839](https://code.google.com/p/robotframework/issues/detail?id=839) | Documentation | Low          | Online version of the Quick Start Guide should explain how to get it |
| [Issue 848](https://code.google.com/p/robotframework/issues/detail?id=848) | Documentation | Low          | Document that if same variable is given multiple times from CLI the last value takes effect |
| [Issue 850](https://code.google.com/p/robotframework/issues/detail?id=850) | Documentation | Low          | Document how to use list variables with length related keywords. |

Altogether 32 issues.

# Robot Framework 2.6 Beta 1 #

The most important fixes in this release are related to enhancing
performance of the new [logs](#Better_log_file_performance.md) and
[reports](#Enhanced_and_better_performing_report.md) with larger data
sets. The table below lists other enhancements and fixes included
into this release.

RF 2.6 beta 1 was releases on Thursday 2011-06-23. All kind of
comments, especially related to the performance and usability of the
new logs and reports, are highly appreciated!

| **ID** | **Type** | **Priority** | **Summary** |
|:-------|:---------|:-------------|:------------|
| [Issue 456](https://code.google.com/p/robotframework/issues/detail?id=456) | Enhancement | Medium       | Possibility to get accurate timestamp when logging messages through stdout |
| [Issue 802](https://code.google.com/p/robotframework/issues/detail?id=802) | Enhancement | Medium       | Command line option `--RunEmptySuite` to allow execution even if there are no tests |
| [Issue 875](https://code.google.com/p/robotframework/issues/detail?id=875) | Enhancement | Medium       | Always visible link from report to log and from log to report |
| [Issue 873](https://code.google.com/p/robotframework/issues/detail?id=873) | Defect   | Low          | Suite name from directory that has '.' in name is parsed wrong |
| [Issue 883](https://code.google.com/p/robotframework/issues/detail?id=883) | Defect   | Low          | Not possible to assign doc or links for combined tag statistics |
| [Issue 307](https://code.google.com/p/robotframework/issues/detail?id=307) | Enhancement | Low          | Paths should not be case-normalized |
| [Issue 877](https://code.google.com/p/robotframework/issues/detail?id=877) | Enhancement | Low          | Always show tag statistics and suite statistics tables in logs an reports |
| [Issue 884](https://code.google.com/p/robotframework/issues/detail?id=884) | Enhancement | Low          | Tag stat link titles should support replaced groups similarly as tag stat link urls |

Altogether 8 issues.

# Robot Framework 2.6 Beta 2 #

The main motivation for this release was fixing compatibility with
[RIDE](http://code.google.com/p/robotframework-ride/)
that beta 1 accidentally broke. The most important new feature is
the support for custom regular expressions when using the embedded
arguments syntax ([issue 854](https://code.google.com/p/robotframework/issues/detail?id=854)).

RF 2.6 beta 2 was releases on Thursday 2011-06-29. All kind of
comments are highly appreciated!

| **ID** | **Type** | **Priority** | **Summary** |
|:-------|:---------|:-------------|:------------|
| [Issue 854](https://code.google.com/p/robotframework/issues/detail?id=854) | Enhancement | Medium       | Regular expression support for embedded argument syntax |
| [Issue 889](https://code.google.com/p/robotframework/issues/detail?id=889) | Documentation | Medium       | Document that Easy Install by default installs latest version even if that is alpha/beta/rc |
| [Issue 891](https://code.google.com/p/robotframework/issues/detail?id=891) | Defect   | Low          | User keyword timeout is not shown in the log |

Altogether 3 issues.

# Robot Framework 2.6 Beta 3 #

This release contains one big enhancement compared to previous RF 2.6
pre-releases and all RF releases in general: transparent log splitting
([issue 898](https://code.google.com/p/robotframework/issues/detail?id=898)). This was the last large issue remaining before the final
release.

RF 2.6 beta 3 was releases on Thursday 2011-07-07. All kind of
comments are highly appreciated!

| **ID** | **Type** | **Priority** | **Summary** |
|:-------|:---------|:-------------|:------------|
| [Issue 898](https://code.google.com/p/robotframework/issues/detail?id=898) | Enhancement | Critical     | Transparent log splitting option |
| [Issue 899](https://code.google.com/p/robotframework/issues/detail?id=899) | Defect   | Medium       | Links from report are not guaranteed to be unique |
| [Issue 864](https://code.google.com/p/robotframework/issues/detail?id=864) | Enhancement | Medium       | Remove summary reports because they are not needed after enhancements to normal reports |

Altogether 3 issues.

# Robot Framework 2.6 Beta 4 #

RF 2.6 beta 4 mainly fixes the `--splitlog` functionality that was
introduced in beta 3 with custom log names. The release was done on
Friday 2011-07-08.

| **ID** | **Type** | **Priority** | **Summary** |
|:-------|:---------|:-------------|:------------|
| [Issue 900](https://code.google.com/p/robotframework/issues/detail?id=900) | Defect   | Medium       | `Run Keyword And Continue On Failure` does not work with user keywords inside FOR loop |

Altogether 1 issue.

# Robot Framework 2.6 Release Candidate 1 #

RF 2.6 RC 1 has some nice enhancements and fixes listed below, but
more importantly it fixes a lot of bigger and smaller problems in the
earlier preview releases. This is the first RF 2.6 release that is
considered to be ready for production use. No more code changes are
planned before the 2.6 final release except for possible bug fixes and
small cleanups.

RF 2.6 RC 1 was released on Friday 2011-07-15. If there are no big
surprises, the final release will be out on next Thursday. All kind of
testing is naturally very highly appreciated at this stage. Findings
can be reported to the [mailing lists](MailingLists.md) and bugs
submitted into the
[issue tracker](http://code.google.com/p/robotframework/issues/list).

| **ID** | **Type** | **Priority** | **Summary** |
|:-------|:---------|:-------------|:------------|
| [Issue 894](https://code.google.com/p/robotframework/issues/detail?id=894) | Defect   | Medium       | Docstrings with non-ASCII characters don't work correctly (unless they are Unicode) |
| [Issue 892](https://code.google.com/p/robotframework/issues/detail?id=892) | Enhancement | Medium       | Messages logged by libraries when they are imported and initialized should go to syslog |
| [Issue 896](https://code.google.com/p/robotframework/issues/detail?id=896) | Enhancement | Medium       | New BuiltIn Keyword "Keywords Should Exist" |
| [Issue 906](https://code.google.com/p/robotframework/issues/detail?id=906) | Defect   | Low          | `metadata` attribute missing from `end_suite` listener method |
| [Issue 905](https://code.google.com/p/robotframework/issues/detail?id=905) | Enhancement | Low          | Add `critical` attribute to `start/end_test` listener methods |
| [Issue 893](https://code.google.com/p/robotframework/issues/detail?id=893) | Documentation | Low          | Document that libraries should communicate with the framework only from main thread |

Altogether 6 issues.

# Robot Framework 2.6 Release Candidate 2 #

Enough problems were found with RC 1 (for example a
[memory leak when running on Jython](http://bugs.jython.org/issue1775))
that a second, and hopefully final, release candidate was needed. In addition
to fixes, this release contains two enhancements listed below.

RF 2.6 RC 2 was released on Friday 2011-07-22. Final release is now targeted
for early next week. All kind of testing is still appreciated and findings
can be reported to the [mailing lists](MailingLists.md) and bugs
submitted into the
[issue tracker](http://code.google.com/p/robotframework/issues/list).

| **ID** | **Type** | **Priority** | **Summary** |
|:-------|:---------|:-------------|:------------|
| [Issue 897](https://code.google.com/p/robotframework/issues/detail?id=897) | Enhancement | Medium       | Add name of the possible template to `start/end_test listener` methods |
| [Issue 909](https://code.google.com/p/robotframework/issues/detail?id=909) | Enhancement | Medium       | Add option to `Collections.Lists Should be Equal` to name indices |

Altogether 2 issues.