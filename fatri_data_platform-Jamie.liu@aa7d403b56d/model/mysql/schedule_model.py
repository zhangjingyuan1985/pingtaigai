from sqlalchemy import Column, String, BIGINT, DATETIME, INT, Enum, SMALLINT, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TaskInfoConf(Base):

    __tablename__ = 't_task_info_conf'
    ID = Column(BIGINT, primary_key=True, autoincrement=True, comment='mysql虚拟主键 自增')
    TASK_ID = Column(BIGINT, nullable=False, comment='调度任务ID 规则8位代码 (qa:00+任务序号; ods:10++任务序号; '
                                                           'fods:20++任务序号 ;dwd:30++任务序号; dws:35++任务序号; '
                                                           'ads:40+任务序号; fs:50+任务序号; al:60+任务序号)')
    TASK_NAME = Column(String(512), nullable=False, comment='调度任务名称')
    TARGET_DB = Column(String(32), nullable=False, comment='目标库')
    TARGET_TABLE = Column(String(32), nullable=False, comment='目标表')
    TASK_TYPE = Column(String(3), nullable=False, comment='调度任务类型 d 日 w 周 m 月 y 年')
    START_MODE = Column(Enum(0, 1, 2, 3), nullable=False, comment='启动方式 0:随初始化启动 1:依赖启动 2:定时启动 3:混合启动')
    PRI_WEIGHT = Column(SMALLINT, nullable=False, default=100, comment='任务优先级权重')
    COMMENT = Column(String(512), comment='说明')
    STATUS = Column(Enum(0, 1, 2), nullable=False, comment='状态 0:未启用 1:在用 2:失效')
    CREATE_BY = Column(String(20), nullable=False, comment='创建人')
    CREATE_TIME = Column(DATETIME, nullable=False, comment='创建时间')
    UPDATE_BY = Column(String(20), comment='更新人')
    UPDATE_TIME = Column(DATETIME, comment='更新时间')

    def __init__(self, task_id, task_name, target_db, target_table, task_type, start_mode, pri_weight,
                 comment, status, create_by, create_time, update_by, update_time):
        self.TASK_ID = task_id
        self.TASK_NAME = task_name
        self.TARGET_DB = target_db
        self.TARGET_TABLE = target_table
        self.TASK_TYPE = task_type
        self.START_MODE = start_mode
        self.PRI_WEIGHT = pri_weight
        self.COMMENT = comment
        self.STATUS = status
        self.CREATE_BY = create_by
        self.CREATE_TIME = create_time
        self.UPDATE_BY = update_by
        self.UPDATE_TIME = update_time


class TaskArgsConf(Base):

    __tablename__ = 't_task_args_conf'
    ID = Column(BIGINT, primary_key=True, autoincrement=True, comment='mysql虚拟主键 自增')
    TASK_ID = Column(BIGINT, nullable=False, comment='调度任务ID')
    INNER_SORT = Column(String(512), nullable=False, comment='任务参数序号 从0开始')
    TASK_ARGUMENT = Column(String(512), nullable=False, comment='任务参数')
    COMMENT = Column(String(512), comment='说明')
    STATUS = Column(Enum(0, 1, 2), nullable=False, comment='状态 0:未启用 1:在用 2:失效')
    CREATE_BY = Column(String(20), nullable=False, comment='创建人')
    CREATE_TIME = Column(DATETIME, nullable=False, comment='创建时间')
    UPDATE_BY = Column(String(20), comment='更新人')
    UPDATE_TIME = Column(DATETIME, comment='更新时间')

    def __init__(self, task_id, inner_sort, task_argument,
                 comment, status, create_by, create_time, update_by, update_time):
        self.TASK_ID = task_id
        self.INNER_SORT = inner_sort
        self.TASK_ARGUMENT = task_argument
        self.COMMENT = comment
        self.STATUS = status
        self.CREATE_BY = create_by
        self.CREATE_TIME = create_time
        self.UPDATE_BY = update_by
        self.UPDATE_TIME = update_time


class TaskRelaConf(Base):

    __tablename__ = 't_task_rela_conf'
    ID = Column(BIGINT, primary_key=True, autoincrement=True, comment='mysql虚拟主键 自增')
    CURR_TASK_ID = Column(BIGINT, nullable=False, comment='当前任务ID')
    DEPD_TASK__ID = Column(String(512), nullable=False, comment='依赖任务ID')
    COMMENT = Column(String(512), comment='说明')
    STATUS = Column(Enum(0, 1, 2), nullable=False, comment='状态 0:未启用 1:在用 2:失效')
    CREATE_BY = Column(String(20), nullable=False, comment='创建人')
    CREATE_TIME = Column(DATETIME, nullable=False, comment='创建时间')
    UPDATE_BY = Column(String(20), comment='更新人')
    UPDATE_TIME = Column(DATETIME, comment='更新时间')

    def __init__(self, curr_task_id, depo_task_id,
                 comment, status, create_by, create_time, update_by, update_time):
        self.CURR_TASK_ID = curr_task_id
        self.DEPD_TASK__ID = depo_task_id
        self.COMMENT = comment
        self.STATUS = status
        self.CREATE_BY = create_by
        self.CREATE_TIME = create_time
        self.UPDATE_BY = update_by
        self.UPDATE_TIME = update_time


