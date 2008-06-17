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


import sys, os, tempfile
from java.awt import Toolkit, Robot, Rectangle
from javax.imageio import ImageIO
from java.io import File

from robot import utils

class Screenshot:
 
    """This library supports taking full-screen screenshots of the desktop.
    
    The library can be initialized with two arguments: 'default_directory' and 
    'log_file_directory'. If the 'default_directory' is provided, all the 
    screenshots will be saved under that directory by default. If the 
    'default_directory' is not provided, the system temporary directory is used 
    as default.
    'log_file_directory' is used to create relative paths when screenshots are 
    logged. By default, absolute paths are used.
    
    The library depends on standard Java APIs and thus requires a Jython runtime
    environment. The library does not, however, require any specific operating
    system. While the library has been tested on Windows and Linux, any 
    operating system for which the JDK is available, should be sufficient. 
    """
    
    def __init__(self, default_directory=None, log_file_directory=None):
        self.set_screenshot_directories(default_directory, log_file_directory)
    
    def set_screenshot_directories(self, default_directory=None, 
                                 log_file_directory=None):
        """Used to set 'default_directory' and 'log_file_directory'.
        
        See the library documentation for details."""

        if default_directory is None:
            default_directory = tempfile.gettempdir()
        self._default_dir = default_directory
        self._log_file_directory = log_file_directory
        
    
    def save_screenshot(self, basename="screenshot", directory=None):
        """Saves a screenshot with a generated unique name.
        
        The unique name is derived based on the provided basename and directory
        passed in as optional arguments. If a directory is provided, the 
        screenshot is saved under that directory. Otherwise, the 
        'default_directory' set during the library import or by the keyword 'Set 
        Screenshot Directories' is used. If a basename for the screenshot file 
        is provided, a unique filename is determined by appending an underscore
        and a running counter. Otherwise, the basename defaults to 'screenshot'.

        Examples:
        
        | Save Screenshot | mypic | /home/user |
        => /home/user/mypic_1.jpg, /home/user/mypic_2.jpg, ...

        | Save Screenshot | mypic |  |
        => /tmp/mypic_1.jpg, /tmp/mypic_2.jpg, ...

        | Save Screenshot |  |  |
        => /tmp/screenshot_1.jpg, /tmp/screenshot_2.jpg, ...
        """
        
        if directory is None:
            directory = self._default_dir
        file = self._next_unique_filename(directory, basename)
        return self.save_screenshot_to(file)

    def _next_unique_filename(self, directory, basename):
        i = 1
        while True:
            path = os.path.join(directory, "%s_%d.jpg" % (basename, i))
            if not os.path.exists(path):
                return path
            i += 1
    
    def save_screenshot_to(self, path):
        """Saves a screenshot to the specified file.
        
        The directory holding the file must exist or an exception is raised.
        """
        if not os.path.exists(os.path.dirname(path)):
            raise Exception("Path '%s' where to save the sceenshot does not exist" 
                            % path)
        tk = Toolkit.getDefaultToolkit()
        screensize = tk.getScreenSize()
        robot = Robot()
        rectangle = Rectangle(0, 0, screensize.width, screensize.height)
        image = robot.createScreenCapture(rectangle)
        ImageIO.write(image, "jpg", File(path))
        print "Screenshot saved to '%s'" % path
        return path
    
    def log_screenshot(self, basename="screenshot", directory=None, 
                       log_file_directory=None, width="100%"):
        """Takes a screenshot and logs it to Robot Framework's log.
        
        Saves the files as defined in the keyword 'Save Screenshot' and creates 
        a picture to Robot Framework's log. 'directory' defines the directory
        where the screenshots are saved. By default, its value is
        'default_directory', which is set at the library import or with the
        keyword 'Set Screenshot Directories'. 'log_file_directory' is used to
        create relative paths to the pictures. This allows moving the log and
        pictures to different machines and having still working pictures. If 
        'log_file_directory' is not given or set (in the same way as 
        'default_directory' is set), the paths are absolute.
        """

        path = self.save_screenshot(basename, directory)
        if log_file_directory is None:
            log_file_directory = self._log_file_directory
        if log_file_directory is not None:
            path  = utils.get_link_path(path, log_file_directory)
        else:
            path = 'file:///' + path.replace('\\', '/')
        print '*HTML* <a href="%s"><img src="%s" width="%s" /></a>' % (path, path, width)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: " + os.path.basename(sys.argv[0]) + " <file>"
        sys.exit(1)
    Screenshot().save_screenshot_to(sys.argv[1])
