<h1>Windows Recycle Bin Parser Version.1</h1>

<h2>Korean Description</h2>

<h3>설명</h3>

Recycle Bin 아티팩트 파일은 Windows 에서 휴지통이라고 불리는 아티팩트 이며 삭제된 파일을 저장하는 공간으로 사용된다.
RBParser_Ver1.py는 Windows XP, Windows 7, Windows 8.1, Windows 10의 OS에서 지원하는 모든 Recycle Bin 아티팩트 파일을 분석할 수 있습니다.

<h3>사용방법</h3>

Recycle Bin 파일 하나에 대한 툴 사용법

```
python RBParser_Ver1.py [INFO2 FILE]
python RBParser_Ver1.py [$I###### FILE]
```

<h3>다른 툴과 비교했을때 개선된점</h3>

- Windows XP , Windows 7, Windows 8 , Windows 10의 Recycle Bin 을 하나의 도구로 분석해 주는 도구가 없다.
- 출력된 데이터를 좀더 깔끔하게 출력해준다.

<h3>부족한 부분</h3>

- Windows 7,8,10 에서는 $I##### 파일 1개를 INPUT 하여 데이터를 출력해 주지만 휴지통 자체의 파일을 전부 읽어서 데이터를 리스트화 해주지 않음.
- CSV 파일로 내보내기 기능
- 한글과 같은 유니코드 출력 기능

위의 기능들은 RBParser_Ver2.py에서 다룰 예정입니다.

<h3>파이썬 요구 모듈</h3>

- from datetime import datetime, timedelta
- import struct
- import sys
- import string

---

<h2>English Description</h2>

<h3>Description</h3>

Recycle Bin artifact files are artifacts called trash cans in Windows and are used as storage spaces for deleted files.
RBParser_Ver1.py can analyze any Recycle Bin artifact file supported by OS in Windows XP, Windows 7, Windows 8.1, and Windows 10.

<h3>How To Use?</h3>

How to use tools for Recycle Bin files

```
python RBParser_Ver1.py [INFO2 FILE]
python RBParser_Ver1.py [$I###### FILE]
```

<h3>Improvements compared to other tools</h3>

- There is no tool to analyze Recycle Bin on Windows XP, Windows 7, Windows 8, or Windows 10 with one tool.
- The printed data should be printed more neatly.

<h3>Deficient Part</h3>

- Windows 7,8,10 will print out one $I#### file, but will not list the data by reading all of the files in the trash.
- Export function to CSV file
- Unicode output functions such as Hangul

The above functions will be covered by RBParser_Ver2.py

<h3>Python Requirements Module</h3>

- from datetime import datetime, timedelta
- import struct
- import sys
- import string