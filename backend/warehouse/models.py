from django.db import models
from django.db.models.fields import validators
from django.contrib.auth.models import AbstractUser
from user.models import *


# ////////////////////////////////////////////////////////////
# 仓储相关
# ////////////////////////////////////////////////////////////

class warehouse_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='仓库编号'
                           )
    name = models.CharField(max_length=20,
                            help_text='仓库名称'
                            )
    users = models.ManyToManyField(user_account_info,related_name='warehouses')


class storage_cell_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='储位编号'
                           )
    warehouse = models.ForeignKey(warehouse_info, on_delete=models.CASCADE,
                                  db_index=True,
                                  related_name="storagecells",
                                  related_query_name='storagecell',
                                  help_text='从属仓库'
                                  )
    capacity = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                   help_text='容量'
                                   )
    occupy = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                 help_text='占用'
                                 )

class product_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='产品编号'
                           )
    name = models.CharField(max_length=20,
                            help_text='产品名称'
                            )
    type = models.CharField(max_length=30,
                            help_text='产品型号'
                            )
    description = models.CharField(max_length=256, null=True,
                                   help_text='产品描述'
                                   )

    def __str__(self):
        return self.name


class entry_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='入库单编号'
                           )
    entry_time = models.DateTimeField(help_text='入库时间')
    product = models.ForeignKey(product_info, on_delete=models.CASCADE,
                                related_name="entry_info",
                                related_query_name='entry_infos',
                                help_text='零件'
                                )
    cell = models.ForeignKey(storage_cell_info, on_delete=models.SET_NULL,
                             db_index=True,
                             related_name="entry_info",
                             related_query_name='entry_infos',
                             help_text='从属储位'
                             )
    number = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                 help_text='入库数量'
                                 )
    operator = models.ForeignKey(user_account_info, on_delete=models.SET_NULL,
                                 related_name="entry_info",
                                 related_query_name='entry_infos',
                                 help_text='操作员'
                                 )

# ////////////////////////////////////////////////////////////
# 出入库测量相关
# ////////////////////////////////////////////////////////////

class shipment_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='出库单编号'
                           )
    shipping_time = models.DateTimeField(help_text='出库时间')
    product = models.ForeignKey(product_info, on_delete=models.CASCADE,
                                related_name="shipment_info",
                                related_query_name='shipment_infos',
                                help_text='零件'
                                )
    cell = models.ForeignKey(storage_cell_info, on_delete=models.SET_NULL,
                             db_index=True,
                             related_name="shipment_info",
                             related_query_name='shipment_infos',
                             help_text='从属储位'
                             )
    number = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                 help_text='出库数量'
                                 )
    operator = models.ForeignKey(user_account_info, on_delete=models.SET_NULL,
                                 db_index=True,
                                 related_name="shipment_info",
                                 related_query_name='shipment_infos',
                                 help_text='操作员'
                                 )


class storage_cell_product_relationship(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='储位零件关系编号'
                           )
    storage_cell = models.ForeignKey(storage_cell_info, on_delete=models.CASCADE,
                                     db_index=True,
                                related_name="product_info",
                                related_query_name='product_infos',
                                help_text='关联储位'
                                )
    number = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                 help_text='存量'
                                 )
    time = models.DateTimeField(help_text='存储开始时间')

# Create your models here.



class ValueTypeChoices(models.IntegerChoices):
    UNCOUNTABLE = 0, 'UNCOUNTABLE'
    COUNTABLE = 1, 'COUNTABLE'


class parameter_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='参数标识符'
                           )
    parameter_id = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                       help_text='参数编号'
                                       )
    product = models.ForeignKey(product_info, on_delete=models.CASCADE,
                                db_index=True,
                                related_name="parameters",  # product_info.parameters.all()
                                related_query_name='parameter',
                                # product_info.objects.filter(parameter_name='[target]')
                                help_text='从属零件'
                                )
    name = models.CharField(max_length=20,
                            help_text='参数名称'
                            )
    value_type = models.IntegerField(choices=ValueTypeChoices.choices,
                                     help_text='数值类型'
                                     )
    scale = models.CharField(max_length=2,
                             help_text='小数位数'
                             )
    unit = models.CharField(max_length=10,
                            help_text='参数单位'
                            )
    description = models.CharField(max_length=256, null=True,
                                   help_text='参数描述'
                                   )

    def __str__(self):
        return self.name


class GraphTypeChoices(models.IntegerChoices):
    '''控制图类型'''
    Xbar_R = 0, 'Xbar-R'
    Xbar_s = 1, 'Xbar-s'
    I_MR = 2, 'I-MR'
    p = 3, 'p'
    np = 4, 'np'
    c = 5, 'c'
    u = 6, 'u'


class control_plan_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='测量控制计划编号')
    parameter = models.OneToOneField(parameter_info, on_delete=models.CASCADE,
                                     db_index=True, related_name='control_plan',
                                     help_text='关联参数'
                                     )
    type = models.IntegerField(choices=GraphTypeChoices.choices,
                               help_text='控制图类型'
                               )
    usl = models.FloatField(max_length=12, null=True,
                            help_text='上规格界限'
                            )
    lsl = models.FloatField(max_length=12, null=True,
                            help_text='下规格界限'
                            )

    def __str__(self):
        return self.uid


