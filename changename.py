# coding=utf-8
import os
import re

# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title

#文件名加上序号
def walkDir(rootdir=None):
    print rootdir
    count = 0
    for parent, dirnames, filenames in os.walk(rootdir):
        #for dirname in dirnames:
        #    print "parent is:" + parent
        #    print "dirname is:" + dirname
        for filename in filenames:
            print filename
            filename = validateTitle(filename)
            # if filename[-5:] == ".jpeg":
            src_file = os.path.join(parent, filename)
            dest_file = str(count)+filename
            os.rename(src_file, dest_file)
            count += 1
    print 'Rename total file count is:', count

def main():
    walkDir(os.getcwd())

if __name__ == "__main__":
    main()