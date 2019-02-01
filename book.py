#用于和数据库创建连接
from sqlalchemy import create_engine
#用于实例一个基类，创建表时必须继续这个父类
from  sqlalchemy.ext.declarative import declarative_base
#导入表元素，列，数据类型，外键，索引..
from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,Index

Base = declarative_base()

class Book(Base):
    # 指定本类映射到users表
    __tablename__ = 'tb_book'

    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    # 指定name映射到name字段; name字段为字符串类形，
    chapter_name = Column(String(20))
    chapter_url = Column(String(50))
    chapters = Column(String(50))

    def __repr__(self):
        return "<Book(chapter_name='%s', chapter_url='%s', chapters='%s')>" % (
            self.chapter_name, self.chapter_url, self.chapters)


class Chapter(Base):
    __tablename__ = 'tb_chapter'

    id = Column(Integer, primary_key=True)
    chapter_id = Column(String(20))
    chapter_content = Column(String())

    def __repr__(self):
        return "<Chapter(chapter_id='%s', chapter_content='%s'>" % (
            self.chapter_id, self.chapter_content)

if __name__ == '__main__':
    engine = create_engine('sqlite:////Users/zll/Desktop/foo.db?check_same_thread=False', echo=True)
    Base.metadata.create_all(engine)