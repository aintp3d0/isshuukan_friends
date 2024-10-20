# Diary for 藤宮 香織
- Anime: 一週間フレンズ。
```bash
python3 main.py
# or
python3 main.py --atr "藤宮 香織"

# ATR - Author
# TTL - Title
# DSN - Description
```

### Example
```
TTL - 表題: 学校の屋根の上
DSN - 説明: 友人と一緒に昼食を持っていた「祐樹」、彼は卵のパンを食べました
DSN - 説明:
DSN - 説明:
DSN - 説明:

+-------------------[ 水曜日2017年11月29日 / 14時12分56秒 ]
|
| -> 学校の屋根の上
| -> 友人と一緒に昼食を持っていた「祐樹」、彼は卵のパンを食べました
|
+-------------------------------------------------------------@藤宮 香織
```

### File Structure
```
# tree . -I "__pycache__|__init__.py"
.
├── data
│   ├── user.txt
│   └── words.db
├── daybook.txt
├── LICENSE
├── main.py
├── README.md
├── scripts
│   ├── db.py
│   └── update_words_id.py
└── smk.txt
```

### TODO
- [ ] Rename `protected-members` (methods)
