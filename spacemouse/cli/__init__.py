import re


def match_regex_options(device, options):
    flags = re.IGNORECASE if options.ignore_case else 0

    for re_opt in ('devnode', 'manufacturer', 'product'):
        regex = getattr(options, re_opt, None)

        if regex and not re.search(regex, getattr(device, re_opt), flags):
            return False

    return True
