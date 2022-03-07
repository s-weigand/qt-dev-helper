# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.2.3
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x00i\
<\
svg height=\x22100\x22\
 width=\x22100\x22>\x0a  \
<circle cx=\x2250\x22 \
cy=\x2250\x22 r=\x2240\x22 s\
troke=\x22black\x22 st\
roke-width=\x223\x22/>\
\x0a</svg>\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00z\xc7\
\x00s\
\x00v\x00g\
\x00\x0a\
\x0a-\x1b\xc7\
\x00c\
\x00i\x00r\x00c\x00l\x00e\x00.\x00s\x00v\x00g\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x7fd\xe4\xa2S\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
