from sqlalchemy import create_engine,Column,ForeignKey,func,Boolean,Time,TEXT
from sqlalchemy import and_,or_,Integer,FLOAT,String,Enum,Date,DECIMAL,Table
from sqlalchemy.orm import sessionmaker,declarative_base,relationship,backref
import enum
from datetime import datetime

# 数据库的变量
HOST = '127.0.0.1' # 127.0.0.1/localhost
PORT = 3306
DATA_BASE = 'flask_db'
USER = 'root'
PWD = "123456"

# DB_URI = f'数据库的名+驱动名://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}'
DB_URI = f'mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}'

#使用create_engine函数创建一个数据库引擎。
engine = create_engine(DB_URI)  

#Base = declarative_base(engine)：创建一个基类Base，并将其与数据库引擎关联。
Base = declarative_base()


new2_person=Table(           #通过第三张表关联两个表  多对多
    't_person_new',
    Base.metadata,
    Column('person_id',Integer,ForeignKey('t_person.id'),primary_key=True),
    Column('new2_id',Integer,ForeignKey('t_news2.id'),primary_key=True)
)

class person(Base):          #主表
    __tablename__ = "t_person"
    #定义一个名为id的列，类型为整数，设置为主键，并且自动递增。
    id  = Column(Integer,primary_key=True)
    name = Column(String(32))
    title = Column(String(32))
    age = Column(Integer)
    country = Column(String(32))

    # new2_t=relationship('new2',backref='person',secondary= new2_person)
    # news = relationship('news',backref='person',cascade='') 
    # cascade='save-update'         # 默认cascade的值是save-update
    # cascade='save-update',delete  # delete可以帮助删除关联表的数据
    #cascade='save-update,delete,delete-orphan',single_parent=True)  
    #当关联关系被解除时，子表数据会被清空

class tagnuem(enum.Enum):    #Enum枚举类型
    python = 'python'
    flask = 'flask'
    mysql = 'MYSQL'

class news(Base):            #子表
    __tablename__ = 't_news'
    id  = Column(Integer,primary_key=True)
    read_count =Column(Integer,default=1)            #defult默认值
    price =Column(FLOAT,default=1)
    price2 =Column(DECIMAL,nullable=False,default=1) #不准为空
    is_delete =Column(Boolean,default=True)
    

    #将主表的数据注入字段 person  将子表数据存入主表
    #person_news = relationship('person',backref=backref('news',lazy='dynamic')) 
    #person_news = relationship('person',backref=backref('news',uselist=False)) 
    
    #默认策略 若子表中有父表对应的关联数据，删除父表对应数据，会阻止删除。默认项
    #person_id =Column(Integer,ForeignKey('t_person.id',ondelete='RESTRICT'),nullable=False) #NO ACTION
    #ondelete='CASCADE  #级联删除。
    #ondelete='SET NULL #SET NULL

class new2(Base):            #子表2
    __tablename__ = 't_news2'
    id  = Column(Integer,primary_key=True)
    title =Column(String(32),default=1)
    phone =Column(String(11),unique=True) #唯一性
    #tag1 =Column('PYTHON')
    tag2 =Column(Enum(tagnuem))
    creat_time =Column(Date,default=datetime.now,onupdate=datetime.now)
    update_time =Column(Time)
    content =Column(TEXT)

#session = sessionmaker(engine)()：创建一个会话工厂。
Session = sessionmaker(engine)

def creat_date():          # 创建信息并上传
    with Session() as session:
        p1 = person(name = 'jx' , age = 22 , country = 'zg')
        new1 =news(price1=1000.0078,price2=1000.0078,is_delete=False,tag1="PYTHON",tag2=tagnuem.python)
        new2 =new2()

        p1.new1=new1

        #session.add(p1)
        session.add_all()
        session.commit()
def query_data_all():      # 获取person的所有数据  query order_by
    with Session() as session:
        all_person = session.query(person).all()  
        age_t = session.query(person).order_by(person.age.desc()).all()

        for p in all_person:  #<__main__.person object at 0x00000195DD476FF0>
            print(p) 
            print(p.name)       
def query_data_one():      # 获取第一个数据
    with Session() as session:
        one_person = session.query(person).first()  
        print(one_person)
        print(one_person.name)
