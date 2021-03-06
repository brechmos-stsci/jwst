"""
Various utilities to handle running Steps from the commandline.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

# import cProfile
import io
import os
import os.path
import textwrap
from astropy.extern import six

from . import config_parser
from . import log
from . import Step
from . import utilities


built_in_configuration_parameters = [
    'debug', 'logcfg', 'verbose'
    ]


def _print_important_message(header, message, no_wrap=None):
    print(u'-' * 70)
    print(textwrap.fill(header))
    print(textwrap.fill(
        message, initial_indent='    ', subsequent_indent='    '))
    if no_wrap:
        print(no_wrap)
    print(u'-' * 70)


def _get_config_and_class(identifier):
    """
    Given a file path to a config file or Python module path, return a
    Step class and a configuration object.
    """
    if os.path.exists(identifier):
        config_file = identifier
        config = config_parser.load_config_file(config_file)
        step_class, name = Step._parse_class_and_name(
            config, config_file=config_file)
    else:
        try:
            step_class = utilities.import_class(identifier, Step)
        except (ImportError, AttributeError, TypeError):
            raise ValueError(
                '{0!r} is not a path to a config file or a Python Step '
                'class'.format(identifier))
        # Don't validate yet
        config = config_parser.config_from_dict({})
        name = None
        config_file = None

    return step_class, config, name, config_file


def _build_arg_parser_from_spec(spec, step_class, parent=None):
    """
    Given a configspec, sets up an argparse argument parser that
    understands its arguments.

    The \"path\" in the configspec becomes a dot-separated identifier
    in the commandline arguments.  For example, in the following
    configfile::

        [foo]
          [[bar]]
             baz = 2

    The "baz" variable can be changed with ``--foo.bar.baz=42``.
    """
    import argparse

    # It doesn't translate the configspec types -- it instead
    # will accept any string.  However, the types of the arguments will
    # later be verified by configobj itself.
    parser = argparse.ArgumentParser(
        parents=[parent],
        description=step_class.__doc__)

    def build_from_spec(subspec, parts=[]):
        for key, val in subspec.items():
            if isinstance(val, dict):
                build_from_spec(val, parts + [key])
            else:
                comment = subspec.inline_comments.get(key) or ''
                comment = comment.lstrip('#').strip()
                argument = "--" + ".".join(parts + [key])
                if argument[2:] in built_in_configuration_parameters:
                    raise ValueError(
                        "The Step's spec is trying to override a built-in "
                        "parameter {0!r}".format(argument))
                parser.add_argument(
                    "--" + ".".join(parts + [key]),
                    type=str, help=comment, metavar='')
    build_from_spec(spec)

    parser.add_argument(
        'args', nargs='*', help='arguments to pass to step')

    return parser


class FromCommandLine(unicode):
    """
    We need a way to distinguish between config values that come from
    a config file and those that come from the commandline.  For
    example, configfile paths must be resolved against the location of
    the config file.  Commandline paths must be resolved against the
    current working directory.  By setting all commandline overrides
    as instances of this class, we can later (in `config_parser.py`)
    use isinstance to see where the values came from.
    """
    pass


def _override_config_from_args(config, args):
    """
    Overrides any configuration values in `config` with values from the
    parsed commandline arguments `args`.
    """
    def set_value(subconf, key, val):
        root, sep, rest = key.partition('.')
        if rest:
            set_value(subconf.setdefault(root, {}), rest, val)
        else:
            val, comment = config._handle_value(val)
            subconf[root] = FromCommandLine(val)

    for key, val in vars(args).items():
        if val is not None:
            set_value(config, key, val)


def step_from_cmdline(args, cls=None):
    """
    Create a step from a configuration file.

    Parameters
    ----------
    args : list of str
        Commandline arguments

    cls : Step class
        The step class to use.  If none is provided, the step

    Returns
    -------
    step : Step instance
        If the config file has a `class` parameter, or the commandline
        specifies a class, the return value will be as instance of
        that class.

        Any parameters found in the config file or on the commandline
        will be set as member variables on the returned `Step`
        instance.
    """
    import argparse
    parser1 = argparse.ArgumentParser(
        description="Run an stpipe Step or Pipeline",
        add_help=False)
    if cls is None:
        parser1.add_argument(
            "cfg_file_or_class", type=str, nargs=1,
            help="The configuration file or Python class to run")
    else:
        parser1.add_argument(
            "--config-file", type=str,
            help="A configuration file to load parameters from")
    parser1.add_argument(
        "--logcfg", type=str,
        help="The logging configuration file to load")
    parser1.add_argument(
        "--verbose", "-v", action="store_true",
        help="Turn on all logging messages")
    parser1.add_argument(
        "--debug", action="store_true",
        help="When an exception occurs, invoke the Python debugger, pdb")
    known, _ = parser1.parse_known_args(args)

    try:
        if cls is None:
            step_class, config, name, config_file = \
                _get_config_and_class(known.cfg_file_or_class[0])
        else:
            config_file = known.config_file
            config = config_parser.load_config_file(config_file)
            step_class, name = Step._parse_class_and_name(
                config, config_file=config_file)
            step_class = cls

        log_config = None
        if known.verbose:
            if known.logcfg is not None:
                raise ValueError(
                    "If --verbose is set, a logging configuration file may "
                    "not be provided")
            log_config = io.BytesIO(log.MAX_CONFIGURATION)
        elif known.logcfg is not None:
            if not os.path.exists(known.logcfg):
                raise IOError(
                    "Logging config {0!r} not found".format(known.logcfg))
            log_config = known.logcfg

        if log_config is not None:
            try:
                log.load_configuration(log_config)
            except Exception as e:
                raise ValueError(
                    "Error parsing logging config {0!r}:\n{1}".format(
                        log_config, e))
    except Exception as e:
        if six.PY2:
            _print_important_message(
                "ERROR PARSING CONFIGURATION:", unicode(e))
        else:
            _print_important_message(
                "ERROR PARSING CONFIGURATION:", str(e))
        parser1.print_help()
        raise

    debug_on_exception = known.debug

    spec = step_class.load_spec_file(preserve_comments=True)

    parser2 = _build_arg_parser_from_spec(spec, step_class, parent=parser1)

    args = parser2.parse_args(args)
    if cls is None:
        del args.cfg_file_or_class
    else:
        del args.config_file
    del args.logcfg
    del args.verbose
    del args.debug
    positional = args.args
    del args.args

    _override_config_from_args(config, args)

    try:
        step = step_class.from_config_section(
            config, name=name, config_file=config_file)
    except config_parser.ValidationError as e:
        # If the configobj validator failed, print usage information.
        if six.PY2:
            _print_important_message("ERROR PARSING CONFIGURATION:", unicode(e))
            parser2.print_help()
            raise ValueError(unicode(e))
        else:
            _print_important_message("ERROR PARSING CONFIGURATION:", str(e))
            parser2.print_help()
            raise ValueError(str(e))

    # Always have an output_file set on the outermost step
    if step.output_file is None:
        if len(positional):
            step.output_file = os.path.abspath(os.path.splitext(
                positional[0])[0] + "_{0}.fits".format(step.name))

    if len(positional):
        step.set_input_filename(positional[0])

    log.log.info("Hostname: {0}".format(os.uname()[1]))
    log.log.info("OS: {0}".format(os.uname()[0]))

    try:
        profile_path = os.environ.pop("JWST_PROFILE", None)
        if profile_path:
            import cProfile
            cProfile.runctx("step.run(*positional)", globals(), locals(), profile_path)
        else:
            step.run(*positional)
    except Exception as e:
        import traceback
        lines = traceback.format_exc()
        if six.PY2:
            _print_important_message(
                "ERROR RUNNING STEP {0!r}:".format(step_class.__name__),
                unicode(e), lines)
        else:
            _print_important_message(
                "ERROR RUNNING STEP {0!r}:".format(step_class.__name__),
                str(e), lines)

        if debug_on_exception:
            import pdb
            pdb.post_mortem()
        else:
            raise

    return step


def step_script(cls):
    import sys

    assert issubclass(cls, Step)

    return step_from_cmdline(sys.argv[1:], cls=cls)
