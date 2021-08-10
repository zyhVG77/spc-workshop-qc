from datetime import datetime
from warehouse.util.dataUpload import *
import random
import time

from workshop.util.utils import WIDTH

SIGMASCALE = 1
INTERVAL = 2

class measurePlanUpdator():
    def __init__(self,measurePlanInfo:measure_plan_info):
        self._tmpformId = int(measure_form_info.objects.get(uid=measurePlanInfo.current_uid).measure_form_id) if measurePlanInfo.current_uid else 0
        self.measurePlanId = measurePlanInfo.uid
        self.sampleSize = measurePlanInfo.sample_size
        self.operatorId = str(random.randint(0,99999999999)).rjust(WIDTH,'0')
        self.startTime = datetime.now()
        self.parameters = []
        for par in measurePlanInfo.product.parameters.all():
            para = {
                'scale': int(par.scale),
                'cl': (par.control_plan.usl+par.control_plan.lsl)/2,
                'sigma': SIGMASCALE*(par.control_plan.usl-par.control_plan.lsl)/6
            }
            self.parameters.append(para)

    @property
    def tmpformId(self):
        self._tmpformId += 1
        return str(self._tmpformId).rjust(WIDTH, '0')

    def generateForm(self):
        measure_form = []
        for i in range(self.sampleSize):
            sample = []
            for par in self.parameters:
                sample.append(round(random.normalvariate(par['cl'],par['sigma']),par['scale']))
            measure_form.append(sample)
        form = {
            'measure_form_id': self.tmpformId,
            'measure_plan':self.measurePlanId,
            'sample_size': self.sampleSize,
            'operator_id': self.operatorId,
            'start_time': self.startTime,
            'end_time': datetime.now(),
            'measure_form': measure_form
        }
        return form

def AutoUpload():
    measurePlans = [measurePlanUpdator(i) for i in measure_plan_info.objects.all()]
    while True:
        for m in measurePlans:
            uploadData(m.generateForm())
        time.sleep(INTERVAL)