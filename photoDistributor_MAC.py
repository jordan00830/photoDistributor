from photoDistributor import *

if __name__ == '__main__':
    # Set True as debug mode (auto setting source folder, target folder, tag list file)
    app = PhotoCtrl(False,EnumEnv.MAC)
    app.MainLoop()