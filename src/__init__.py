import pkg_resources
from io import BytesIO
import re
import sys
import csv
import string
import os
import os.path
from os.path import join
from zipfile import ZipFile
import zipfile
import shutil

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
    from urllib.request import urlopen
else:
    from urllib import urlretrieve
    from urllib import urlopen

IPBurp = '192.168.1.12'
libAppArm64 = '',''
libAppArm = '',''
libAppX64 = '',''
libAppX86 = '',''
libios = '',''
libappHash = ''
ZIPSTORED = False

def patchLibrary():
 if len(libios[1]) != 0:
    buffer = open('Flutter', 'rb').read().replace(b'192.168.133.104', IPBurp.encode('ascii'))
    open('Flutter', 'wb').write(buffer)
 if len(libAppArm64[1]) != 0:
    buffer = open('libflutter_arm64.so', 'rb').read().replace(b'192.168.133.104', IPBurp.encode('ascii'))
    open('libflutter_arm64.so', 'wb').write(buffer)
 if len(libAppArm[1]) != 0:
    buffer = open('libflutter_arm.so', 'rb').read().replace(b'192.168.133.104', IPBurp.encode('ascii'))
    open('libflutter_arm.so', 'wb').write(buffer)
 if len(libAppX64[1]) != 0:
    buffer = open('libflutter_x64.so', 'rb').read().replace(b'192.168.133.104', IPBurp.encode('ascii'))
    open('libflutter_x64.so', 'wb').write(buffer)

def inputIPBurp():
    global IPBurp
    try:
        IPBurp = raw_input("Example: (192.168.1.154) etc.\nPlease enter your BurpSuite IP: ")
        if not re.match(r'[0-9]+(?:\.[0-9]+){3}', IPBurp):
            print("Invalid IP Address")
            inputIPBurp()
    except:
        IPBurp = input('Example: (192.168.1.154) etc.\nPlease enter your BurpSuite IP: ')
        if not re.match(r'[0-9]+(?:\.[0-9]+){3}', IPBurp):
            print("Invalid IP Address")
            inputIPBurp()
    convertIPFix()

def networkLib():
    global libAppArm64,libAppArm,libAppX64,libAppX86,libios
    if len(libios[1]) != 0:
       try:
        urlretrieve("https://github.com/HuChundong/reflutter-hucd/releases/download/ios-v3-"+libios[1]+"/Flutter", "Flutter")
       except:
        libios='',''
        notexcept("Flutter")
    if len(libAppArm64[1]) != 0:
       try: 
        urlretrieve("https://github.com/HuChundong/reflutter-hucd/releases/download/android-v3-"+libAppArm64[1]+"/libflutter_arm64.so", "libflutter_arm64.so")
       except:
        libAppArm64='',''
        notexcept("libflutter_arm64.so")
    if len(libAppArm[1]) != 0:
       try:
        urlretrieve("https://github.com/HuChundong/reflutter-hucd/releases/download/android-v3-"+libAppArm[1]+"/libflutter_arm.so", "libflutter_arm.so")
       except:
        libAppArm='',''
        notexcept("libflutter_arm.so")
    if len(libAppX64[1]) != 0:
       try:
        urlretrieve("https://github.com/HuChundong/reflutter-hucd/releases/download/android-v3-"+libAppX64[1]+"/libflutter_x64.so", "libflutter_x64.so")
       except:
        libAppX64='',''
        notexcept("libflutter_x64.so")
    if len(libAppX86[1]) != 0:
       try:
        urlretrieve("https://github.com/HuChundong/reflutter-hucd/releases/download/android-v3-"+libAppX86[1]+"/libflutter_x86.so", "libflutter_x86.so")
       except:
        libAppX86='',''
        notexcept("libflutter_x86.so")
    patchLibrary()

