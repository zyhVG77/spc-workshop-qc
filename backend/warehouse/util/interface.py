from django.db.models import F
from django.template import loader

from warehouse.util.charts import generateMainBoardHeatMap, generateMainBoardSunburstMap
from warehouse.util.utils import TEMPLATENAME, CELLSPERPAGE, entry_uid, storage_cell_product_relationship_uid, \
    warehouse_uid, storage_cell_uid
from warehouse.util.graphCheck import getGraph, getGraphByTime
from warehouse.util.sheduleMake import addProduct, addParameter, alterProduct, alterParameter, delProduct, \
    _addMeasurePlan  # , alterWorkshop, addWorkshop, delWorkshop
from warehouse.models import *
from user.util.interface import verify_decorator
from datetime import datetime, date, timedelta


# warehouse = warehouse_info(next(warehouse_uid),'仓库一',capacity=6000,occupy=0)
# warehouse.save()
# for i in range(300):
#     cell = storage_cell_info(next(storage_cell_uid),warehouse.uid,20,0)
#     cell.save()
# warehouse = warehouse_info(next(warehouse_uid),'仓库二',capacity=6000,occupy=0)
# warehouse.save()
# for i in range(300):
#     cell = storage_cell_info(next(storage_cell_uid),warehouse.uid,20,0)
#     cell.save()

# ////////////////////////////////////////////////////////////
# 仓位图
# ////////////////////////////////////////////////////////////

# GET METHOD
@verify_decorator()
def getStorageCells(user:user_account_info = None, **kwargs):
    warehouse_id = kwargs['warehouse_id'][0]
    order = kwargs['order'][0]
    page = kwargs['page'][0]
    if warehouse_id == 'all':
        if user.role_warehouse == RoleChoices.ADMIN:
            if order=='0':
                cells = storage_cell_info.objects.order_by('warehouse__uid','uid')
            elif order=='1':
                cells = storage_cell_info.objects.order_by('warehouse__uid',(F('occupy')/F('capacity')).asc())
            elif order=='2':
                cells = storage_cell_info.objects.order_by('warehouse__uid', (F('occupy')/F('capacity')).desc())
            else:
                raise Exception('unknown order')
            if page != 'all':
                page = int(page)
                cells = cells[page * CELLSPERPAGE:(page + 1) * CELLSPERPAGE]
        else:
            raise Exception('unauthorized operation')
    else:
        if user.role_warehouse == RoleChoices.ADMIN or warehouse_info.objects.get(uid=warehouse_id).users.filter(uid=user.uid).exists():
            if order=='0':
                cells = storage_cell_info.objects.filter(warehouse__uid=warehouse_id).order_by('uid')
            elif order=='1':
                cells = storage_cell_info.objects.filter(warehouse__uid=warehouse_id).order_by((F('occupy')/F('capacity')).asc())
            elif order=='2':
                cells = storage_cell_info.objects.filter(warehouse__uid=warehouse_id).order_by((F('occupy')/F('capacity')).desc())
            else:
                raise Exception('unknown order')
            if page != 'all':
                page = int(page)
                cells = cells[page * CELLSPERPAGE:(page + 1) * CELLSPERPAGE]
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

# GET METHOD
@verify_decorator()
def getWarehouseInfo(user:user_account_info = None, **kwargs):
    if user.role_warehouse == RoleChoices.ADMIN:
        warehouses = [{'id':warehouse.uid,'name':warehouse.name,'capacity':warehouse.capacity,'occupy':warehouse.occupy} for warehouse in warehouse_info.objects.all()]
    else:
        warehouses = [{'id':warehouse.uid,'name':warehouse.name,'capacity':warehouse.capacity,'occupy':warehouse.occupy} for warehouse in user.warehouses.all()]
    response = {
        'status':'success',
        'warehouses':warehouses
    }
    return response

# GET METHOD
@verify_decorator()
def getNumberOfStorageCells(user:user_account_info = None, **kwargs):
    warehouse_id = kwargs['warehouse_id'][0]
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

