##  python操作evernote

印象笔记是一个比较常见的笔记软件。官方给出了python操作印象笔记的街口。但不足之处是，官方的中文文档和大多数的博客都是基于python2编写的。官方的API是英文结构。所以，笔者在使用后，写了这篇中文介绍。

### 安装

安装有2种方法。pip和源代码安装。

使用pip安装时，对应的语句是:

```python
pip install evernote3
```

使用源代码安装时，首先需要从github网站上clone源代码，对应的github网站是<https://github.com/evernote/evernote-sdk-python3>

安装时，运行下面语句：

```python
python setup.py install
```

#### 认证

认证需要首先获得一个token，字面意思就是令牌。获取地址是：

<https://sandbox.yinxiang.com/api/DeveloperToken.action>

点击revoke your developer token,然后会进入到下面的URL对应的页面：

<https://sandbox.yinxiang.com/api/DeveloperToken.action>

点击create a developer token，就会生产一个token

复制developer Token对应的字符串，该字符串就是你的Token

#### 初始化

初始化的时候需要导入一些包：

```python
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import os
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.type.ttypes import NoteSortOrder
```

其中，EvernoteClient是客户端的类，客户端初始化，即和官网的服务器建立连接的方法是：

```python
sandbox=False
china=True

client = EvernoteClient(token=auth_token, sandbox=sandbox,china=china)
```

其中，sandox等于False表示使用产品服务，等于True时使用沙箱服务器，

token是前面所说的Token，如果连接国际服务器，国际服务器是evernote，对应的china需要设定为False，如果连接国内服务器，国内服务器是印象笔记，对应的china需要设定为True。sandox和china这两个属性必须设置，否则容易导致认证失败，错误代码通常为8。

### 获得笔记本列表

获得笔记本列表的步骤如下：

* 获得笔记仓库

  ```python
  note_store = client.get_note_store()
  ```

* 获得笔记本列表

  ```python
  notebooks = note_store.listNotebooks()
  ```

获得是很多个Notebook类组成的列表，随便拿出来一个来看一下notebook类的结构：

```
Notebook(guid='aaa5bbfe-4025-4070-857e-aa1236e99cc3', name='微信', updateSequenceNum=24673, defaultNotebook=False, serviceCreated=1501604819000, serviceUpdated=1557889613000, publishing=None, published=None, stack='临时', sharedNotebookIds=None, sharedNotebooks=None, businessNotebook=None, contact=None, restrictions=NotebookRestrictions(noReadNotes=None, noCreateNotes=None, noUpdateNotes=None, noExpungeNotes=None, noShareNotes=None, noEmailNotes=True, noSendMessageToRecipients=None, noUpdateNotebook=None, noExpungeNotebook=None, noSetDefaultNotebook=None, noSetNotebookStack=None, noPublishToPublic=True, noPublishToBusinessLibrary=True, noCreateTags=None, noUpdateTags=None, noExpungeTags=None, noSetParentTag=None, noCreateSharedNotebooks=None, updateWhichSharedNotebookRestrictions=None, expungeWhichSharedNotebookRestrictions=None))
```

可见，Notebook类包含很多属性：

* guid:笔记本的id
* name:笔记本的名字
* stack: 笔记本所在的笔记本组的名字
* restrictions：使用NotebookRestrictions类对笔记本的相关属性做很多限制，不过大多数是None