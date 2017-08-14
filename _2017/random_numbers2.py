# https://gist.github.com/jo-tez/7f0a6bad2cd6731d8db16d9542719edb

import agate
import numpy.random as npr
import isodate
from faker import Factory

random_groups = npr.choice(3, 100, p=[.25, .65, .10])

column_names = ['id', 'name', 'hire_date', 'pb', 'salary']

column_types = [
  agate.Number(),
  agate.Text(),
  agate.Date(),
  agate.Number(),
  agate.Number()
]


def generate_test_data():
  # Set seed to generate consistent test data
  npr.seed(1)
  
  data_lists = []
  n_recs = 110
  fk = Factory.create()
  
  for i in range(n_recs):
    payband = npr.choice([1, 2, 3], p=[0.7, 0.25, 0.05])
    payband = int(payband)
    salary = 0,
    if payband == 1:
      salary = fk.random_int(min=60000, max=120000)
    elif payband == 2:
      salary = fk.random_int(min=120000, max=160000)
    else:
      salary = fk.random_int(min=160000, max=200000)

    list_record = [
      i + 1,
      '{}, {}'.format(fk.last_name(), fk.first_name()),
      isodate.parse_date(fk.date()),
      payband,
      salary
    ]
    data_lists.append(list_record)
  return data_lists


def _generate_random(row):
  '''Generate random number according to the specified distribution'''
  r_n = npr.choice(3, 1, p=[.25, .65, .10])
  return int(r_n + 1)


def _add_random_column(data_tbl):
  # Reset seed to produce random numbers
  npr.seed()

  new_table = data_tbl.compute([
    ('random_group', agate.Formula(agate.Number(), _generate_random))
  ])
  return new_table


if __name__ == '__main__':
  data_lists = generate_test_data()
  
  # Create data table
  tbl = agate.Table(data_lists, column_names=column_names, column_types=column_types)
  
  # Produce summary table
  by_payband = tbl.group_by('pb')
  summary_tbl = by_payband.aggregate([
    ('count', agate.Count()),
    ('sal_min', agate.Min('salary')),
    ('sal_max', agate.Max('salary')),
    ('sal_median', agate.Median('salary'))
  ])
  
  # Display summary of generated test data
  print('Model data summary:\n')
  summary_tbl.print_table()
  print()
  summary_tbl.print_bars('pb', 'count', width=40)
  
  # ---Generate random numbers for simulation
  new_table = _add_random_column(tbl)
  
  # Show distributions of new table
  rand_tbl_count = new_table.pivot('random_group')
  rand_tbl_count = rand_tbl_count.order_by('random_group')
  
  rand_tbl_count = rand_tbl_count.compute([
    ('Percent', agate.Percent('Count'))
  ])
  
  print('\n Group distribution (count):\n')
  rand_tbl_count.print_table()
  
  
