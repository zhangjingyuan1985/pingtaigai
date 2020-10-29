from sqlalchemy import Column, String, BIGINT, DATETIME, INT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KafkaLog(Base):
    __tablename__ = 't_kafka_log'
    id = Column(BIGINT, primary_key=True, autoincrement=True, comment='mysql虚拟主键 自增')
    brokers = Column(String(512), nullable=False, comment='Kafka brokers')
    group_id = Column(String(32), nullable=True, comment='Kafka组id')
    topic = Column(String(32), nullable=False, comment='Kafka topic')
    partition = Column(String(32), nullable=False, comment='Kafka 分区')
    offset = Column(INT, nullable=False, comment='Kafka 当前消费的offset')
    create_time = Column(DATETIME, nullable=False, comment='topic创建时间')
    consume_time = Column(DATETIME, nullable=True, comment='消费时间')
    status = Column(INT, nullable=False, default=0, comment='消费状态, {0: 未消费, 1:已消费}')
    consume_count = Column(BIGINT, nullable=True, default=0, comment="消费次数")

    def __init__(self, brokers, group_id, topic, partition, offset, create_time):
        self.brokers = brokers
        self.group_id = group_id
        self.topic = topic
        self.partition = partition
        self.offset = offset
        self.create_time = create_time


class KafkaOffset(Base): 
    __tablename__ = "t_kafka_offset"

    id = Column(BIGINT, primary_key=True, autoincrement=True, comment='mysql虚拟主键 自增')
    brokers = Column(String(512), nullable=False, comment='Kafka brokers')
    group_id = Column(String(32), nullable=True, comment='Kafka组id')
    topic = Column(String(32), nullable=False, comment='Kafka topic')
    partition = Column(String(32), nullable=False, comment='Kafka 分区')
    offset = Column(INT, nullable=False, comment='Kafka 当前消费的offset')
    consume_time = Column(DATETIME, nullable=True, comment='消费时间')

    def __init__(self, brokers, group_id, topic, partition, offset, consume_time):
        self.brokers = brokers
        self.group_id = group_id
        self.topic = topic
        self.partition = partition
        self.offset = offset
        self.consume_time = consume_time