# GET METHOD
@verify_decorator()
def getStorageCellDetail(user:user_account_info = None, **kwargs):
    cell_id = kwargs['id'][0]
    if not user.role_warehouse == RoleChoices.ADMIN and not user.warehouses.filter(uid=storage_cell_info.objects.get(uid=cell_id).warehouse.uid):
        raise Exception('unauthorized operation')
    cell = storage_cell_info.objects.get(uid=cell_id)
    products = []
    for p in cell.products_related.all():
        product = {
            'id':p.product.uid,
            'name':p.product.name,
            'quantity':p.occupy,
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
# 出入库
# ////////////////////////////////////////////////////////////

def _storeIntoCell(parameter,cell:storage_cell_info):
    capacity = cell.free
    if capacity <= 0:
        return parameter,None
    try:
        relationship = cell.products_related.get(product__uid=parameter['index'])
    except:
        relationship = storage_cell_product_relationship(next(storage_cell_product_relationship_uid), cell.uid, parameter['index'], 0,
                                         datetime.now())
    warehouse = cell.warehouse
    try:
        board = main_board.objects.get(date=datetime.today(),warehouse=warehouse)
    except:
        board = main_board(date=datetime.today(), warehouse_id=warehouse.uid)
        try:
            board.occupation = main_board.objects.filter(warehouse=warehouse).order_by('-date')[0].occupation
        except: # todo: check if it works
            board.occupation = 0
        board.save()
    if parameter['quantity']>capacity:
        shift = cell.free
        parameter['quantity'] -= shift
        relationship.occupy += shift
        relationship.time = datetime.now()
        relationship.save()
        cell.occupy += shift
        cell.save()
        warehouse.occupy += shift
        warehouse.save()
        board.occupation += shift
        board.save()
        return parameter,None
    else:
        shift = parameter['quantity']
        relationship.occupy += shift
        relationship.time = datetime.now()
        relationship.save()
        cell.occupy += shift
        cell.save()
        warehouse.occupy += shift
        warehouse.save()
        board.occupation += shift
        board.save()
        return None,cell

@verify_decorator()
def submitPutInForm(user:user_account_info=None,**kwargs):
    parameters = kwargs.pop('parameters')
    total = sum([int(par['quantity']) for par in parameters])
    if kwargs.pop('autodistribute'):
        if user.role == RoleChoices.ADMIN:
            capacity = warehouse_info.objects.aggregate(capacity=models.Sum(F('capacity')-F('occupy')))['capacity']
            cells = storage_cell_info.objects.all()
        else:
            capacity = user.warehouses.aggregate(capacity=models.Sum(F('capacity')-F('occupy')))['capacity']
            cells = storage_cell_info.objects.filter(warehouse__users=user)
        if capacity < total:
            raise Exception("not enough space")
    else:
        cells = []
        capacity = 0
        for id in kwargs.pop('storeid'):
            cell = storage_cell_info.objects.get(uid=id)
            if not user in cell.warehouse.users: # todo: check if it can work
                raise Exception("unauthorized operation")
            cells.append(cell)
            capacity += cell.free
        if capacity < total:
            raise Exception("not enough space")
    entry = entry_info(next(entry_uid),datetime.now(),user.uid)
    entry.save()
    for parameter in parameters:
        parameter['quantity'] = int(parameter['quantity'])
        entry_product_relationship(product_id = parameter['index'],entry_id = entry.uid,number = parameter['quantity']).save()
    it = iter(cells)
    cell = next(it)
    # todo: check if right
    for parameter in parameters:
        while(parameter):
            parameter,cell = _storeIntoCell(parameter,cell)
            if(cell):
                cell = next(it)
    return {'status':'success'}

def _getFromCell(parameter,cell:storage_cell_info):
    try:
        relationship = cell.products_related.get(product__uid=parameter['index'])
    except:
        return parameter,None
    warehouse = cell.warehouse
    try:
        board = main_board.objects.get(date=datetime.today(),warehouse=warehouse)
    except:
        board = main_board(date=datetime.today(), warehouse_id=warehouse.uid)
        board.occupation = main_board.objects.filter(warehouse=warehouse).order_by('-date')[0].occupation
        board.save()
    if parameter['quantity']>relationship.occupy:
        shift = relationship.occupy
        parameter['quantity'] -= shift
        relationship.delete()
        cell.occupy -= shift
        cell.save()
        warehouse.occupy -= shift
        warehouse.save()
        board.occupation -= shift
        board.save()
        return parameter,None
    else:
        shift = parameter['quantity']
        relationship.occupy -= shift
        relationship.time = datetime.now()
        relationship.save()
        cell.occupy -= shift
        cell.save()
        warehouse.occupy -= shift
        warehouse.save()
        board.occupation -= shift
        board.save()
        return None,cell


@verify_decorator()
def submitTakeoutForm(user:user_account_info=None, **kwargs):
    parameters = kwargs.pop('parameters')
    total = sum([int(par['quantity']) for par in parameters])
    if kwargs.pop('autodistribute'):
        if user.role == RoleChoices.ADMIN:
            # capacity = warehouse_info.objects.aggregate(capcity=models.Sum('free'))['capacity']
            cells = storage_cell_info.objects.all()
        else:
            # capacity = user.warehouses.aggregate(capacity=models.Sum('free'))['capacity']
            cells = storage_cell_info.objects.filter(warehouse__users=user)
        # if capacity < total:
        #     raise Exception("not enough space")
    else:
        cells = []
        # capacity = 0
        for id in kwargs.pop('storeid'):
            cell = storage_cell_info.objects.get(uid=id)
            if not user in cell.warehouse.users: # todo: check if it can work
                raise Exception("unauthorized operation")
            cells.append(cell)
            # capacity += cell.free
        # if capacity < total:
        #     raise Exception("not enough space")
    shipment = shipment_info(next(entry_uid),datetime.now(),user.uid)
    shipment.save()
    for parameter in parameters:
        parameter['quantity'] = int(parameter['quantity'])
        shipment_product_relationship(product_id = parameter['index'],entry_id = shipment.uid,number = parameter['quantity']).save()
    it = iter(cells)
    cell = next(it)
    # todo: check if right
    for parameter in parameters:
        while(parameter):
            parameter,cell = _getFromCell(parameter,cell)
            if(cell):
                try:
                    cell = next(it)
                except:
                    raise Exception('not enough inventory')
    return {'status':'success'}

# ////////////////////////////////////////////////////////////
# 看板
# ////////////////////////////////////////////////////////////

# GET METHOD
@verify_decorator()
def getWarehouseBasicInfo(user:user_account_info=None,**kwargs):
    import random
    return {
        'status': 'success',
        'basicInfo': {
            'storeBatches': 10,
            'storeAmount': 10,
            'storeMoney': 10,
            'deliverBatches': 10,
            'deliverAmount': 10,
            'deliverMoney': 10,
        },
        'storeDeliverGraphOpiton': generateMainBoardHeatMap([[(date(2020, 1, 1) + timedelta(d)).strftime("%Y-%m-%d"), random.randint(1, 100)] for d in range(365)]),
        'occupationStateGraphOption': generateMainBoardSunburstMap(
            [
                {
                    'name': warehouse.name,
                    'value': warehouse.capacity,
                    'children': [
                        {'name': '空闲', 'value': warehouse.capacity - warehouse.occupy},
                        {'name': '占用' if warehouse.occupy != 0 else "", 'value': warehouse.occupy}
                    ]
                } for warehouse in warehouse_info.objects.all()
            ] + [
                {
                    'name':'仓库三（test）',
                    'value':9000,
                    'children':[
                        {'name':'空闲','value':6000},
                        {'name':'占用','value':3000}
                    ]
                }
            ]
        )
    }

# GET METHOD
@verify_decorator()
def getWarehouseAffairs(user:user_account_info=None,**kwargs):
    return {
        'status':'success',
        'affairs':[
            {
                'time':datetime.now(),
                'type':'store',
                'detail':'dasfsdaf',
                'operator':'dafasregtsoruiejgw'
            },
            {
                'time': datetime.now(),
                'type': 'deliver',
                'detail': 'dasfsdaf',
                'operator': 'dafasregtsoruiejgw'
            }
        ]
    }

# ////////////////////////////////////////////////////////////
# 零件相关
# ////////////////////////////////////////////////////////////

def _getProduct(productInfo: product_info = None, user=None):
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

    # workshops = []
    # # fixme: bugs here
    # measurePlanInfos = productInfo.measure_plans.filter(
    #     workshop__worker=user) if user else productInfo.measure_plans.all()
    # for measurePlanInfo in measurePlanInfos:
    #     measurePlan = {'measure_plan_id': measurePlanInfo.uid, 'workshop_name': measurePlanInfo.workshop.name}
    #     workshops.append(measurePlan)

    product = {
        'id': productInfo.uid,
        'name': productInfo.name,
        'type': productInfo.type,
        'description': productInfo.description,
        'parameters': parameters,
        # 'workshop': workshops
    }

    return product


@verify_decorator()
def getProducts(user: user_account_info = None, **kwargs):
    products = []

    productInfos = product_info.objects.all()
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
            'name':product.name,
            'parameters': [
                {
                    'id': par.parameter_id,
                    'name': par.name,
                    'unit': par.unit,
                    'scale': par.scale,
                    'graph_type': par.control_plan.get_type_display(),
                    'usl': par.control_plan.usl,
                    'lsl': par.control_plan.lsl
                } for par in product.parameters.all()
            ],
        },
        'description': measureplanInfo.description
    }


@verify_decorator()
def getMeasurePlans(user: user_account_info = None, **kwargs):
    measureplans = []
    if user.role == RoleChoices.ADMIN:
        measurePlans = measure_plan_info.objects.all()
    else:
        measurePlans = measure_plan_info.objects.filter(relationship_info__storage_cell__warehouse__in=user.warehouses.all())

    for measureplan in measurePlans:
        measureplans.append(_getMeasureplan(measureplan))
    response = {
        'status': 'success',
        'measurePlans': measureplans
    }
    return response


@verify_decorator()
def submitMeasurePlan(user: user_account_info = None, measurePlan=None, **kwargs):
    storageCellId = measurePlan['storageCellId']
    cell = storage_cell_info.objects.get(uid=storageCellId)
    if not user.role_warehouse == RoleChoices.ADMIN and not warehouse_info.objects.get(uid=cell.warehouse.uid).users.filter(
            uid=user.uid).exists():
        raise Exception('unauthorized operation')

    batchSize = measurePlan['batchSize']
    batch = measurePlan['batch']
    productId = measurePlan['productId']
    description = measurePlan['description']

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
