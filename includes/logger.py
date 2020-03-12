from datetime import datetime

def log(prefix, string, boolean):
        f = open(prefix + "_log.txt", "a")

        if boolean == True:
            f.write(string + " -- " + str(datetime.now()) + "\n")
            print(string)
        else:
            pass
        f.close()
