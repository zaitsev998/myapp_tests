from sqlalchemy import Column, Integer, VARCHAR, null, SMALLINT, DATETIME, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestUser(Base):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(16), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(64), nullable=False, unique=True)
    access = Column(SMALLINT, default=null)
    active = Column(SMALLINT, default=null)
    start_active_time = Column(DATETIME, default=null)

    UniqueConstraint(email, name='email')
    UniqueConstraint(username, name='ix_test_users_username')

    def __repr__(self):
        return f"<LogRecord(" \
               f"id='{self.id}'," \
               f"username='{self.username}'," \
               f"password='{self.password}'," \
               f"email='{self.email}'," \
               f"access='{self.access}'," \
               f"active='{self.active}'," \
               f"start_active_time='{self.start_active_time}'," \
               f")>"