def query_data_by_parms(): # 通过检索筛选 person的属性 找到该数据
    with Session() as session:
        p1 = session.query(person).filter_by(name="jx").first()
        p2 = session.query(person).filter(person.age == "22").first()
        print(p1,p2)
def update_data():         # 找到数据然后修改
    with Session() as session:
        p1 = session.query(person).filter_by(name="jx").first()
        p1.age = 20
        session.commit()
def delete_date():         # 找到数据然后删除
     with Session() as session:
        # 默认删除主表数据时，会将子表的引用主表数据的外键设置Null 可以设置子表外键nullable
        p1 = session.query(person).filter_by(name="jx").first()
        session.delete(p1)
        session.commit()
def query_model():         # query函数的使用
    with Session() as session:
        rs1=session.query(func.count(person.id)).first()
        rs2=session.query(func.sum(person.id)).first()
        rs3=session.query(func.max(person.id)).first()
        rs4=session.query(func.min(person.id)).first()
        print(rs1)
def filter_model():        # filter函数的使用
    with Session() as session:
        person12=session.query(person).filter(person.title == "title1").first()
        person22=session.query(person).filter(person.name != 'ed')
        person32=session.query(person).filter(person.name.like('%ed%'))
        person42=session.query(person).filter(person.name.in_(['ed','wendy','jack']))
        person52=session.query(person).filter(~person.name.in_(['ed','wendy','jack']))
        person62=session.query(person).filter(~person.name.not_in(['ed','wendy','jack']))
        person72=session.query(person).filter(or_(person.name=='ed',person.name=='wendy'))
        person72=session.query(person).filter(and_(person.name=='ed',person.title=='wendy'))
        print(person22)
def quary_outkey_data():   # 通过子表外键反向查找到主表数据
    with Session() as session:
        n1 = session.query(news).first()
        print(n1.person)

        p1 = session.query(person).first()
        print(p1.news)
def query_by_limit():      # limit限制前n条
  with Session() as ses:
    newss = ses.query(new2).limit(3).all()
    for n in newss:
      print(n)
def query_by_offset():     # offset跳过前n条
  with Session() as ses:
    newss = ses.query(new2).offset(3).all()
    for n in newss:
      print(n)     
def query_by_page():       # 分页效果
  # limit topN数据
  # offset 跳过n数据
  # 分页效果  1-3  4-6  7-9  
  # 3  0    1  (pagenum-1)*pagesize
  # 3  3    2  (2-1)*3 = 3
  # 3  6    3  (3-1)*3 = 6
  # 3  9    4  (4-1)*3 = 6
  with Session() as ses:
    # (pagenum-1)*pagesize
    newss = ses.query(new2).limit(3).offset(3).all()
    for n in newss:
      print(n) 
def query_by_slice():      # 从哪个索引开始,到哪个索引结束
  with Session() as ses:
    newss = ses.query(new2).slice(3,6).all()
    for n in newss:
      print(n) 
def query_by_qiepian():    # 从哪个索引开始,到哪个索引结束
  with Session() as ses:

    newss = ses.query(new2).all()[3:6]
    for n in newss:
      print(n) 
def query_lazy():          # lazy='dynamic'一对多 多对多数据过多的情况
  # 'lazy = select 默认不能2次过滤'
  with Session() as ses:
    users = ses.query(news).all()
    newss = users[-1].newss.filter(news.read_count >500 ).all()
    print(newss)
def query_by_age():        # 统计 每个年龄的人数
  with Session() as ses:
    user = ses.query(person.age,func.count(person.id)).group_by(person.age).all()
    print(user)
def query_by_age_gt_18():  # 统计 每个年龄的人数，要求排除未成年人
  with Session() as ses:
    user = ses.query(person.age,func.count(person.id)).group_by(person.age).having(person.age>18).all()
    print(user)
def oper2():               # 子查询
  with Session() as session:
    stmt = session.query(person.city.label('city'), person.age.label('age')).filter(person.uname == '一哥').subquery()
    result = session.query(person).filter(person.city == stmt.c.city, person.age == stmt.c.age).all()
    print(result) # 查看结果






















if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)