class measure_plan_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='测量计划编号'
                           )
    product = models.ForeignKey(product_info, on_delete=models.CASCADE,
                                db_index=True, related_name='measure_plans',
                                help_text='关联产品'
                                )
    entry_info = models.ForeignKey(entry_info, on_delete=models.CASCADE,
                                related_name='measure_plans',
                                help_text='关联入库单'
                                )
    sample_size = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                      null=True,
                                      help_text='计划样本容量'
                                      )
    current_uid = models.CharField(max_length=11,
                                   help_text='当前批号',
                                   null=True
                                   )
    batch_count = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                      help_text='默认批数'
                                      )
    user = models.ForeignKey(user_account_info, on_delete=models.SET_NULL,
                                 related_name="measure_plan_info",
                                 help_text='从属者'
                                 )

    def __str__(self):
        return self.uid

class measure_form_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='测量单标识符'
                           )
    measure_form_id = models.CharField(max_length=11,
                                       help_text='测量单编号'
                                       )
    measure_plan = models.ForeignKey(measure_plan_info, on_delete=models.CASCADE,
                                     db_index=True,
                                     related_name='measure_forms',
                                     related_query_name='measure_form',
                                     help_text='从属测量计划'
                                     )
    sample_size = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                      null=True,
                                      help_text='测量样本容量'
                                      )
    start_time = models.DateTimeField(help_text='测量起始时间')
    end_time = models.DateTimeField(help_text='测量结束时间')
    # [models.ForeignKey('user_account')
    operator_id = models.CharField(max_length=11, validators=(validators.MinLengthValidator(11),),
                                   help_text='操作者编号'
                                   )

    def __str__(self):
        return self.uid


class parameter_data_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='数据编号'
                           )
    sample_id = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                    help_text='组内样本编号'
                                    )
    measure_form = models.ForeignKey(measure_form_info, on_delete=models.CASCADE,
                                     db_index=True,
                                     related_name='parameter_datas',
                                     related_query_name='parameter_data',
                                     help_text='从属测量单'
                                     )
    parameter = models.ForeignKey(parameter_info, on_delete=models.CASCADE, related_name='+',
                                  help_text='从属测量参数'
                                  )
    value = models.FloatField(max_length=11,
                              help_text='数据数值'
                              )

    def __str__(self):
        return self.uid


class control_point_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='控制点编号'
                           )
    control_plan = models.ForeignKey(control_plan_info, on_delete=models.CASCADE,
                                     db_index=True,
                                     related_name='control_points',
                                     related_query_name='control_point',
                                     help_text='从属控制计划'
                                     )
    measure_form = models.ForeignKey(measure_form_info, on_delete=models.CASCADE,
                                     related_name='control_points',
                                     related_query_name='control_point',
                                     help_text='从属测量单'
                                     )
    sample_size = models.IntegerField(validators=(validators.MinValueValidator(0),),
                                      null=True,
                                      help_text='样本容量'
                                      )
    x = models.FloatField(max_length=12,
                          null=True,
                          help_text='平均值'
                          )
    r = models.FloatField(max_length=12,
                          null=True,
                          help_text='极差'
                          )
    s = models.FloatField(max_length=12,
                          null=True,
                          help_text='标准差'
                          )
    p = models.IntegerField(validators=(validators.MinValueValidator(0),),
                            null=True,
                            help_text='频数'
                            )
    np = models.FloatField(max_length=6,
                           null=True,
                           help_text='频率'
                           )
    c = models.FloatField(max_length=6,
                          null=True,
                          help_text='平均计数'
                          )
    u = models.FloatField(max_length=6,
                          null=True,
                          help_text='平均单位计数'
                          )

    def __str__(self):
        return self.uid


class abnormality_info(models.Model):
    uid = models.CharField(max_length=11,
                           primary_key=True,
                           validators=(validators.MinLengthValidator(11),),
                           help_text='异常信息编号'
                           )
    measure_plan = models.ForeignKey(measure_plan_info, on_delete=models.CASCADE,
                                     related_name='abnormalities',
                                     related_query_name='abnormality',
                                     help_text='关联测量计划')
    control_plan = models.ForeignKey(control_plan_info, on_delete=models.CASCADE,
                                     related_name='+',
                                     help_text='关联控制计划')
    abnormality_id = models.ForeignKey(measure_form_info, on_delete=models.CASCADE,
                                       related_name='+',
                                       help_text='异常测量单编号')
    start_id = models.CharField(max_length=11,
                                help_text='测量单起始编号'
                                )
    end_id = models.CharField(max_length=11,
                              help_text='测量单终止编号'
                              )
    information = models.CharField(max_length=256,
                                   help_text='异常信息描述'
                                   )
    reason = models.CharField(max_length=256,
                              help_text='异常信息原因'
                              )
    if_read = models.BooleanField(help_text='是否已读')
