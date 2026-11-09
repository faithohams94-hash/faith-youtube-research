"""Add a Morph transition (with fade fallback) to every slide of a .pptx."""
import sys, zipfile, shutil, re
src, dst = sys.argv[1], sys.argv[2]
TRANS = ('<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
         '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
         '<p:transition xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" spd="slow" p14:dur="1600">'
         '<p159:morph option="byObject"/></p:transition></mc:Choice>'
         '<mc:Fallback><p:transition spd="slow"><p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')
zin = zipfile.ZipFile(src)
zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
n = 0
for item in zin.infolist():
    data = zin.read(item.filename)
    if re.match(r'ppt/slides/slide\d+\.xml$', item.filename):
        x = data.decode('utf-8')
        x = re.sub(r'<p:transition.*?</p:transition>|<p:transition[^>]*/>', '', x, flags=re.S)
        if '</p:clrMapOvr>' in x:
            x = x.replace('</p:clrMapOvr>', '</p:clrMapOvr>' + TRANS, 1)
        else:
            x = x.replace('</p:cSld>', '</p:cSld>' + TRANS, 1)
        data = x.encode('utf-8'); n += 1
    zout.writestr(item, data)
zout.close()
print('morph added to', n, 'slides')
