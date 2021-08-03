from warehouse.models import product_info, parameter_info, measure_plan_info, control_plan_info, warehouse_info
from warehouse.models import ValueTypeChoices, GraphTypeChoices
from warehouse.util.utils import UNK, product_uid, par_uid, measure_plan_uid, control_plan_uid, DEBUG

# ////////////////////////////////////////////////////////////
# 产品相关
# ////////////////////////////////////////////////////////////

def addProduct(name, type=UNK, description=None, defaultMeasurePlan=True, sample_size=5, batch_count=25, **kwargs):
    """
    add product_info, add measure_plan
    if sample_size is None, parameter's model should be either 'e' or 'u'
    """
    product = None

    try:
        product = product_info(next(product_uid), name, type, description)
        product.save()

        if DEBUG:
            print('\nAdd product')
            print('---------------------------------------')
            print('uid: ', product.uid)
            print('name: ', product.name)
            print('type: ', product.type)

        if defaultMeasurePlan:
            _addMeasurePlan(product.uid, sample_size, batch_count)
        return product

    except Exception as e:
        if product:
            product.delete()
        if DEBUG:
            print('Add product failed')
        raise e


def alterProduct(product_id, **kwargs):
    """
    alter product_info
    only name and model could be altered
    """
    product = product_info.objects.get(uid=product_id)

    if 'name' in kwargs:
        product.name = kwargs.pop('name')
    if 'type' in kwargs:
        product.type = kwargs.pop('type')
    if 'description' in kwargs:
        product.description = kwargs.pop('description')
    product.save()

    if DEBUG:
        print('\nAlter product')
        print('---------------------------------------')
        print('uid: ', product.uid)
        print('name: ', product.name)
        print('model: ', product.type)

    return product


def delProduct(product_id):
    if DEBUG:
        print('\nDelete product, uid = ', product_id)
    return product_info.objects.get(uid=product_id).delete()

# ////////////////////////////////////////////////////////////
# 车间(控制计划)相关
# ////////////////////////////////////////////////////////////

def _addMeasurePlan(product_id, sample_size=5, batch_count=25, **kwargs):
    """
    add measure plan
    a product can have multiple measure plans
    """
    measure_plan = None

    try:
        measure_plan = measure_plan_info(next(measure_plan_uid), product_id, sample_size, None, batch_count)
        measure_plan.save()

        if DEBUG:
            print('\nAdd measure plan')
            print('---------------------------------------')
            print('uid: ', measure_plan.uid)
            print('product: ', measure_plan.product)
            print('sample_size: ', measure_plan.sample_size)
            print('current_uid: ', measure_plan.current_uid)
            print('batch_count: ', measure_plan.batch_count)

        return measure_plan

    except Exception as e:
        if measure_plan:
            measure_plan.delete()
        if DEBUG:
            print('Add measure plan failed')
        raise e


def _alterMeasurePlan(plan_id, **kwargs):
    """
    alter measure plan
    only batch count could be altered
    """
    measure_plan = measure_plan_info.objects.get(uid=plan_id)

    if 'batch_count' in kwargs:
        measure_plan.batch_count = kwargs.pop('batch_count')
    measure_plan.save()

    if DEBUG:
        print('\nAlter measure plan')
        print('---------------------------------------')
        print('uid: ', measure_plan.uid)
        print('product: ', measure_plan.product)
        print('sample_size: ', measure_plan.sample_size)
        print('current_uid: ', measure_plan.current_uid)
        print('batch_count: ', measure_plan.batch_count)

    return measure_plan


def _delMeasurePlan(plan_id):
    if DEBUG:
        print('\nDelete measure plan, uid = ', plan_id)
    return measure_plan_info.objects.get(uid=plan_id).delete()

# def addWorkshop(name=UNK,productId=None,batchSize=5,windowSize=25,description=None,worker=None, **kwargs):
#     """
#     workshop dont have id, it is bounded with measureplan
#     """
#     measure_plan = None
#     workshop = None
#     try:
#         measure_plan = _addMeasurePlan(productId,batchSize,windowSize,**kwargs)
#         workshop = workshop_info(measure_plan.uid,name,description,worker)
#         workshop.save()
#
#         if DEBUG:
#             print('\nAdd workshop')
#             print('---------------------------------------')
#             print('name: ', name)
#             print('description: ', description)
#             print('worker: ', worker)
#
#         return workshop
#
#     except Exception as e:
#         if measure_plan:
#             measure_plan.delete()
#         if workshop:
#             workshop.delete()
#         if DEBUG:
#             print('Add workshop failed')
#         raise e
#
# def alterWorkshop(plan_id,**kwargs):
#     measure_plan = _alterMeasurePlan(plan_id,**kwargs)
#     workshop = workshop_info.objects.get(measure_plan = measure_plan)
#     if DEBUG:
#         print('\nAlter workshop')
#         print('---------------------------------------')
#         print('name: ', workshop.name)
#         print('description: ', workshop.description)
#         print('worker: ', workshop.worker)
#
#     return workshop
#
# def delWorkshop(plan_id):
#     if DEBUG:
#         print('\nDelete workshop')
#     return _delMeasurePlan(plan_id)

