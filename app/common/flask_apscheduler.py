import threading

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_MAX_INSTANCES, EVENT_ALL_JOBS_REMOVED, \
    EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED, EVENT_JOB_EXECUTED, EVENT_JOB_SUBMITTED
from flask_apscheduler.scheduler import APScheduler, LOGGER

from app.models import ApschedulerJobInfo, ApschedulerJobEventInfo


class CustomAPScheduler(APScheduler):
    # scheduler事件映射本地状态
    STATUS_MAPPING = {
        EVENT_JOB_ADDED: 0,
        EVENT_JOB_MODIFIED: 1,
        EVENT_JOB_SUBMITTED: 2,
        EVENT_JOB_EXECUTED: 3,
        EVENT_JOB_REMOVED: 4,
        EVENT_JOB_ERROR: 5,
        EVENT_JOB_MISSED: 6,
        EVENT_ALL_JOBS_REMOVED: 7,
        EVENT_JOB_MAX_INSTANCES: 8
    }

    def __init__(self, session, scheduler=None, app=None):
        super(CustomAPScheduler, self).__init__(scheduler, app)
        self.session = session

    def listener_all_job(self, event):
        """
        监控job的生命周期，可视化监控，并且可增加后续的没有触发任务等监控
        添加到线程做处理
        :param event:
        :return:
        """
        job_id = None
        args = []
        if event.code != EVENT_ALL_JOBS_REMOVED:
            job_id = event.job_id
        if job_id:
            jobstore_alias = event.jobstore
            job = self.scheduler.get_job(job_id, jobstore_alias)
            if job:
                name = job.name
                func = str(job.func_ref)
                trigger = job.trigger if isinstance(job.trigger, str) else str(job.trigger).split("[")[0]
                next_run_time = str(job.next_run_time).split(".")[0]
            else:
                name = None
                func = None
                trigger = None
                next_run_time = None
            args = [name, func, trigger, next_run_time]
        traceback = event.traceback if hasattr(event, 'traceback') else "",
        args.append(traceback)
        t = threading.Thread(target=self.handle_listener_all_job, args=[event.code, job_id, *args])
        t.start()
        t.join()

    def handle_listener_all_job(self, event_type, *args):
        """
        实际处理IO操作
        如何处理一个job_id重复使用的问题，采用本地id自增，如果真有job_id重复的情况，则认为指定的是最后一个job_id对应的任务
        """
        try:
            if event_type == EVENT_JOB_ADDED:
                # 添加任务定义表
                job = ApschedulerJobInfo()
                job.job_id = args[0]
                job.job_name = args[1]
                job.job_func = args[2]
                job.job_trigger = args[3]
                job.job_next_run_time = args[4]
                job.job_status = 0
                self.session.add(job)
                self.session.flush()
                # 增加任务事件表
                job_event = ApschedulerJobEventInfo()
                job_event.job_info_id = job.id
                job_event.event = self.STATUS_MAPPING[event_type]
                self.session.add(job_event)
                self.session.commit()
            elif event_type == EVENT_JOB_MODIFIED:
                # 修改job[取数据库表中job_id最后一个进行修改]
                job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                    ApschedulerJobInfo.job_id == args[0]).first()
                if job:
                    # 更新JOB表
                    job.job_name = args[1]
                    job.job_func = args[2]
                    job.job_trigger = args[3]
                    job.job_next_run_time = args[4]
                    job.job_status = 0

                    # 增加任务事件表
                    job_event = ApschedulerJobEventInfo()
                    job_event.job_info_id = job.id
                    job_event.event = self.STATUS_MAPPING[event_type]
                    self.session.add(job_event)
                    self.session.commit()
                else:
                    LOGGER.warning("指定的job本地不存在{}".format(args))
            elif event_type == EVENT_JOB_SUBMITTED:
                # 提交job执行
                job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                    ApschedulerJobInfo.job_id == args[0]).first()
                if job:
                    # 增加任务事件表
                    job_event = ApschedulerJobEventInfo()
                    job_event.job_info_id = job.id
                    job_event.event = self.STATUS_MAPPING[event_type]
                    self.session.add(job_event)
                    self.session.commit()
                else:
                    LOGGER.warning("指定的job本地不存在{}".format(args))
            elif event_type == EVENT_JOB_EXECUTED:
                # 执行job
                job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                    ApschedulerJobInfo.job_id == args[0]).first()
                if job:
                    # 更新JOB表
                    job.job_status = 1

                    # 增加任务事件表
                    job_event = ApschedulerJobEventInfo()
                    job_event.job_info_id = job.id
                    job_event.event = self.STATUS_MAPPING[event_type]
                    self.session.add(job_event)
                    self.session.commit()
                else:
                    LOGGER.warning("指定的job本地不存在{}".format(args))
            elif event_type == EVENT_JOB_REMOVED:
                # 删除job
                job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                    ApschedulerJobInfo.job_id == args[0]).first()
                if job:
                    # 更新JOB表
                    job.job_status = 5

                    # 增加任务事件表
                    job_event = ApschedulerJobEventInfo()
                    job_event.job_info_id = job.id
                    job_event.event = self.STATUS_MAPPING[event_type]
                    self.session.add(job_event)
                    self.session.commit()
                else:
                    LOGGER.warning("指定的job本地不存在{}".format(args))
            elif event_type == EVENT_JOB_ERROR:
                # 执行job出错
                job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                    ApschedulerJobInfo.job_id == args[0]).first()
                if job:
                    # 更新JOB表
                    job.job_status = 2
                    job.job_traceback = args[5]
                    # 增加任务事件表
                    job_event = ApschedulerJobEventInfo()
                    job_event.job_info_id = job.id
                    job_event.event = self.STATUS_MAPPING[event_type]
                    self.session.add(job_event)
                    self.session.commit()
                else:
                    LOGGER.warning("指定的job本地不存在{}".format(args))
            elif event_type == EVENT_JOB_MISSED:
                # job执行错过
                job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                    ApschedulerJobInfo.job_id == args[0]).first()
                if job:
                    # 更新JOB表
                    job.job_status = 3
                    job.job_traceback = args[5]
                    # 增加任务事件表
                    job_event = ApschedulerJobEventInfo()
                    job_event.job_info_id = job.id
                    job_event.event = self.STATUS_MAPPING[event_type]
                    self.session.add(job_event)
                    self.session.commit()
                else:
                    LOGGER.warning("指定的job本地不存在{}".format(args))
            elif event_type == EVENT_ALL_JOBS_REMOVED:
                # 删除所有job
                all_jobs = ApschedulerJobInfo.query.filter(ApschedulerJobInfo.job_status == 0).all()
                for job in all_jobs:
                    job.job_status = 6
                    # 增加任务事件表
                    job_event = ApschedulerJobEventInfo()
                    job_event.job_info_id = job.id
                    job_event.event = self.STATUS_MAPPING[event_type]
                    self.session.add(job_event)
                    self.session.commit()
            elif event_type == EVENT_JOB_MAX_INSTANCES:
                # job超过最大实例
                job = ApschedulerJobInfo.query.order_by(ApschedulerJobInfo.id.desc()).filter(
                    ApschedulerJobInfo.job_id == args[0]).first()
                if job:
                    # 更新JOB表
                    job.job_status = 4
                    job.job_traceback = args[5]
                    # 增加任务事件表
                    job_event = ApschedulerJobEventInfo()
                    job_event.job_info_id = job.id
                    job_event.event = self.STATUS_MAPPING[event_type]
                    self.session.add(job_event)
                    self.session.commit()
                else:
                    LOGGER.warning("指定的job本地不存在{}".format(args))
        except:
            LOGGER.exception("执行任务异常")

    def init_app(self, app):
        super(CustomAPScheduler, self).init_app(app)

        # 增加监听函数，监听所有job的生命周期
        self.add_listener(self.listener_all_job,
                          EVENT_JOB_ERROR | EVENT_JOB_MISSED | EVENT_JOB_MAX_INSTANCES | EVENT_ALL_JOBS_REMOVED | EVENT_JOB_ADDED | EVENT_JOB_REMOVED | EVENT_JOB_MODIFIED | EVENT_JOB_EXECUTED | EVENT_JOB_SUBMITTED)
