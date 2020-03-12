from datetime import datetime
import logging

#Ska kunna ta ett prefix + en sträng som den sedan sparar med tidsstämpel i prefix_log.txt.
#Vid behov ska man också kunna säga som tredje
#input True eller False om man vill data strängen ska printas när den lagras.
#Exempel på input:
#func("server", "En test sträng", True)
#Ska ge output:
#En test sträng i filen server_log.txt samt en print i konsollen som säger En test sträng.
#Subsekventa skrivningar ska sparas i samma fil och inte överskridas.

def func(prefix, string, boolean):
        f = open(prefix + "_log.txt", "a")

        if boolean == True:
            f.write(string + " -- " + str(datetime.now()) + "\n")
            print(string)
        else:
            pass
        f.close()
func("server", "En test sträng", True)
func("Test", "nytt test", False)
