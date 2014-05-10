# -*- coding: utf-8 -*-

import os
import os.path
import glob

import sublime, sublime_plugin

class AnyFileFinderCommand(sublime_plugin.WindowCommand):
        """
        Sublime text 3 WindowCommand plugin
        Is the plugin, open and select the file from the file system.
        """

        def __init__(self, window):
                sublime_plugin.WindowCommand.__init__(self, window)

                self.APPEND_ITEM_PREFIX = ["../"]
                self.APPEND_ITEM_SUFFIX = ["~", "/"]
                self.items = [] # panel list
                self.highlight_abspath = None # highlight filesystem abspath

        def on_select(self, index):
                """
                Quick panel on_done event
                @see sublime.Window.show_input_panel
                @param index Panel list of selected numbers

                """
                #print ("on_select: " + str(index))

                item = self.items[index]
                if item[:1] == "/":
                        #print ("on_select: /")
                        item = os.path.expanduser("/")
                        self.update_highlight(item)
                        self.show_quick_panel()
                        return

                if item[:1] == "~":
                        #print ("on_select: ~")
                        item = os.path.expanduser("~")
                        self.update_highlight(item)
                        self.show_quick_panel()
                        return

                if item[:1] == "../":
                        #print ("on_select: ../")
                        find_path = "%s/%s" % (self.highlight_abspath, item)
                        self.update_highlight(find_path)
                        self.show_quick_panel()
                        return

                # concat file path
                find_path = "%s/%s" % (self.highlight_abspath, item)

                if os.path.isfile(find_path) is True:
                        #print ("on_select: open file=" + find_path)
                        self.window.open_file(find_path)

                        return

                if os.path.isdir(find_path) is True:
                        #print ("on_select: open directory=" + find_path)
                        self.update_highlight(find_path)
                        self.show_quick_panel()
                        return

                return

        def on_highlight(self, index):
                """
                Quick panel on_highlight event
                @see sublime.Window.show_input_panel
                @param index Panel list of selection numbers
                """
                #print ("### on_highlight#" + str(index))

                def _format(path):
                        if os.path.islink(path) is True:
                                msg = "path: %s, realpath: %s" % (path, os.path.realpath(path))
                        else:
                                msg = "path: %s" % (os.path.realpath(path))

                        return msg

                # --
                item = self.items[index]

                if item == "~":
                        path = os.path.expanduser("~")
                elif item == "/":
                        path = "/"
                elif item == "../":
                        path = os.path.dirname(self.highlight_abspath)
                else:
                        path = "%s/%s" % (self.highlight_abspath, item)

                msg = _format(path)
                
                #print ("msg: " + msg)

                sublime.status_message(msg)


        def get_display(self):
                ret = []
                for i, x in enumerate(self.items):
                        ret.append("%d: %s : %s" % (i, x, "aaa"))

                return ret



        def highlight_find(self):
                """Search from the file path of the currently selected
                """
                return os.listdir(self.highlight_abspath)

        def update_highlight(self, path):
                """Update the file path of the currently selected
                @param path Panel list of selection file path
                """
                self.highlight_abspath = os.path.normpath(path)
                #print ("self.highlight_abspath: " + self.highlight_abspath)
                #print ("listdir: " + str(os.listdir(self.highlight_abspath)))
                self.items = self.APPEND_ITEM_PREFIX + self.highlight_find() + self.APPEND_ITEM_SUFFIX

        def show_quick_panel(self):
                """Run the sublime.window.show_quick_panel in the callback-style
                """
                sublime.set_timeout(lambda: self.window.show_quick_panel(
                        self.items,
                        self.on_select,
                        sublime.MONOSPACE_FONT,
                        -1,
                        self.on_highlight
                        ), 1)


        def run(self):
                """
                At the entrance of the plug-ins
                @see sublime_plugin.WindowCommand.run()
                """
                # active view file path
                highlight_dirname = os.path.dirname(self.window.active_view().file_name())
                self.update_highlight(highlight_dirname)

                sublime.status_message(self.highlight_abspath)
                self.show_quick_panel()
                
                return
