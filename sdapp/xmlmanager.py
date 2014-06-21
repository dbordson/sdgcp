def filemapper(CIK, form):
    import os
    xmldirectory = []
    cwd = os.getcwd()

    if form == '4/A':
        form = '4A'

    for root, dirs, files in os.walk(cwd + "/AutomatedFTP/storage/" +
                                     str(CIK) + "/" + str(form) + "/"):
        for file in files:
            if file.endswith('.xml'):
#               if os.path.join(root, file).find("0001179110") == -1:
#                   print os.path.join(root, file)
                xmldirectory.append(os.path.join(root, file))
    return xmldirectory
