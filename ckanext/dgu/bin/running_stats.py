'''Tool for a script to keep track changes performed on a large number
of objects.

Example:

from running_stats import Stats
stats = Stats()
for package in packages:
    if package.enabled:
        package.delete()
        print stats.add('deleted', package.name)
    else:
        print stats.add('not deleted' package.name)
print stats
> deleted: 30 pollution-uk, flood-regions, river-quality, ...
> not deleted: 70 spending-bristol, ...

'''

import copy
import datetime

class Stats(dict):
    # {category:[values]}
    _init_value = []
    report_value_limit = 150

    def __init__(self, *args, **kwargs):
        self._start_time = datetime.datetime.now()
        super(Stats, self).__init__(*args, **kwargs)

    def _init_category(self, category):
        if not category in self:
            self[category] = copy.deepcopy(self._init_value)

    def add(self, category, value):
        self._init_category(category)
        self[category].append(value)
        return ('%s: %s' % (category, value)).encode('ascii', 'ignore') # so you can log it too

    def report_value(self, category):
        value = self[category]
        number_of_values = len(value)
        value_str = '%i %r' % (number_of_values, value)
        if len(value_str) > self.report_value_limit:
            value_str = value_str[:self.report_value_limit] + '...'
        return (value_str, number_of_values)

    def report(self, indent=1, order_by_title=False, show_time_taken=True):
        lines = []
        indent_str = '\t' * indent
        report_dict = dict()
        for category in self.keys():
            report_dict[category] = self.report_value(category)

        if order_by_title:
            items = sorted(report_dict.iteritems())
        else:
            items = sorted(report_dict.iteritems(),
                           key=lambda x: -x[1][1])

        for category, value_tuple in items:
            value = value_tuple[0]
            lines.append(indent_str + '%s: %s' % (category, value))
        if not self:
            lines = [indent_str + 'None']

        if show_time_taken:
            time_taken = str(datetime.datetime.now() - self._start_time).split('.')[0]
            lines.append(indent_str + 'Time taken (h:m:s): %s' % time_taken)
        return '\n'.join(lines)

    def __repr__(self):
        return self.report()


# deprecated name - kept for backward compatibility
class StatsList(Stats):
    pass


if __name__ == '__main__':
    package_stats = Stats()
    package_stats.add('Success', 'good1')
    package_stats.add('Success', 'good2')
    package_stats.add('Success', 'good3')
    package_stats.add('Success', 'good4')
    package_stats.add('Failure', 'bad1')
    print package_stats