def convertIPFix():
    global IPBurp
    intoct = list(IPBurp.split('.'))
    finallistIP=list(IPBurp.split('.'))
    intoct.sort(key=lambda s: len(s))
    intoct.reverse()
    for i in intoct:
        if len(i)!=3 and int(i)>7 and int(i)>63 and len('.'.join(intoct))<15: #64-99
            intoct[intoct.index(i)]=str(oct(int(i))).replace('o','')
        elif len(i)!=3 and int(i)>7 and int(i)<64 and len('.'.join(intoct))<15: #8-63
            intoct[intoct.index(i)]=str(oct(int(i))).replace('o','')
        elif len(i)<3 and int(i)<8 and len('.'.join(intoct))<15: #0-7
            intoct[intoct.index(i)]=intoct[intoct.index(i)].zfill(3)
    for i in intoct:
        if i.startswith('0'):
            if len(i)!=3 and int(i, 8)>7 and len('.'.join(intoct))>15: #8-63
                intoct[intoct.index(i)]=str(int(i, 8)).replace('o','')
            elif len(i)<3 and int(i)<8 and len('.'.join(intoct))<15: #0-7
                intoct[intoct.index(i)]=intoct[intoct.index(i)].zfill(3)
        elif len(i)==3 and int(i)>7 and int(i)>99 and len('.'.join(intoct))>15: #64-99
            intoct[intoct.index(i)]=str(oct(int(i))).replace('o','')
    for f in finallistIP:
        for i in intoct:
            if i.startswith('0'):
                if f==str(int(i, 8)):
                    finallistIP[finallistIP.index(f)]=i.replace('o','')
    IPBurp = '.'.join(finallistIP)

def notexcept(filename):
    try:
        os.remove(filename)
    except:
        pass

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            if type(file) is str:
                if file.endswith('.so') and ZIPSTORED or file.endswith('resources.arsc'):
                    ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root.replace('release/',''), file),os.path.join(path, '..')),zipfile.ZIP_STORED)
                else:
                    ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root.replace('release/',''), file),os.path.join(path, '..')),zipfile.ZIP_DEFLATED)
            else:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root.replace('release/',''), file),os.path.join(path, '..')),zipfile.ZIP_DEFLATED)

def replaceLibFlutter():
    if len(sys.argv) < 3:
        checkHash()
        inputIPBurp()
        networkLib()
    if os.path.exists("libflutter_arm64.so") or os.path.exists("libflutter_arm.so") or os.path.exists("libflutter_x64.so") or os.path.exists("libflutter_x86.so") or os.path.exists("Flutter"):
     try:
        shutil.move("Flutter", join("release",libios[0].replace("App.framework/App","Flutter.framework/Flutter").replace("FlutterApp.framework/FlutterApp","Flutter.framework/Flutter")))
     except:
         pass
     try:
        shutil.move("libflutter_arm64.so", join("release",libAppArm64[0].replace("libapp.so","libflutter.so")))
     except:
         pass
     try:
        shutil.move("libflutter_arm.so", join("release",libAppArm[0].replace("libapp.so","libflutter.so")))
     except:
         pass
     try:
        shutil.move("libflutter_x64.so", join("release",libAppX64[0].replace("libapp.so","libflutter.so")))
     except:
         pass
     try:
        shutil.move("libflutter_x86.so", join("release",libAppX86[0]))
     except:
         pass

     zipf = zipfile.ZipFile('release.RE.zip', 'w', zipfile.ZIP_DEFLATED)
     zipdir('release/', zipf)
     zipf.close()
     shutil.rmtree('libappTmp')
     shutil.rmtree('release')
     print("\nSnapshotHash: "+libappHash)
     if len(libios[1]) != 0:
         shutil.move("release.RE.zip", "release.RE.ipa")
         print("The resulting ipa file: ./release.RE.ipa\nPlease install the ipa file\n\nConfigure Burp Suite proxy server to listen on *:8083\nProxy Tab -> Options -> Proxy Listeners -> Edit -> Binding Tab\n\nThen enable invisible proxying in Request Handling Tab\nSupport Invisible Proxying -> true\n")
     else:
         shutil.move("release.RE.zip", "release.RE.apk")
         print("The resulting apk file: ./release.RE.apk")
         print("Please sign,align the apk file\n\nConfigure Burp Suite proxy server to listen on *:8083\nProxy Tab -> Options -> Proxy Listeners -> Edit -> Binding Tab\n\nThen enable invisible proxying in Request Handling Tab\nSupport Invisible Proxying -> true\n")
     sys.exit()

def replaceFileText(fname,textOrig,textReplace):
   try:
    with open(fname, 'r') as file :
     filedata = file.read()
     filedata = filedata.replace(textOrig, textReplace)
    with open(fname, 'w') as file:
     file.write(filedata)
   except (IOError, OSError) as e:
       pass

def patchSource(hashS,ver):
    return

def ELFF(fname, **kwargs):
    global libappHash
    min=32
    if sys.version_info >= (3, 0):
       f = open(fname, errors="ignore")
    else:
       f = open(fname, 'rb') 
    result = ""
    for c in f.read():
       if c in string.printable:
          result += c
          continue
       if len(result) >= min:
          hashT = re.findall(r"([a-f\d]{32})", result)
          if(len(hashT)>0):
            libappHash = hashT[0]
            f.close()
            return hashT[0]
       result = ""

