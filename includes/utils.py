def get_info(filename, key):
    try:
        
        file = open(filename)
        
        lines = file.readline()
        while lines:
            if key in lines:
                lines = lines.partition(key)[2]
                return lines
                break
    except:
        print("No configuration file was found, creating sample configuration file...")
        file = open('config.txt', 'w+')
        file.write("DB_IP = 127.0.0.1\nDB_PORT = 8159\nDB_USER = root\nDB_PASS = admin\nDB_DATABASE = meshdep\n\nSERVER_IP = 127.0.0.1\nSERVER_PORT = 6220\nSERVER_MAX_NODES = 3\n\nNODE_TRANSFER_STARTPORT = 7430\n")
        return "Configuration file, config.txt, has been created. Change the default values to accurate values. "
    finally:
        file.close()


test = get_info('config.txt', 'DB_IP = ')
print(test)
