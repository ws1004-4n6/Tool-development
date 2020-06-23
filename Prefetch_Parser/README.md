<h1>Windows Prefetch Parser Version.1</h1>

<h2>Korean Description</h2>

<h3>설명</h3>

프리패치 파일은 응용프로그램이 실행 됬을때 생성되는 윈도우 아티팩트로 실행 횟수, 마지막 실행시간, 실행된 볼륨의 VSN값 등등 여러 중요 정보가 들어있는 아티팩트입니다.
Prefetch_Parser_Ver1.py는 Windows XP, Windows 7, Windows 8.1, Windows 10의 OS에서 지원하는 모든 프리패치 파일을 분석할 수 있습니다.

<h3>사용방법</h3>

.pf 파일 하나에 대한 툴 사용법

```
python Prefetch_Parser_Ver1.py [Prefetch_File_Name]
```

디렉터리 하위에 있는 모든 .pf 파일에 대한 툴 사용법

```
python Prefetch_Parser_Ver1.py [Prefetch_File_Directory]\

or

python Prefetch_Parser_Ver1.py [Prefetch_File_Directory]/
```

<h3>다른 툴과 비교했을때 개선된점</h3>

- Windows 10에서는 프리패치 파일을 MAM 시그니처로 압축해서 관리를 진행하는데 MAM 시그니처에서 압축이 해제된 프리패치 파일을 분석하지 않는 도구가 있어서 압축해제된 프리패치 파일도 분석에 도움이 되도록 추가하였습니다.
- 프리패치 관련 모든 도구에서는 해당 프리패치에 사용된 볼륨 정보를 따로 출력해 주지 않아서 쉽게 확인이 가능할수 있도록 볼륨 정보 출력 기능을 추가하였습니다.

<h3>부족한 부분</h3>

- CSV 파일로 내보내기 기능
- 한글과 같은 유니코드 출력 기능(Ver.1에서는 무시해서 이상한 값 출력)
- GUI 기능

위의 기능들은 Prefetch_Parser_Ver2.py에서 다룰 예정입니다.

<h3>파이썬 요구 모듈</h3>

- from datetime import datetime, timedelta
- import binascii
- import ctypes
- import struct
- import sys
- import os
- import io

---

<h2>English Description</h2>

<h3>Description</h3>

A Prefatch file is a window artifact created when the application runs, and is an artifact that contains important information such as the number of runs, the last run time, and the VSN value of the executed volume.
Prefetch_Parser_Ver1.py can analyze all prefatch files supported by the OS on Windows XP, Windows 7, Windows 8.1, and Windows 10.

<h3>How To Use?</h3>

How to use tools for .pf files

```
python Prefetch_Parser_Ver1.py [Prefetch_File_Name]
```

Using the tool for all ".pf" files in the lower part of the directory

```
python Prefetch_Parser_Ver1.py [Prefetch_File_Directory]\

or

python Prefetch_Parser_Ver1.py [Prefetch_File_Directory]/
```

<h3>Improvements compared to other tools</h3>

- Windows 10 compressing and managing prefetch files with MAM signatures does not analyze uncompressed prefetch files, so we added uncompressed prefetch files to aid analysis.
- All tools related to prefatch do not print volume information used in the prefatch, so we added volume information output function to make it easier to check.

<h3>Deficient Part</h3>

- Export function to CSV file
- Unicode output functions such as Hangul(Outputs strange values ignored in Ver.1)
- GUI Function

The above functions will be covered by Prefetch_Parser_Ver2.py.

<h3>Python Requirements Module</h3>

- from datetime import datetime, timedelta
- import binascii
- import ctypes
- import struct
- import sys
- import os
- import io