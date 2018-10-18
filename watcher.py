#!/usr/bin/python3
import shlex
import subprocess
import time
import sys
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    directory_to_watch = ''
    command_array = []

    def __init__(self, directory, exclude, command):
        self.directory_to_watch = directory
        self.files_to_exclude = exclude
        self.observer = Observer()
        self.command_array = command

    def run(self):
        event_handler = DirChangedHandler()
        event_handler.setCommand(self.command_array)
        event_handler.setExclude(self.files_to_exclude)
        self.observer.schedule(
            event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print ('Error')

        self.observer.join()


class DirChangedHandler(FileSystemEventHandler):

    process = None
    command = None
    exclude = None

    def setExclude(self, excludePattern):
        self.exclude = re.compile(excludePattern)

    def setCommand(self, command):
        self.command = command
        self._runCommandOnFileChange('')

    def _runCommandOnFileChange(self, file):
        if (self.process != None):
            self.process.kill()
        if (file != ''):
            print('\n')
            print('### FILE ', file, ' CHANGED')
            print('\n')

        self.process = subprocess.Popen(self.command)

    def _skipChange(self, file):
        return self.exclude.match(file)

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            if (not self._skipChange(event.src_path)):
                self._runCommandOnFileChange(event.src_path)

        elif event.event_type == 'modified':
            if (not self._skipChange(event.src_path)):
                self._runCommandOnFileChange(event.src_path)

        return event.src_path


if __name__ == '__main__':
    print(sys.argv)

    directoy = '.'
    exclude = None
    offset = 1
    while offset + 2 < len(sys.argv):
        if sys.argv[offset] in ['--directoy', '-d']:
            directoy = sys.argv[offset + 1]
            offset += 2
        elif sys.argv[offset] in ['--exclude', '-e']:
            exclude = sys.argv[offset + 1]
            offset += 2
        else:
            break

    if (offset + 1 >= len(sys.argv)):
        print(
            '\nUsage:\n ', sys.argv[0], '<directory> [OPTIONS] <command> [command parameter]')
        print('\nOptions:')
        print('    -d, --directoy <watch directoy>          default is current dir')
        print('    -e, --exclude  <exclude reg exp>         default ist no exclude')
        exit(1)

    w = Watcher(directoy, exclude, sys.argv[offset:])
    w.run()
