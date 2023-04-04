# add source to sys.path so python can look up created modules
import LtMAO.prettyUI
import sys
sys.path.append(
    '\\'.join(__file__.split('\\')[:-1])
)

LtMAO.prettyUI.start()
