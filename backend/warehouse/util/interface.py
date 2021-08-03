from django.template import loader
from warehouse.util.utils import TEMPLATENAME,CELLSPERPAGE
from warehouse.util.graphCheck import getGraph, getGraphByTime
from warehouse.util.sheduleMake import addProduct, addParameter, alterProduct, alterParameter, delProduct, \
    _addMeasurePlan  # , alterWorkshop, addWorkshop, delWorkshop
from warehouse.models import *
from user.util.interface import verify_decorator

# ////////////////////////////////////////////////////////////
# 仓位图
# ////////////////////////////////////////////////////////////

@verify_decorator()
def getStorageCells(user:user_account_info = None, **kwargs):
    warehouse_id = kwargs['warehouse_id']
    order = kwargs['order']
    page = kwargs['page']
    if warehouse_id == 'all':
        if user.role_warehouse == RoleChoices.ADMIN:
            if order==0:
                cells = storage_cell_info.objects.order_by('warehouse__uid','uid')[page*CELLSPERPAGE-1:(page+1)*CELLSPERPAGE]
            elif order==1: # todo: may have problem
                cells = storage_cell_info.objects.order_by('warehouse__uid','free')[page*CELLSPERPAGE-1:(page+1)*CELLSPERPAGE]
            elif order==2:
                cells = storage_cell_info.objects.order_by('warehouse__uid', '-free')[page * CELLSPERPAGE - 1:(page + 1) * CELLSPERPAGE]
            else:
                raise Exception('unknown order')
        else:
            raise Exception('unauthorized operation')
    else:
        if user.role_warehouse == RoleChoices.ADMIN or warehouse_info.objects.get(uid=warehouse_id).users.filter(uid=user.uid).exists():
            if order==0:
                cells = storage_cell_info.objects.filter(warehouse__uid=warehouse_id).order_by('uid')[page*CELLSPERPAGE-1:(page+1)*CELLSPERPAGE]
            elif order==1:
                cells = storage_cell_info.objects.filter(warehouse__uid=warehouse_id).order_by('free')[page * CELLSPERPAGE - 1:(page + 1) * CELLSPERPAGE]
            elif order==2:
                cells = storage_cell_info.objects.filter(warehouse__uid=warehouse_id).order_by('-free')[page * CELLSPERPAGE - 1:(page + 1) * CELLSPERPAGE]
            else:
                raise Exception('unknown order')
        else:
            raise Exception('unauthorized operation')
    storage_cells = []
    for cell in cells:
        storage_cell = {
            'id':cell.uid,
            'warehouse_id':cell.warehouse.uid,
            'capacity':cell.capacity,
            'occupy':cell.occupy
        }
        storage_cells.append(storage_cell)
    response = {
        'status':'success',
        'storage_cells':storage_cells
    }
    return response

@verify_decorator()
def getWarehouseInfo(user:user_account_info = None, **kwargs):
    if user.role_warehouse == RoleChoices.ADMIN:
        warehouses = [{'id':warehouse.id,'name':warehouse.name} for warehouse in warehouse_info.objects.all()]
    else:
        warehouses = [{'id':warehouse.id,'name':warehouse.name} for warehouse in user.warehouses]
    response = {
        'status':'success',
        'warehouses':warehouses
    }
    return response

@verify_decorator()
def getNumberOfStorageCells(user:user_account_info = None, **kwargs):
    warehouse_id = kwargs['warehouse_id']
    if warehouse_id == 'all':
        if user.role_warehouse == RoleChoices.ADMIN:
            number = storage_cell_info.objects.all().count()
        else:
            raise Exception('unauthorized operation')
    else:
        if user.role_warehouse == RoleChoices.ADMIN or warehouse_info.objects.get(uid=warehouse_id).users.filter(uid=user.uid).exists():
            number = storage_cell_info.objects.filter(warehouse__uid=warehouse_id).count()
        else:
            raise Exception('unauthorized operation')
    response = {
        'status': 'success',
        'number': number
    }
    return response

