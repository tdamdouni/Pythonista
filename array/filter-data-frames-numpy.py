# http://stackoverflow.com/questions/40694073/how-to-replicate-pandas-syntax-to-filter-data-frames

# recarray or structured array
# https://docs.scipy.org/doc/numpy/user/basics.rec.html

import numpy as np

myarray = np.array([("Hello",2.5,3),
                        ("World",3.6,2),
                        ('Foobar',2,7)]).T

df = np.core.records.fromarrays(myarray,
                             names='column1, column2, column3',
                             formats = 'S8, f8, i8')

print(df)
print(df[df.column3<=3])

# subclassing ndarray
# https://docs.scipy.org/doc/numpy/user/basics.subclassing.html

myarray = np.array([(1,2.5,3.),
                        (2,3.6,2.),
                        (3,2,7.)])
print(myarray[myarray[:,2]<=3.])

