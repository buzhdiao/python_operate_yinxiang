# -*- coding: utf-8 -*-
import hashlib
import binascii
import evernote.edam.type.ttypes as Types
import os
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.type.ttypes import NoteSortOrder

auth_token = "S=s1:U=29:E=16cb1f1b52b:D=16c8de52f18:P=1cd:C=en-devtoken:V=2:H=2e47232c944f6cd1d3948b507658d2c1"

sandbox=False
china=True
client = EvernoteClient(token=auth_token, sandbox=sandbox,china=china)

user_store = client.get_user_store()

note_store = client.get_note_store()

# List all of the notebooks in the user's account
notebooks = note_store.listNotebooks()
print("Found ", len(notebooks), " notebooks:")
for notebook in notebooks:
    print("  * ", notebook.name)

print()
print("Creating a new note in the default notebook")
print()

# 创建一个笔记本
new_book = Types.Notebook(name='014 牛客网-华为机试',stack='编程')
note_store.createNotebook(auth_token,new_book)
selected_book = [item for item in note_store.listNotebooks() if item.name=='014 牛客网-华为机试'][0]


updated_filter = NoteFilter(order=NoteSortOrder.CREATED, notebookGuid=selected_book.guid )
# 偏移0
offset = 0
# 只取一条笔记
max_notes = 1

# 查找出符合条件的笔记
result_list = note_store.findNotes(updated_filter, offset, max_notes)

def read_file(file):
    with open(file,'r',encoding='utf-8') as f:
        data = f.read()
    return data
# 创建Note
dir_name = 'F:\zkl_repository\jianzhiffer_with_java\牛客网-华为机试练习题\md'
docList = os.listdir(dir_name)  #特定目录下的文件存入列表
docList.sort()   # 显示当前文件夹下所有文件并进行排序
ignore_file = ['all.md']
docList = [item for item in docList if item not in ignore_file]
attribute = Types.NoteAttributes()
#attribute.contentClass='yinxiang.markdown'
for item in docList:
    note = Types.Note()
    note.title = item
    fname  = os.path.join(dir_name,item)
    data = read_file(fname)
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
                '"http://xml.evernote.com/pub/enml2.dtd">'
    note.content+='<en-note>'+data
    note.content += '</en-note>'
    note.notebookGuid = selected_book.guid
    note.attributes=attribute
    created_note = note_store.createNote(auth_token,note)
    


# To create a new note, simply create a new Note object and fill in
# attributes such as the note's title.
note = Types.Note()
note.title = "Test note from EDAMTest.py"

# To include an attachment such as an image in a note, first create a Resource
# for the attachment. At a minimum, the Resource contains the binary attachment
# data, an MD5 hash of the binary data, and the attachment MIME type.
# It can also include attributes such as filename and location.
image_path = constants_path = os.path.join(os.path.dirname(__file__), "enlogo.png")
with open(image_path, 'rb') as image_file:
    image = image_file.read()
md5 = hashlib.md5()
md5.update(image)
hash = md5.digest()

data = Types.Data()
data.size = len(image)
data.bodyHash = hash
data.body = image

resource = Types.Resource()
resource.mime = 'image/png'
resource.data = data

# Now, add the new Resource to the note's list of resources
note.resources = [resource]

# To display the Resource as part of the note's content, include an <en-media>
# tag in the note's ENML content. The en-media tag identifies the corresponding
# Resource using the MD5 hash.
hash_hex = binascii.hexlify(hash)
hash_str = hash_hex.decode("UTF-8")

# The content of an Evernote note is represented using Evernote Markup Language
# (ENML). The full ENML specification can be found in the Evernote API Overview
# at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM ' \
                '"http://xml.evernote.com/pub/enml2.dtd">'
note.content+='<en-note>'+data
note.content += '</en-note>'

# Finally, send the new note to Evernote using the createNote method
# The new Note object that is returned will contain server-generated
# attributes such as the new note's unique GUID.
created_note = note_store.createNote(note)

print("Successfully created a new note with GUID: ", created_note.guid)