def checkHash():
    if libappHash=="":
        print("\nIs this really a Flutter app? \nThere was no libapp.so (Android) or App (iOS) found in the package.\n\n Make sure there is arm64-v8a/libapp.so or App.framework/App file in the package. If flutter library name differs you need to rename it properly before patching.\n")
        sys.exit()
    resp = urlopen('https://raw.githubusercontent.com/HuChundong/reflutter-hucd/main/enginehash.csv').read().decode('utf-8')
    if libappHash not in resp:
        shutil.rmtree('libappTmp')
        print("\n Engine SnapshotHash: "+libappHash+"\n\n This engine is currently not supported.\n Most likely this flutter application uses the Debug version engine which you need to build manually using Docker at the moment.\n More details: https://github.com/HuChundong/reFlutter\n")
        sys.exit()

def extractZip(zipname):
    global libAppArm64,libAppArm,libAppX64,libAppX86,libios,ZIPSTORED
    with ZipFile(zipname, 'r') as zipObject:
        listOfFileNames = zipObject.namelist()
        zipObject.extractall('release')
        for fileName in listOfFileNames:
            if fileName.endswith('App.framework/App') or fileName.endswith('FlutterApp.framework/FlutterApp'):
                zipObject.extract(fileName, 'libappTmp')
                libios = fileName, ELFF(join('libappTmp',fileName))
                sys.argv[1] = join('libappTmp',libios[0])
            if fileName.endswith('v8a/libapp.so'):
                if zipObject.getinfo(fileName).compress_type == zipfile.ZIP_STORED:
                    ZIPSTORED = True
                zipObject.extract(fileName, 'libappTmp')
                libAppArm64 = fileName, ELFF(join('libappTmp',fileName))
                sys.argv[1] = join('libappTmp',libAppArm64[0])
            if fileName.endswith('v7a/libapp.so'):
                if zipObject.getinfo(fileName).compress_type == zipfile.ZIP_STORED:
                    ZIPSTORED = True
                zipObject.extract(fileName, 'libappTmp')
                libAppArm = fileName, ELFF(join('libappTmp',fileName))
                sys.argv[1] = join('libappTmp',libAppArm[0])
            if fileName.endswith('64/libapp.so'):
                if zipObject.getinfo(fileName).compress_type == zipfile.ZIP_STORED:
                    ZIPSTORED = True
                zipObject.extract(fileName, 'libappTmp')
                libAppX64 = fileName, ELFF(join('libappTmp',fileName))
                sys.argv[1] = join('libappTmp',libAppX64[0])
            if fileName.endswith('86/libflutter.so'):
                zipObject.extract(fileName, 'libappTmp')
                libAppX86 = fileName, ELFF(sys.argv[1])
        zipObject.close()
        replaceLibFlutter()

def main():
 try:
  if sys.argv[1].lower().endswith('.apk') or sys.argv[1].lower().endswith('.ipa'):
    extractZip(sys.argv[1])
    libappHash = ELFF(sys.argv[1])
    shutil.rmtree('libappTmp')
  else:
    libappHash = sys.argv[1]

  if not os.path.exists("enginehash.csv"):
    urlretrieve("https://raw.githubusercontent.com/HuChundong/reflutter-hucd/main/enginehash.csv", "enginehash.csv")

  with open("enginehash.csv") as f_obj:
   replaceFileText('src/src/flutter/BUILD.gn','  if (is_android) {\n    public_deps +=\n        [ "//flutter/shell/platform/android:flutter_shell_native_unittests" ]\n  }','')
   read = csv.DictReader(f_obj, delimiter=',')
   row_count = sum(1 for _ in read)
   f_obj.seek(0)
   reader = csv.DictReader(f_obj, delimiter=',')
   i = -row_count
   for line in reader:
    i=i+1
    if libappHash in line["Snapshot_Hash"]:
     print(line["Engine_commit"])
     if os.path.exists("src/third_party/dart/runtime/vm/dart.cc") or os.path.exists("tools/generate_package_config/pubspec.yaml") or os.path.exists("DEPS"):
         patchSource(libappHash,abs(i))
 except (IndexError, ValueError) as e:
       print("USAGE:\nreflutter your.(apk)|(ipa)")
