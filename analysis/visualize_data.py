
# libraries and data
from matplquiotlib import pyplot as plt
import pandas as pd
import numpy as np

df = pd.DataFrame({'x': range(1, 101), 'y': np.random.randn(100) * 15 + range(1, 101),
                   'z': (np.random.randn(100) * 15 + range(1, 101)) * 2})

# Cut your window in 1 row and 2 columns, and start a plot in the first part
plt.subplot(121)
plt.plot('x', 'y', data=df, marker='o', alpha=0.4)
plt.title("A subplot with 2 lines")

# And now add something in the second part:
plt.subplot(122)
plt.plot('x', 'z', data=df, linestyle='none', marker='o', color="orange", alpha=0.3)
plt.savefig('PNG/#194_matplotlib_subplot1.png', dpi=96)

# Show the graph
plt.show()