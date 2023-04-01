# add source to sys.path so python can look up created modules
import sys
sys.path.append(
    '\\'.join(__file__.split('\\')[:-1])
)

import LtMAO
