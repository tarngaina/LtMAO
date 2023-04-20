
def main():
    # add source to sys.path so python can look up created modules
    import sys
    sys.path.append(
        '\\'.join(__file__.split('\\')[:-1])
    )

    # json float 8 digits
    class PrettyFloat(float):
        __repr__ = staticmethod(lambda x: f'{x:.8f}')
    import json
    json.encoder.float = PrettyFloat

    # start UI
    import LtMAO.prettyUI
    LtMAO.prettyUI.start()


main()