# ////////////////////////////////////////////////////////////
# 参数相关
# ////////////////////////////////////////////////////////////

def addParameter(product_id, name, parameter_id=None, value_type=ValueTypeChoices.UNCOUNTABLE, scale='5', unit=UNK,
                 desctiption=None,
                 graph_type=GraphTypeChoices.Xbar_R, usl=None, lsl=None, **kwargs):
    """
    add parameter_info, add control_plan, add control_graphs
    """
    par = None
    try:
        if parameter_id is None:
            product = product_info.objects.get(uid=product_id)
            parameter_id = len(product.parameters.all())
        if value_type == ValueTypeChoices.UNCOUNTABLE:
            if graph_type not in (GraphTypeChoices.Xbar_R, GraphTypeChoices.Xbar_s, GraphTypeChoices.I_MR):
                raise Exception('variable charts for subgroups could not be applied for individuals')
        else:
            if graph_type not in (GraphTypeChoices.p, GraphTypeChoices.np, GraphTypeChoices.c, GraphTypeChoices.u):
                raise Exception('variable charts for individuals could not be applied for subgroups')

        par = parameter_info(next(par_uid), parameter_id, product_id, name, value_type, scale, unit, desctiption)
        control_plan = control_plan_info(next(control_plan_uid), par.uid, graph_type, usl, lsl)
        par.save()
        control_plan.save()

        if DEBUG:
            print('\nAdd parameter')
            print('---------------------------------------')
            print('uid: ', par.uid)
            print('parameter_id: ', par.parameter_id)
            print('product: ', par.product)
            print('name: ', par.name)
            print('value_type: ', par.value_type)
            print('scale: ', par.scale)
            print('unit: ', par.unit)
            print('description: ', par.description)
            print('\nControl plan:')
            print('uid: ', control_plan.uid)
            print('type: ', control_plan.get_type_display())
            print('usl: ', control_plan.usl)
            print('lsl: ', control_plan.lsl)

        return par

    except Exception as e:
        if par:
            par.delete()
        if DEBUG:
            print('\nAdd parameter failed')
        raise e


def alterParameter(par_id, **kwargs):
    """
    alter parameter info
    graph type is not recommended to change
    """
    try:
        par = parameter_info.objects.get(uid=par_id)
        if 'name' in kwargs:
            par.name = kwargs.pop('name')
        if 'scale' in kwargs:
            par.scale = kwargs.pop('scale')
        if 'unit' in kwargs:
            par.unit = kwargs.pop('unit')
        if 'description' in kwargs:
            par.description = kwargs.pop('description')

        control_plan = None
        if 'usl' in kwargs:
            control_plan = par.control_plan
            control_plan.usl = kwargs.pop('usl')
        if 'lsl' in kwargs:
            control_plan = control_plan if control_plan else par.control_plan
            control_plan.lsl = kwargs.pop('lsl')
        if 'graph_type' in kwargs:
            type = kwargs.pop('graph_type')
            control_plan = control_plan if control_plan else par.control_plan
            if type == control_plan.type:
                pass
            elif par.value_type == ValueTypeChoices.UNCOUNTABLE:
                assert type in (0, 1)
            else:
                assert type in (3, 4, 5, 6)
            control_plan.type = type
        par.save()

        if DEBUG:
            print('\nAlter parameter')
            print('---------------------------------------')
            print('uid: ', par.uid)
            print('parameter_id: ', par.parameter_id)
            print('product: ', par.product)
            print('name: ', par.name)
            print('value_type: ', par.value_type)
            print('scale: ', par.scale)
            print('unit: ', par.unit)
            print('description: ', par.description)
            if control_plan:
                print('\nControl plan:')
                print('uid: ', control_plan.uid)
                print('type: ', control_plan.get_type_display())
                print('usl: ', control_plan.usl)
                print('lsl: ', control_plan.lsl)

        return par

    except Exception as e:
        if DEBUG:
            print('Alter parameter failed')
        raise e


def delParameter(par_id):
    if DEBUG:
        print('Delete parameter, uid = ', par_id)
    return parameter_info.objects.get(uid=par_id).delete()