@verify_decorator()
def getStorageCellDetail(user:user_account_info = None, **kwargs):
    cell_id = kwargs['id']
    if not user.role_warehouse == RoleChoices.ADMIN and not user.warehouses.filter(uid=storage_cell_info.objects.get(uid=cell_id).warehouse.uid):
        raise Exception('unauthorized operation')
    cell = storage_cell_info.objects.get(uid=cell_id)
    products = []
    for p in cell.products_related:
        product = {
            'id':p.product.id,
            'name':p.product.name,
            'quantity':p.number,
            'start_time':p.time
        }
        products.append(product)
    detail = {
        'id':cell_id,
        'warehouse_id':cell.warehouse.uid,
        'capacity':cell.capacity,
        'occupy':cell.occupy,
        'products':products
    }
    response = {
        'status':'success',
        'detail':detail
    }
    return response

# ////////////////////////////////////////////////////////////
# 入库单
# ////////////////////////////////////////////////////////////



# ////////////////////////////////////////////////////////////
# 零件相关
# ////////////////////////////////////////////////////////////

def _getProduct(productInfo: product_info, user=None):
    parameters = []
    for parameterInfo in productInfo.parameters.order_by('parameter_id'):
        parameter = {
            'id': parameterInfo.uid,
            'name': parameterInfo.name,
            'value_type': parameterInfo.get_value_type_display(),
            'scale': parameterInfo.scale,
            'unit': parameterInfo.unit,
            'description': parameterInfo.description,
            'graph_type': parameterInfo.control_plan.get_type_display(),
            'usl': parameterInfo.control_plan.usl,
            'lsl': parameterInfo.control_plan.lsl,
            'control_plan_id': parameterInfo.control_plan.uid
        }
        parameters.append(parameter)

    workshops = []

    measurePlanInfos = productInfo.measure_plans.filter(
        workshop__worker=user) if user else productInfo.measure_plans.all()
    for measurePlanInfo in measurePlanInfos:
        measurePlan = {'measure_plan_id': measurePlanInfo.uid, 'workshop_name': measurePlanInfo.workshop.name}
        workshops.append(measurePlan)

    product = {
        'id': productInfo.uid,
        'name': productInfo.name,
        'type': productInfo.type,
        'description': productInfo.description,
        'parameters': parameters,
        'workshop': workshops
    }

    return product


@verify_decorator()
def getProducts(user: user_account_info = None, **kwargs):
    products = []

    if user.role == RoleChoices.ADMIN:
        productInfos = product_info.objects.all()
    else:
        productInfos = product_info.objects.filter(measure_plans__workshop__worker=user)  # todo: check if right

    for productInfo in productInfos:
        product = _getProduct(productInfo, None if user.role == RoleChoices.ADMIN else user)
        products.append(product)

    response = {
        'status': 'success',
        'products': products
    }
    return response


@verify_decorator()
def alterProducts(user: user_account_info = None, product=None, modify=None, **kwargs):
    if user.role != RoleChoices.ADMIN:
        raise Exception('unauthorized operation')

    productId = None
    productInfo = None
    if modify:  # 修改零件
        try:
            productId = product.pop('id')
            productInfo = alterProduct(productId, **product)
            parameters = product.pop('parameters')
            for parameter in parameters:
                # todo: value_type in frontend is inconsistent with backened
                parameter['value_type'] = {'variable_data': 0, 'attribute_data': 1}[parameter['value_type']]
                parameter['graph_type'] = GraphTypeChoices.labels.index(parameter['graph_type'])
                alterParameter(parameter.pop('id'), **parameter)

        except Exception as e:
            if not productInfo:
                productInfo = product_info.objects.get(uid=productId)
            response = {
                'status': 'fail',
                'error_message': str(e),
                'product': _getProduct(productInfo)
            }
            return response

    else:
        try:
            productInfo = addProduct(defaultMeasurePlan=False, **product)
            productId = productInfo.uid
            parameters = product.pop('parameters')
            for parameter in parameters:
                # todo: value_type in frontend is inconsistent with backened
                parameter['value_type'] = {'variable_data': 0, 'attribute_data': 1}[parameter['value_type']]
                parameter['graph_type'] = GraphTypeChoices.labels.index(parameter['graph_type'])
                addParameter(product_id=productId,
                             parameter_id=None,
                             **parameter)
        except Exception as e:
            if productInfo:
                productInfo.delete()
            raise e

    response = {
        'status': 'success',
        'product': _getProduct(productInfo)
    }
    return response