class TaskInst(Base):

    __tablename__ = 't_task_inst'
    ID = Column(BIGINT, primary_key=True, autoincrement=True, comment='mysql虚拟主键 自增')
    INST_ID = Column(BIGINT, nullable=False, comment='任务实例ID  任务类型(10日 20周 30月 40年)'
                                                           '+yyyymmdd+task_id(补齐8位)')
    TASK_ID = Column(String(512), nullable=False, comment='调度任务ID')
    REPEAT_CNT = Column(SMALLINT, nullable=False, default=0, comment='重跑次数(累加)')
    TARGET_TABLE = Column(String(32), nullable=False, comment='目标表')
    TASK_TYPE = Column(String(3), nullable=False, comment='调度任务类型 d 日 w 周 m 月 y 年')
    START_MODE = Column(Enum(0, 1, 2, 3), nullable=False, comment='启动方式 0:随初始化启动 1:依赖启动 2:定时启动 3:混合启动')
    TASK_STATUS = Column(Enum(0, 1, 2, 9), nullable=False, default=0, comment='状态 0:未执行 1:执行中 2:完成 9:失败')
    CREATE_BY = Column(String(20), nullable=False, comment='创建人')
    CREATE_TIME = Column(DATETIME, nullable=False, comment='创建时间')
    UPDATE_BY = Column(String(20), comment='更新人')
    UPDATE_TIME = Column(DATETIME, comment='更新时间')

    def __init__(self, task_id, task_name, target_db, target_table, task_type, start_mode, pri_weight,
                 comment, status, create_by, create_time, update_by, update_time):
        self.TASK_ID = task_id
        self.TASK_NAME = task_name
        self.TARGET_DB = target_db
        self.TARGET_TABLE = target_table
        self.TASK_TYPE = task_type
        self.START_MODE = start_mode
        self.PRI_WEIGHT = pri_weight
        self.COMMENT = comment
        self.STATUS = status
        self.CREATE_BY = create_by
        self.CREATE_TIME = create_time
        self.UPDATE_BY = update_by
        self.UPDATE_TIME = update_time


class TaskLog(Base):

    __tablename__ = 't_task_log'
    ID = Column(BIGINT, primary_key=True, autoincrement=True, comment='mysql虚拟主键 自增')
    DATE_ID = Column(String(10), comment='日期编号，如果是按日跑批就用DAY_ID,月跑批就是MONTH_ID')
    INST_ID = Column(BIGINT, comment='任务实例ID  yyyymmdd+task_id(补齐6位)')
    PROC_FILE = Column(String(200), nullable=False, comment='存储过程文件')
    TARGET_DB = Column(String(32), nullable=False, comment='目标库')
    TARGET_TABLE = Column(String(32), nullable=False, comment='目标表')
    REPEAT_CNT = Column(SMALLINT, nullable=False, default=0, comment='重跑次数(累加)')
    STEP_STATUS = Column(String(3), nullable=False, comment='步骤状态 如果正常输出步骤编号，如果异常输出-1')
    START_TIME = Column(DATETIME, nullable=False, default=0, comment='创建时间')
    END_TIME = Column(DATETIME, nullable=False, comment='结束时间')
    DURING = Column(INT, nullable=False, comment='持续时间')
    COMMAND = Column(String(2000), comment='当前步骤执行的shell命令或sql')
    OUTPUT = Column(TEXT(4000), comment='输出内容')
    CREATE_BY = Column(String(20), comment='创建人')
    CREATE_TIME = Column(DATETIME, comment='创建时间')

    def __init__(self, date_id, inst_id, proc_file, target_db, target_table, repeat_cnt, step_status, start_time,
                 end_time, during, command, output, create_by, create_time):
        self.DATE_ID = date_id
        self.INST_ID = inst_id
        self.PROC_FILE = proc_file
        self.TARGET_DB = target_db
        self.TARGET_TABLE = target_table
        self.REPEAT_CNT = repeat_cnt
        self.STEP_STATUS = step_status
        self.START_TIME = start_time
        self.END_TIME = end_time
        self.DURING = during
        self.COMMAND = command
        self.OUTPUT = output
        self.CREATE_BY = create_by
        self.CREATE_TIME = create_time


class TaskCrontabConf(Base):

    __tablename__ = 't_task_crontab_conf'
    ID = Column(BIGINT, primary_key=True, autoincrement=True, comment='mysql虚拟主键 自增')
    MINUTE = Column(String(20), nullable=False,comment='第几分钟')
    HOUR = Column(String(32), nullable=False, comment='第几小时')
    DAY = Column(String(32), nullable=False, comment='第几天')
    MONTH = Column(String(32), nullable=False, comment='第几个月')
    WEEK = Column(String(32), nullable=False, comment='星期几')
    COMMENT = Column(String(512), comment='说明')
    STATUS = Column(Enum(0, 1, 2), nullable=False, comment='状态 0:未启用 1:在用 2:失效')
    CREATE_BY = Column(String(20), nullable=False, comment='创建人')
    CREATE_TIME = Column(DATETIME, nullable=False, comment='创建时间')
    UPDATE_BY = Column(String(20), comment='更新人')
    UPDATE_TIME = Column(DATETIME, comment='更新时间')

    def __init__(self, minute, hour, day, month, week,
                 comment, status, create_by, create_time, update_by, update_time):
        self.MINUTE = minute
        self.HOUR = hour
        self.DAY = day
        self.MONTH = month
        self.WEEK = week
        self.COMMENT = comment
        self.STATUS = status
        self.CREATE_BY = create_by
        self.CREATE_TIME = create_time
        self.UPDATE_BY = update_by
        self.UPDATE_TIME = update_time
