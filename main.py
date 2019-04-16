import os
import shutil
import hashlib
import tqdm
import sys

def makeFolder(path):
    if path=="" or os.path.exists(path):
        pass
    else:
        makeFolder(os.path.split(path)[0])
        os.mkdir(path)

def readDirectory(path):
    files = []
    for r,d,f in os.walk(path):
        for file in f:
            files.append(os.path.join(r,file))
    return files

def scanPath(prompt):
    valid = False
    while(not valid):
        valid = True
        path = input(prompt+"\n")
        path = path.replace('"',"")
        path = path.replace("'","")
        if path[-1]=='\\':
            path = path[:-1]
        pathList = path.split("\\")
        if not os.path.exists(pathList[0]):
            valid = False
            print(f"{pathList[0]} does not exist.")
        elif os.path.isfile(path):
            print(f"'{path}' is a File.\nTruncating to:\n'{os.path.dirname(path)}'")
            path = os.path.dirname(path)
        elif not os.path.exists(path):
            if input("Path does not exist. Create? (y/n)\n")[0]=='y':
                makeFolder(path)
            else:
                valid = False
    return path

def hashCheck(src,dst):
    with open(src,'rb') as old, open(dst,'rb') as new:
        hasher1,hasher2 = hashlib.md5(),hashlib.md5()
        hasher1.update(old.read())
        hasher2.update(new.read())
        hash1 = hasher1.hexdigest()
        hash2 = hasher2.hexdigest()
        return hash1==hash2

def init():
    src = scanPath("Enter source path:")
    dst = scanPath("Enter destination path:")
    srcFiles = readDirectory(src)
    return src,dst,srcFiles

def cleanEmptyDirectoriesRec(path):
    if os.listdir(path):
        for dir in next(os.walk(path))[1]:
            cleanEmptyDirectoriesRec(os.path.join(path,dir))
        cleanEmptyDirectoriesRec(path)
    else:
        os.rmdir(path)

def cleanEmptyDirectories(path):
    try:
        for dir in next(os.walk(path))[1]:
            cleanEmptyDirectoriesRec(os.path.join(path,dir))
    except (StopIteration, RecursionError):
        pass

def worker(src,dst,srcFiles):
    failed = []
    print(f"{len(srcFiles)} files to be processed")
    for file in tqdm.tqdm(srcFiles):
        if not os.path.exists(file.replace(src,dst)) or input(f"{file.replace(src,dst)} already exists. Replace? (y,n)\n")[0]=='y':
            makeFolder(os.path.dirname(file.replace(src,dst)))
            shutil.copy(file,file.replace(src,dst))
            if hashCheck(file,file.replace(src,dst)):
                os.remove(file)
            else:
                os.remove(file.replace(src,dst))
                print(f"{file} failed to copy.")
                failed.append(file)
    cleanEmptyDirectories(src)
    print(f"Processed {len(srcFiles)} files. {len(failed)} failed to copy.")
    if len(failed)>0:
        if input("Show details? (y,n)\n")[0]=='y':
            for entry in failed:
                print(entry)

def main():
    if "test" in sys.argv[1:]:
        print("Using test case:")
        worker("I:\\temp\\Daily_temp\\old","I:\\temp\\Daily_temp\\new",readDirectory("I:\\temp\\Daily_temp\\old"))
    else:
        worker(init())



if __name__ == '__main__':
    main()