# GET METHOD
@verify_decorator()
def deleteProduct(user: user_account_info = None, id=None, **kwargs):
    if user.role != RoleChoices.ADMIN:
        raise Exception('unauthorized operation')

    delProduct(id[0])  # args from GET is always a list
    return {'status': 'success'}


# ////////////////////////////////////////////////////////////
# 车间(测量计划)相关
# ////////////////////////////////////////////////////////////

def _getMeasureplan(measureplanInfo: measure_plan_info):
    cell = measureplanInfo.relationship_info.storage_cell
    product = measureplanInfo.relationship_info.product
    return {
        'id': measureplanInfo.uid,
        'storageCellId': cell.uid,
        'batchSize':measureplanInfo.sample_size,
        'batch':measureplanInfo.batch_count,
        'warehouse':{
            'id':cell.warehouse.uid,
            'name':cell.warehouse.name
        },
        'product':{
            'id':product.uid,
            'name':product.name
        },
        'parameters':[
            {'id':par.parameter_id,'name':par.name} for par in product.parameters.all()
        ],
        'description': measureplanInfo.description
    }


@verify_decorator()
def getMeasurePlans(user: user_account_info, **kwargs):
    measureplans = []
    if user.role == RoleChoices.ADMIN:
        measurePlans = measure_plan_info.objects.all()
    else:
        measurePlans = measure_plan_info.objects.filter(relationship_info__storage_cell__warehouse__in=user.warehouses.all())

    for measureplan in measurePlans:
        measureplans.append(_getMeasureplan(measureplan))
    response = {
        'status': 'success',
        'workshops': measureplans
    }
    return response


@verify_decorator()
def submitMeasurePlan(user: user_account_info = None, **kwargs):
    storageCellId = kwargs['storageCellId']
    cell = storage_cell_info.objects.get(uid=storageCellId)
    if not user.role_warehouse == RoleChoices.ADMIN and not warehouse_info.objects.get(uid=cell.warehouse.uid).users.filter(
            uid=user.uid).exists():
        raise Exception('unauthorized operation')

    batchSize = kwargs['batchSize']
    batch = kwargs['batch']
    productId = kwargs['productId']
    description = kwargs['description']

    _addMeasurePlan(productId,cell.uid,batchSize,batch,description)

    return {'status':'success'}

    # if modify:
    #     try:
    #         workshopId = workshop.pop('id')
    #         workshopInfo = alterWorkshop(workshopId, **workshop)
    #     except Exception as e:
    #         if not workshopInfo:
    #             workshopInfo = workshop_info.objects.get(measure_plan__uid=workshopId)
    #         response = {
    #             'status': 'fail',
    #             'error_message': str(e),
    #             'workshop': _getWorkshop(workshopInfo)
    #         }
    #         return response
    #
    # else:
    #     workshopInfo = addWorkshop(**workshop)
    #
    # response = {
    #     'status': 'success',
    #     'workshop': _getWorkshop(workshopInfo)
    # }
    #
    # return response

# GET METHOD
@verify_decorator()
def deleteMeasurePlan(user: user_account_info = None, id=None, **kwargs):
    measure_plan = measure_plan_info.objects.get(uid=id) # todo: may cause secure problems
    if user.role != RoleChoices.ADMIN or not warehouse_info.objects.get(uid=measure_plan.relationship_info.storage_cell.warehouse.uid).users.filter(
            uid=user.uid).exists():
        raise Exception('unauthorized operation')

    deleteMeasurePlan(id[0]) # args from GET is always a list
    return {'status': 'success'}

