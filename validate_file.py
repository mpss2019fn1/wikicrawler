import argparse
import os


class ValidateFile(argparse.Action):

    def __call__(self, parser, parser_namespace, values, option_string=None):
        path = os.path.abspath(os.path.expanduser(values))

        if not os.path.isfile(path):
            raise argparse.ArgumentError(self, "{0} is not a valid path".format(path))

        if not os.access(path, os.R_OK):
            raise argparse.ArgumentError(self, "Permission denied to read from {0}".format(path))

        setattr(parser_namespace, self.dest, path)
