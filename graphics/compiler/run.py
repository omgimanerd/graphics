import mdl

def run(filename):
    """
    This function runs an mdl script
    """

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return
        
    #for command in commands:
        #print command
    for symbol in symbols:
        print symbol

if __name__ == "__main__":
    run("dwrobot.mdl")