# ////////////////////////////////////////////////////////////
# 控制图异常报告相关
# ////////////////////////////////////////////////////////////

@verify_decorator()
def getControlGraph(user: user_account_info = None, **kwargs):
    if user.role != RoleChoices.ADMIN and measure_plan_info.objects.get(
            uid=kwargs['measure_plan_id']).workshop.worker != user:
        raise Exception('unauthorized operation')

    start_time = kwargs.pop('start_time')
    end_time = kwargs.pop('end_time')
    if start_time != None and end_time != None:
        graph = getGraphByTime(kwargs.pop('measure_plan_id'),
                               kwargs.pop('control_plan_id'),
                               start_time,
                               end_time)
    elif start_time != None:
        graph = getGraphByTime(kwargs.pop('measure_plan_id'),
                               kwargs.pop('control_plan_id'),
                               start_time)
    else:
        graph = getGraph(kwargs.pop('measure_plan_id'),
                         kwargs.pop('control_plan_id'))

    if kwargs.pop('analyze'):
        # return render(kwargs['request'], TEMPLATENAME, graph.generateReportDict())
        return {
            'status': 'success',
            'content': loader.render_to_string(TEMPLATENAME, graph.generateReportDict())
        }

    response = {'status': 'success'}
    # todo: bugs here
    if 'tmp_point_id' in kwargs and graph.point_ids[-1] == kwargs.pop('tmp_point_id') and False:
        response['updated'] = False
    else:
        response['updated'] = True
        response['options'] = graph.generateEchartsDict()
    response['tmp_point_id'] = graph.point_ids[-1]

    return response


@verify_decorator()
def getAllExceptionReports(user: user_account_info = None, **kwargs):
    abnormalities = []
    if user.role == RoleChoices.ADMIN:
        # abnormalityInfos = abnormality_info.objects.order_by('-uid')
        abnormalityInfos = abnormality_info.objects.order_by('if_read', '-uid')
    else:
        # abnormalityInfos = abnormality_info.objects.filter(measure_plan__workshop__worker=user).order_by('-uid')
        abnormalityInfos = abnormality_info.objects.filter(measure_plan__workshop__worker=user).order_by('if_read', '-uid')

    for abnormalityInfo in abnormalityInfos:
        abnormalities.append(
            {
                'id': abnormalityInfo.uid,
                'product': abnormalityInfo.measure_plan.product.name,
                'parameter': abnormalityInfo.control_plan.parameter.name,
                'measure_plan': abnormalityInfo.measure_plan.uid,
                'measure_form_id': abnormalityInfo.abnormality_id.measure_form_id,
                'time': abnormalityInfo.abnormality_id.end_time,
                'information': abnormalityInfo.information,
                'reason': abnormalityInfo.reason,
                'read': abnormalityInfo.if_read
            }
        )
    response = {
        'status': 'success',
        'reports': abnormalities
    }
    return response


# GET METHOD
@verify_decorator()
def getDetailReport(user: user_account_info = None, id=None, **kwargs):
    abnormalityInfo = abnormality_info.objects.get(uid=id[0])  # args from GET is always a list

    if user.role != RoleChoices.ADMIN and abnormalityInfo.measure_plan.workshop.worker != user.uid:
        raise Exception('unauthorized operation')

    history_points = control_point_info.objects.filter(control_plan_id=abnormalityInfo.control_plan_id,
                                                       measure_form__measure_plan_id=abnormalityInfo.measure_plan_id,
                                                       uid__gte=abnormalityInfo.start_id,
                                                       uid__lte=abnormalityInfo.end_id).order_by('-uid')
    graph = getGraph(abnormalityInfo.measure_plan_id, abnormalityInfo.control_plan_id, history_points)
    abnormalityInfo.if_read = True
    abnormalityInfo.save()
    # return render(kwargs['request'], TEMPLATENAME, graph.generateReportDict())
    return {
        'status': 'success',
        'content': loader.render_to_string(TEMPLATENAME, graph.generateReportDict())
    }
