from django.template import loader
from workshop.util.utils import TEMPLATENAME
from workshop.util.graphCheck import getGraph, getGraphByTime
from workshop.util.sheduleMake import addProduct, addParameter, alterProduct, alterParameter, delProduct, alterWorkshop, addWorkshop, delWorkshop
from workshop.models import *
from user.util.interface import verify_decorator


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

def _getWorkshop(workshopInfo: workshop_info):
    return {
        'id': workshopInfo.measure_plan.uid,
        'name': workshopInfo.name,
        'productId': workshopInfo.measure_plan.product.uid,
        'batchSize': workshopInfo.measure_plan.sample_size,
        'windowSize': workshopInfo.measure_plan.batch_count,
        'description': workshopInfo.description,
    }


@verify_decorator()
def getAllWorkshopInfo(user: user_account_info, **kwargs):
    workshops = []
    if user.role == RoleChoices.ADMIN:
        workshopInfos = workshop_info.objects.all()
    else:
        workshopInfos = workshop_info.objects.filter(worker=user)

    for workshopInfo in workshopInfos:
        workshopInfo: workshop_info
        workshops.append(_getWorkshop(workshopInfo))
    response = {
        'status': 'success',
        'workshops': workshops
    }
    return response


@verify_decorator()
def alterWorkshops(user: user_account_info = None, workshop=None, modify=None, **kwargs):
    if user.role != RoleChoices.ADMIN:
        raise Exception('unauthorized operation')

    workshopId = None
    workshopInfo = None

    if modify:
        try:
            workshopId = workshop.pop('id')
            workshopInfo = alterWorkshop(workshopId, **workshop)
        except Exception as e:
            if not workshopInfo:
                workshopInfo = workshop_info.objects.get(measure_plan__uid=workshopId)
            response = {
                'status': 'fail',
                'error_message': str(e),
                'workshop': _getWorkshop(workshopInfo)
            }
            return response

    else:
        workshopInfo = addWorkshop(**workshop)

    response = {
        'status': 'success',
        'workshop': _getWorkshop(workshopInfo)
    }

    return response



# GET METHOD
@verify_decorator()
def deleteWorkshop(user: user_account_info = None, id=None, **kwargs):
    if user.role != RoleChoices.ADMIN:
        raise Exception('unauthorized operation')

    delWorkshop(id[0]) # args from GET is always a list
    return {'status': 'success'}

# ////////////////////////////////////////////////////////////
# 控制图异常报告相关
# ////////////////////////////////////////////////////////////

@verify_decorator()
def getControlGraph(user: user_account_info = None, **kwargs):
    # todo: check if right
    if user.role != RoleChoices.ADMIN and not user.workshops.filter(measure_plan__uid=kwargs['measure_plan_id']):
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

    # todo: check if right
    if user.role != RoleChoices.ADMIN and user.workshops.filter(measure_plan__uid=abnormalityInfo.measure_plan_id):
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

# ////////////////////////////////////////////////////////////
# 权限管理相关
# ////////////////////////////////////////////////////////////

@verify_decorator()
def getRelationshipForm(user:user_account_info, userid=None, **kwargs):
    if user.role != RoleChoices.ADMIN:
        raise Exception('unauthorized operation')
    targetUser = user_account_info.objects.get(uid=userid)
    return {
        'status':'success',
        'relationshipform':[
            {
                'workshopid':workshop.measure_plan.uid,
                'name':workshop.name
            } for workshop in targetUser.workshops.all()
        ]
    }

@verify_decorator()
def getUserId(user:user_account_info, **kwargs):
    if user.role != RoleChoices.ADMIN:
        raise Exception('unauthorized operation')
    return {
        'status':'success',
        'userid':[
            {
                'id':user.uid,
                'name':user.name,
                'checkrole':user.get_role_display()
            } for user in user_account_info.objects.all()
        ]
    }

@verify_decorator()
def getAllWorkshopsId(user:user_account_info, **kwargs):
    if user.role != RoleChoices.ADMIN:
        raise Exception('unauthorized operation')
    return {
        'status':'success',
        'workshopid':[
            {
                'id':workshop.measure_plan.uid,
                'name':workshop.name
            } for workshop in workshop_info.objects.all()
        ]
    }

@verify_decorator()
def submitRelationship(user:user_account_info, **kwargs):
    if user.role != RoleChoices.ADMIN:
        raise Exception('unauthorized operation')
    myform = kwargs['myform']
    targetUser = user_account_info.objects.get(uid=myform['userid'])
    for relation in myform['relations']:
        if relation['checked']:
            user.workshops.add(relation['workshopId'])
        else:
            user.workshops.remove(relation['workshopId'])
    return {'status':'success'}