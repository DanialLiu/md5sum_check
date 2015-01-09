import os
import sys
import md5
gFileMatch = 'zip'
gWorkPath = '.'
gGenCount = 0
gMatchedCount = 0

if len(sys.argv) > 1:
    gFileMatch = sys.argv[1]
    gFileMatch.lower()
if len(sys.argv) > 2:
    gWorkPath = sys.argv[2]
gFileMatch = '.' + gFileMatch


def IsMd5Ok(md5path, md5sum):
    try:
        f = open(md5path, 'r')
        filemd5 = f.read(32)
        f.close()
        print "file md5", filemd5, "md5 in file", md5sum
        return filemd5.lower() == md5sum.lower()
    except Exception:
        print "--- md5 file missing ---"
        return False


def GenMd5(filepath):
    # check if md5sum already here,or wrong
    print "file:", filepath
    f = open(filepath, 'rb')
    md5sum = md5.new(f.read()).hexdigest()
    f.close()
    print "md5:", md5sum
    if len(md5sum) != 32:
        raise "error md5"
    md5path = filepath + ".md5sum.txt"
    if IsMd5Ok(md5path, md5sum):
        global gMatchedCount
        print "### md5sum.txt match, pass ###"
        gMatchedCount = gMatchedCount + 1
    else:
        global gGenCount
        f = open(md5path, 'w')
        f.write(md5sum)
        f.close()
        print "=== write md5sum.txt success ==="
        gGenCount = gGenCount + 1


def Check(rootDir):
    for f in os.listdir(rootDir):
        path = os.path.join(rootDir, f)
        if os.path.isfile(path) and os.path.splitext(f)[1].lower() == gFileMatch:
            GenMd5(path)
Check(gWorkPath)
print "new generate md5 file:", gGenCount
print "already matched file:", gMatchedCount
