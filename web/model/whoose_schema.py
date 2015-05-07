

## define whoose schema

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from jieba.analyse import ChineseAnalyzer

class InspirationSchema(SchemaClass):
    inspiration_id = ID(stored=True)
    content = TEXT(analyzer=ChineseAnalyzer())
