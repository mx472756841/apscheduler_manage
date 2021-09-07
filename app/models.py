from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class ApschedulerJobInfo(db.Model):
    """
        apscheduler job 定义表
    """
    JOB_STATUS_MAPPING = {
        0: "待执行",
        1: "执行完成",
        2: "执行异常",
        3: "未执行结束",
        4: "系统异常",
        5: "已删除",
        6: "批量删除"
    }

    # 应对历史的job名字映射 函数映射文字
    COMMON_JOB_NAME_MAPPING = {
        "end_before_2hours_notice": "拍卖结束前通知用户",
        "end_auction": "拍卖结束",
        "end_type1_auction": "直播拍卖结束",
        "auction_type1_start_product": "直播拍卖开始",
        "auction_preview_notify": "拍卖预展通知",
        "live_auction_start_notify": "拍卖开拍前提醒",
        "notify_ws": "拍卖开始",
        "heart_beat": "心跳任务",
    }

    __tablename__ = "apscheduler_job_info"
    id = db.Column(db.Integer, primary_key=True, comment="id 主键，用于防止JObID多次使用的情况")
    job_id = db.Column(db.String(200), nullable=False, comment="JOBID")
    job_name = db.Column(db.String(200), comment="JOB名字")
    job_trigger = db.Column(db.String(30), comment="触发类型")
    job_func = db.Column(db.String(200), comment="执行的函数信息")
    job_next_run_time = db.Column(db.String(30), comment="JOB下次执行时间")
    job_status = db.Column(db.Integer, nullable=False, comment="JOB 状态 0:待执行 1:执行完成 2:执行异常 3:未执行结束 4:系统异常 5:已删除 6:批量删除")
    job_traceback = db.Column(db.TEXT, comment="执行报错时的错误信息")
    create_time = db.Column(db.TIMESTAMP(True), default=datetime.now, nullable=False, comment="创建时间")
    update_time = db.Column(db.TIMESTAMP(True), default=datetime.now, onupdate=datetime.now, nullable=False, comment="更新时间")

    def __repr__(self):
        return self.job_id


class ApschedulerJobEventInfo(db.Model):
    """
        apscheduler job 事件表
    """
    EVENT_MAPPING = {
        0: "添加JOB",
        1: "修改JOB",
        2: "提交JOB",
        3: "执行JOB",
        4: "删除JOB",
        5: "执行JOB异常",
        6: "执行JOB过期",
        7: "全量删除JOB",
        8: "JOB超过最大实例数"
    }

    __tablename__ = "apscheduler_job_event_info"
    id = db.Column(db.Integer, primary_key=True, comment="id 主键，用于防止JObID多次使用的情况")
    job_info_id = db.Column(db.Integer, db.ForeignKey('apscheduler_job_info.id'), comment="JOB_INFO_ID")
    job_info = db.relationship("ApschedulerJobInfo", backref='events')
    event = db.Column(db.Integer,
                      comment="JOB事件 0:添加JOB 1:修改JOB 2:提交JOB 3:执行JOB 4:删除JOB 5:执行JOB异常 6:执行JOB过期 7:全量删除JOB 8:JOB超过最大实例数")
    create_time = db.Column(db.TIMESTAMP(True), default=datetime.now, nullable=False, comment="创建时间")

    def __repr__(self):
        return "<<job:{} event:{}>>".format(self.job_info.job_id, self.EVENT_MAPPING.get(self.event, self.event))
