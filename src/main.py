
def main():
    # add source to sys.path so python can look up created modules
    import sys
    sys.path.append(
        '\\'.join(__file__.split('\\')[:-1])
    )

    # start UI
    import LtMAO.prettyUI
    LtMAO.prettyUI.start()


if __name__ == '__main__':
    main()
