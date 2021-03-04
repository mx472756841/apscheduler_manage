#!/usr/bin/python3
# -*- coding: utf-8
""" 
@author: mengx@funsun.cn 
@file: common.py.py
@time: 2019/4/16 9:59
"""
import logging

from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FilterLike, FilterEqual

from app.models import db, ApschedulerJobInfo, ApschedulerJobEventInfo

logger = logging.getLogger(__name__)


class ApschedulerJobInfoView(ModelView):
    """ apscheduler 任务管理 """
    extra_css = []

    extra_js = []

    list_template = 'apscheduler_job_info_list.html'

    # 创建窗口，不使用modal
    create_modal = False
    can_create = False
    # 编辑窗口，不使用modal
    edit_modal = False
    can_edit = False
    # 是否可以删除
    can_delete = False
    page_size = 20
    can_set_page_size = True
    # 是否可以看详情
    can_view_details = True

    # 配置列表中要展示的字段
    column_list = [
        "id", "job_id", "job_name", "job_trigger", "job_next_run_time", "job_status",
        "events", "create_time", "update_time"
    ]

    # 配置各字段在页面中的中文显示
    column_labels = {
        "id": "id",
        "events": "执行事件",
        "job_id": "任务ID",
        "job_name": "任务描述",
        "job_trigger": "触发器",
        "job_func": "执行函数",
        "job_next_run_time": "执行时间",
        "job_status": "状态",
        "create_time": "创建时间",
        "update_time": "更新时间",
        "job_traceback": "执行异常信息"
    }
    # 初始化排序
    column_default_sort = [('id', True)]

    # 页面筛选
    column_filters = [
        FilterLike(column=ApschedulerJobInfo.job_name, name='任务描述'),
        FilterEqual(column=ApschedulerJobInfo.job_id, name='任务ID'),
    ]

    # 页面中可排序的字段
    column_sortable_list = ["id", "update_time"]

    column_formatters = dict(
        job_status=lambda v, c, m, p: m.JOB_STATUS_MAPPING.get(m.job_status, "错误数据"),
        job_name=lambda v, c, m, p: m.COMMON_JOB_NAME_MAPPING.get(m.job_name, m.job_name),
        events=lambda v, c, m, p: len(m.events),
    )

    # 详细中的展示
    column_details_list = ["id", "job_id", "job_name", "job_trigger", "job_func", "job_traceback"]


class ApschedulerJobEventInfoView(ModelView):
    """ apscheduler 任务管理 """
    extra_css = [
    ]

    extra_js = []

    # 创建窗口，不使用modal
    create_modal = False
    can_create = False
    # 编辑窗口，不使用modal
    edit_modal = False
    can_edit = False
    # 是否可以删除
    can_delete = False
    page_size = 20
    can_set_page_size = True

    # 配置列表中要展示的字段
    column_list = ["id", "job_info.job_id", "event", "create_time"]

    # 配置各字段在页面中的中文显示
    column_labels = {
        "id": "ID",
        "event": "执行事件",
        "job_info.job_id": "任务ID",
        "job_info.job_name": "任务描述",
        "create_time": "执行时间"
    }
    # 初始化排序
    column_default_sort = [('id', True)]

    # 页面筛选
    column_filters = [
        FilterEqual(column=ApschedulerJobInfo.id, name='任务本地ID'),
        FilterEqual(column=ApschedulerJobInfo.job_id, name='任务ID'),
    ]

    # 页面中可排序的字段
    column_sortable_list = ["id"]

    column_formatters = dict(
        event=lambda v, c, m, p: m.EVENT_MAPPING.get(m.event, m.event),
    )


views = [
    ApschedulerJobInfoView(ApschedulerJobInfo, db.session, name="任务管理", category="apscheduler管理",
                           endpoint="apscheduler_job_manage"),
    ApschedulerJobEventInfoView(ApschedulerJobEventInfo, db.session, name="任务执行明细", category="apscheduler管理",
                                endpoint="apscheduler_job_event_manage")
]
