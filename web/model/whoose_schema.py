

## define whoose schema

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from jieba.analyse import ChineseAnalyzer

class InspirationSchema(SchemaClass):
    labels = KEYWORD(commas=True)
    inspiration_id = ID(stored=True, unique=True)
    content = TEXT(analyzer=ChineseAnalyzer())
