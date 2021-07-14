from warehouse.models import control_point_info, parameter_data_info, measure_plan_info, measure_form_info
from warehouse.util.graphCheck import graphType
from warehouse.util.utils import control_point_uid, parameter_data_uid, measure_form_uid, DEBUG
import numpy as np


def _generatePoint(control_plan_id, measure_form_id, form, par, model, last_measure_form=None):
    sample_size = len(form)
    control_point = control_point_info(next(control_point_uid), control_plan_id, measure_form_id, sample_size)
    colNum = par.parameter_id
    sample = np.array([i[colNum] for i in form])

    for idx, n in enumerate(sample):
        parameter_data_info(next(parameter_data_uid), idx, measure_form_id, par.uid, n).save()

    if model in (0, 1, 2):
        control_point.x = np.mean(sample)
        control_point.s = np.std(sample)
        if last_measure_form:
            last_data = last_measure_form.parameter_datas.get(id=par.uid)
            last_data = last_data.value
            control_point.r = abs(last_data - sample[0])
        else:
            control_point.r = np.ptp(sample)
    else:
        control_point.p = sum(sample == 1)
        control_point.np = control_point.p / sample_size
        control_point.c = np.mean(sample)
        control_point.u = np.mean(sample)

    control_point.save()
    return control_point


def uploadData(form):
    measure_form = None

    try:
        measure_form_id = form['measure_form_id']
        measure_plan_id = form['measure_plan']
        sample_size = form['sample_size']
        operator_id = form['operator_id']
        start_time = form['start_time']
        end_time = form['end_time']
        form = form['measure_form']

        if DEBUG:
            print('\nUpload data')
            print('---------------------------------------')
            print('measure_form_id: ', measure_form_id)
            print('measure_plan_id: ', measure_plan_id)
            print('sample_size: ', sample_size)

        measure_plan = measure_plan_info.objects.get(uid=measure_plan_id)

        if measure_plan.sample_size is not None and sample_size != measure_plan.sample_size:
            raise Exception('sample size unqualified')

        pars = measure_plan.product.parameters.order_by('parameter_id')
        measure_form = measure_form_info(next(measure_form_uid), measure_form_id,
                                         measure_plan_id, sample_size, start_time, end_time, operator_id)
        measure_form.save()

        for par in pars:
            control_plan = par.control_plan
            _generatePoint(control_plan.uid, measure_form.uid, form, par, control_plan.type,
                           measure_plan.measure_forms.get(
                               uid=measure_plan.current_uid) if control_plan.type == 2 else None)
            history_points = control_point_info.objects.filter(control_plan=control_plan,
                                                               measure_form__measure_plan=measure_plan).order_by(
                '-uid')[:measure_plan.batch_count]
            graph = graphType[control_plan.get_type_display()](measure_plan, control_plan, history_points)
            graph.getData()
            graph.analyze()

            if DEBUG:
                printHead = False
                for report in graph.getAbnormality():
                    if not printHead:
                        print('Abnormality: ', par.name)
                        printHead = True
                    print(report)

        measure_plan.current_uid = measure_form.uid
        measure_plan.save()

    except Exception as e:
        if measure_form:
            measure_form.delete()
        if DEBUG:
            print('uploadData failed')
        raise e
