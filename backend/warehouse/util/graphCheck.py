from warehouse.models import control_plan_info, measure_plan_info, abnormality_info
from warehouse.util.utils import SPC_parameters, abnormality_uid, SCALE
from warehouse.util.charts import generateXbarRIMREchartsDict, generateXbarsEchartsDict, generatePNpCUEchartsDict, generateReportDict
import math


def idStrip(pointId):
    if isinstance(pointId, str):
        return '0' + pointId.lstrip('0')
    else:
        prefix = len(pointId[-1]) - len(pointId[-1].lstrip('0'))
        return [id[prefix - 1:] for id in pointId]


class SPCAnalyzer():
    def __init__(self, windowSize, limitValue, test, helpText, reason):
        self.windowSize = windowSize
        self.limitValue = limitValue
        self.test = test
        self.helpText = helpText
        self.reason = reason

    def generateReport(self, startPoint, endPoint):
        if self.limitValue == 1:
            assert startPoint == endPoint
            return self.helpText % idStrip(startPoint)
        else:
            return self.helpText % tuple(idStrip([startPoint, endPoint]))

    def report(self, measure_plan_id, control_plan_id, start_point, end_point, start_id, end_id, abnormality_id):
        try:
            abnormality = abnormality_info.objects.get(measure_plan__uid=measure_plan_id,
                                                       control_plan__uid=control_plan_id,
                                                       abnormality_id__uid=abnormality_id)
            abnormality.start_id = start_id
            abnormality.end_id = end_id
            abnormality.information = self.generateReport(start_point, end_point)
        except:
            abnormality = abnormality_info(next(abnormality_uid), measure_plan_id, control_plan_id, abnormality_id,
                                           start_id, end_id, self.generateReport(start_point, end_point),self.reason, False)
        print(abnormality_id)
        print(abnormality.abnormality_id.uid)
        abnormality.save()


class pointInfo():
    def __init__(self, sigma, value, lastvalue=None):
        self.value = value
        self._sigma = sigma
        self.position = self.generateLocation()
        self.ifHigher = value >= lastvalue if lastvalue is not None else False
        self.ifLower = value <= lastvalue if lastvalue is not None else False

    def generateLocation(self):
        """
        -1 | 0 | 1 | 2 | 3 | 4 | 5 | 6
          lcl          cl         ucl
        """
        location = -1
        for i in self._sigma:
            if self.value >= i:
                location += 1
            else:
                break
        return location


SPC_analyzer = [SPCAnalyzer(1, 1, lambda x: x.position == -1 or x.position == 6, '样本%s超出控制界限','子组异常，过程可能已经失控'),
                SPCAnalyzer(8, 8, lambda x: x.position >= 3, '%s-%s连续8个样本在中心线上方','子组存在较小的偏移，过程可能失控'),
                SPCAnalyzer(8, 8, lambda x: x.position <= 2, '%s-%s连续8个样本在中心线下方','子组存在较小的偏移，过程可能失控'),
                SPCAnalyzer(7, 7, lambda x: x.ifHigher, '%s-%s这7个样本值持续上升','过程可能正处于失控趋势'),
                SPCAnalyzer(7, 7, lambda x: x.ifLower, '%s-%s这7个样本值持续下降','过程可能正处于失控趋势'),
                SPCAnalyzer(3, 2, lambda x: x.position >= 5, '%s-%s这3个样本中有2个在上方A区或A区以外','过程中存在小偏移'),
                SPCAnalyzer(3, 2, lambda x: x.position <= 0, '%s-%s这3个样本中有2个在下方A区或A区以外','过程中存在小偏移'),
                SPCAnalyzer(5, 4, lambda x: x.position >= 4, '%s-%s这5个样本中有4个在上方B区或B区以外','过程中存在小偏移'),
                SPCAnalyzer(5, 4, lambda x: x.position <= 1, '%s-%s这5个样本中有4个在下方B区或B区以外','过程中存在小偏移'),
                SPCAnalyzer(15, 15, lambda x: 2 <= x.position <= 3, '%s-%s连续15个样本在C区或C区内','数据发生分层现象，过程中可能存在系统变异源'),
                SPCAnalyzer(8, 8, lambda x: x.position <= 1 or x.position >= 4, '%s-%s连续8个样本在两侧B区或B区以外','子组有避开中心线的趋势，过程可能出现两个均值')]


class Graph():
    def __init__(self, measure_plan: measure_plan_info, control_plan: control_plan_info, points=None, reverse=True,
                 **kwargs):
        self._measure_plan = measure_plan
        self._control_plan = control_plan
        self._type = control_plan.get_type_display()
        self._size = measure_plan.sample_size
        self._scale = int(control_plan.parameter.scale)

        if points:
            self._original_points = [i for i in points]
        else:
            self._getPoints(**kwargs)
        if reverse:
            self._original_points = self._original_points[::-1]

        self.__point_ids = [i.measure_form.measure_form_id for i in self._original_points]

    @property
    def measure_plan(self):
        return self._measure_plan

    @property
    def control_plan(self):
        return self._control_plan

    @property
    def type(self):
        return self._type

    @property
    def size(self):
        return self._size

    @property
    def scale(self):
        return self._scale

    @property
    def point_ids(self):
        return idStrip(self.__point_ids)

    def _getPoints(self, **kwargs):
        if 'start_time' in kwargs:
            start_time = kwargs['start_time']
        else:
            raise Exception('start time should be specified')

        if 'end_time' in kwargs:
            end_time = kwargs['end_time']
        else:
            end_time = measure_form_info.objects.get(uid=self._measure_plan.current_uid).end_time

        points = control_point_info.objects.filter(control_plan=self._control_plan,
                                                   measure_form__measure_plan=self._measure_plan,
                                                   measure_form__end_time__gte=start_time,
                                                   measure_form__end_time__lte=end_time).order_by('-uid')

        self._original_points = points

    def _analyze(self, data, sigma, SPC_analyzer):
        report = [[] for i in self._original_points]
        points = []

        for i in range(len(data)):
            if i == 0:
                points.append(pointInfo(sigma, data[i]))
            else:
                points.append(pointInfo(sigma, data[i], data[i - 1]))

        pointArray = np.array([[1 if analyzer.test(point) else 0 for analyzer in SPC_analyzer] for point in points])

        checkArray = np.array([0 for i in range(len(SPC_analyzer))])

        indexArray = np.zeros_like(checkArray)

        for index in range(len(points)):
            minusArray = np.array([0 if indexArray[i] - SPC_analyzer[i].windowSize < 0
                                   else pointArray[indexArray[i] - SPC_analyzer[i].windowSize][i]
                                   for i in range(len(SPC_analyzer))])

            checkArray = checkArray + pointArray[index] - minusArray
            for i in range(len(SPC_analyzer) - 1, -1, -1):
                if checkArray[i] >= SPC_analyzer[i].limitValue:
                    startId = index - SPC_analyzer[i].windowSize + 1 if index - SPC_analyzer[i].windowSize + 1 >= 0 else \
                        indexArray[i]
                    endId = index if index - SPC_analyzer[i].windowSize >= 0 else indexArray[i] + SPC_analyzer[
                        i].windowSize - 1
                    startId = self.__point_ids[startId]
                    endId = self.__point_ids[endId if endId < len(self.__point_ids) else -1]
                    report[index] = [i, index, startId, endId]
                    checkArray[i] = 0
                    indexArray[i] = index

            indexArray += np.ones_like(indexArray)

        return filter(lambda x: x != [], report)

    def _generateReport(self, report):
        result = []
        for i in report:
            assert i != []
            index, _, startId, endId = i
            result.append([SPC_analyzer[index].generateReport(startId, endId),SPC_analyzer[index].reason])
        return result

    def _reportAbnormality(self, report):
        for i in report:
            analyzerIndex, pointIndex, startId, endId = i
            SPC_analyzer[analyzerIndex].report(self._measure_plan.uid,
                                               self._control_plan.uid,
                                               startId, endId,
                                               self._original_points[0].uid,
                                               self._original_points[-1].uid,
                                               self._original_points[pointIndex].measure_form.uid)

    def generateReportDict(self):
        return generateReportDict(self)

    def analyze(self):
        raise NotImplementedError

    def getAbnormality(self):
        raise NotImplementedError

    def generateEchartsDict(self):
        raise NotImplementedError


class Xbar_R(Graph):
    def __init__(self, measure_plan: measure_plan_info, control_plan: control_plan_info, points=None, **kwargs):
        super().__init__(measure_plan, control_plan, points, **kwargs)
        self._pointx = None
        self._pointr = None
        self._clx = self._uclx = self._lclx = None
        self._clr = self._uclr = self._lclr = None
        self._sigmax = None
        self._sigmar = None
        self._uslx = None
        self._lslx = None
        self._Xmin = self._Xmax = None
        self._Rmin = self._Rmax = None
        self._reportR = None
        self._reportX = None

    @property
    def pointx(self):
        return [round(i, self.scale) for i in self._pointx]

    @property
    def pointr(self):
        return [round(i, self.scale) for i in self._pointr]

    @property
    def clx(self):
        return round(self._clx, self.scale)

    @property
    def uclx(self):
        return round(self._uclx, self.scale)

    @property
    def lclx(self):
        return round(self._lclx, self.scale)

    @property
    def clr(self):
        return round(self._clr, self.scale)

    @property
    def uclr(self):
        return round(self._uclr, self.scale)

    @property
    def lclr(self):
        return round(self._lclr, self.scale)

    @property
    def uslx(self):
        return None if self._uslx is None else round(self._uslx, self.scale)

    @property
    def lslx(self):
        return None if self._lslx is None else round(self._lslx, self.scale)

    @property
    def Xmin(self):
        return round(self._Xmin, self.scale - 1)

    @property
    def Xmax(self):
        return round(self._Xmax, self.scale - 1)

    @property
    def Rmin(self):
        return round(self._Rmin, self.scale - 1)

    @property
    def Rmax(self):
        return round(self._Rmax, self.scale - 1)

    @property
    def CPK(self):
        Tu = self._uslx if self._uslx is not None else self._uclx
        Tl = self._lslx if self._lslx is not None else self._lclx

        SigmaST = self._clr / SPC_parameters['XR']['d2'][self._size]
        Cpu = (Tu - self._clx) / (3 * SigmaST)
        Cpl = (self._clx - Tl) / (3 * SigmaST)
        return round(min(Cpu, Cpl), 2)

    @property
    def PPK(self):
        Tu = self._uslx if self._uslx is not None else self._uclx
        Tl = self._lslx if self._lslx is not None else self._lclx

        SigmaLT = np.std(self._pointx)
        Ppu = (Tu - self._clx) / (3 * SigmaLT)
        Ppl = (self._clx - Tl) / (3 * SigmaLT)
        return round(min(Ppu, Ppl), 2)

    @property
    def progressIndex(self):
        if not self.reportR and not self.reportX:
            return {'name': 'Cpk', 'value': self.CPK}
        else:
            return {'name':'Ppk','value': self.PPK}

    @property
    def reportR(self):
        if not self._reportR:
            self._reportR = [i for i in self._analyze(self._pointr, self._sigmar, SPC_analyzer[:7])]
        return self._reportR

    @property
    def reportX(self):
        if not self._reportX:
            self._reportX = [i for i in self._analyze(self._pointx, self._sigmax, SPC_analyzer)]
        return self._reportX

    def getData(self):
        self._pointx = np.array([i.x for i in self._original_points])
        self._pointr = np.array([i.r for i in self._original_points])
        self._uslx = self._control_plan.usl
        self._lslx = self._control_plan.lsl

        self._clr = np.average(self._pointr)
        self._uclr = SPC_parameters['XR']['D4'][self._size] * self._clr
        self._lclr = SPC_parameters['XR']['D3'][self._size] * self._clr

        self._clx = np.average(self._pointx)
        self._uclx = self._clx + SPC_parameters['XR']['A2'][self._size] * self._clr
        self._lclx = self._clx - SPC_parameters['XR']['A2'][self._size] * self._clr

        uRange = self._uclx - self._clx
        lRange = self._clx - self._lclx
        self._sigmax = [self._lclx, self._clx - lRange * 2 / 3, self._clx - lRange / 3, self._clx,
                        self._clx + uRange / 3, self._clx + uRange * 2 / 3, self._uclx]
        self._Xmin = self._lclx - lRange * SCALE
        self._Xmax = self._uclx + uRange * SCALE

        uRange = self._uclr - self._clr
        lRange = self._clr - self._lclr
        self._sigmar = [self._lclr, self._clr - lRange * 2 / 3, self._clr - lRange / 3, self._clr,
                        self._clr + uRange / 3, self._clr + uRange * 2 / 3, self._uclr]
        self._Rmin = self._lclr - lRange * SCALE
        self._Rmax = self._uclr + uRange * SCALE

    def analyze(self):
        if self.reportR:
            self._reportAbnormality(self.reportR)
        else:
            self._reportAbnormality(self.reportX)

    def getAbnormality(self):
        if self.reportR:
            return self._generateReport(self.reportR)
        else:
            return self._generateReport(self.reportX)

    def generateEchartsDict(self):
        return generateXbarRIMREchartsDict(self)


class Xbar_s(Graph):
    def __init__(self, measure_plan: measure_plan_info, control_plan: control_plan_info, points, **kwargs):
        super().__init__(measure_plan, control_plan, points, **kwargs)
        self._pointx = None
        self._points = None
        self._clx = self._uclx = self._lclx = None
        self._cls = self._ucls = self._lcls = None
        self._sigmax = None
        self._sigmas = None
        self._uslx = None
        self._lslx = None
        self._Xmin = self._Xmax = None
        self._Smin = self._Smax = None
        self._reportS = None
        self._reportX = None

    @property
    def pointx(self):
        return [round(i, self.scale) for i in self._pointx]

    @property
    def points(self):
        return [round(i, self.scale) for i in self._points]

    @property
    def clx(self):
        return round(self._clx, self.scale)

    @property
    def uclx(self):
        return round(self._uclx, self.scale)

    @property
    def lclx(self):
        return round(self._lclx, self.scale)

    @property
    def cls(self):
        return round(self._cls, self.scale)

    @property
    def ucls(self):
        return round(self._ucls, self.scale)

    @property
    def lcls(self):
        return round(self._lcls, self.scale)

    @property
    def uslx(self):
        return None if self._uslx is None else round(self._uslx, self.scale)

    @property
    def lslx(self):
        return None if self._lslx is None else round(self._lslx, self.scale)

    @property
    def Xmin(self):
        return round(self._Xmin, self.scale - 1)

    @property
    def Xmax(self):
        return round(self._Xmax, self.scale - 1)

    @property
    def Smin(self):
        return round(self._Smin, self.scale - 1)

    @property
    def Smax(self):
        return round(self._Smax, self.scale - 1)

    @property
    def CPK(self):
        Tu = self._uslx if self._uslx is not None else self._uclx
        Tl = self._lslx if self._lslx is not None else self._lclx

        SigmaST = self._cls / SPC_parameters['XS']['c4'][self._size]
        Cpu = (Tu - self._clx) / (3 * SigmaST)
        Cpl = (self._clx - Tl) / (3 * SigmaST)
        return round(min(Cpu, Cpl), 2)

    @property
    def PPK(self):
        Tu = self._uslx if self._uslx is not None else self._uclx
        Tl = self._lslx if self._lslx is not None else self._lclx

        SigmaLT = np.std(self._pointx)
        Ppu = (Tu - self._clx) / (3 * SigmaLT)
        Ppl = (self._clx - Tl) / (3 * SigmaLT)
        return round(min(Ppu, Ppl), 2)

    @property
    def progressIndex(self):
        if not self.reportS and not self.reportX:
            return {'name': 'Cpk', 'value': self.CPK}
        else:
            return {'name': 'Ppk', 'value': self.PPK}

    @property
    def reportS(self):
        if not self._reportS:
            self._reportS = [i for i in self._analyze(self._points, self._sigmas, SPC_analyzer[:7])]
        return self._reportS

    @property
    def reportX(self):
        if not self._reportX:
            self._reportX = [i for i in self._analyze(self._pointx, self._sigmax, SPC_analyzer)]
        return self._reportX

    def getData(self):
        self._pointx = np.array([i.x for i in self._original_points])
        self._points = np.array([i.s for i in self._original_points])
        self._uslx = self._control_plan.usl
        self._lslx = self._control_plan.lsl

        self._cls = np.average(self._points)
        self._ucls = SPC_parameters['XS']['B4'][self._size] * self._cls
        self._lcls = SPC_parameters['XS']['B3'][self._size] * self._cls

        self._clx = np.average(self._pointx)
        self._uclx = self._clx + SPC_parameters['XS']['A3'][self._size] * self._cls
        self._lclx = self._clx - SPC_parameters['XS']['A3'][self._size] * self._cls

        uRange = self._uclx - self._clx
        lRange = self._clx - self._lclx
        self._sigmax = [self._lclx, self._clx - lRange * 2 / 3, self._clx - lRange / 3, self._clx,
                        self._clx + uRange / 3, self._clx + uRange * 2 / 3, self._uclx]
        self._Xmin = self._lclx - lRange * SCALE
        self._Xmax = self._uclx + uRange * SCALE

        uRange = self._ucls - self._cls
        lRange = self._cls - self._lcls
        self._sigmas = [self._lcls, self._cls - lRange * 2 / 3, self._cls - lRange / 3, self._cls,
                        self._cls + uRange / 3, self._cls + uRange * 2 / 3, self._ucls]
        self._Smin = self._lcls - lRange * SCALE
        self._Smax = self._ucls + uRange * SCALE

    def analyze(self):
        if self.reportS:
            self._reportAbnormality(self.reportS)
        else:
            self._reportAbnormality(self.reportX)

    def getAbnormality(self):
        if self.reportS:
            return self._generateReport(self.reportS)
        else:
            return self._generateReport(self.reportX)

    def generateEchartsDict(self):
        return generateXbarsEchartsDict(self)


class I_MR(Xbar_R):
    def __init__(self, measure_plan: measure_plan_info, control_plan: control_plan_info, **kwargs):
        super().__init__(measure_plan, control_plan, **kwargs)
        assert len(self._original_points)

    @property
    def progressIndex(self):
        Tu = self._uslx if self._uslx is not None else self._uclx
        Tl = self._lslx if self._lslx is not None else self._lclx

        if not self.reportR and not self.reportX:
            SigmaST = self._clr / SPC_parameters['IMR']['d2'][len(self._original_points)]
            Cpu = (Tu-self._clr)/(3*SigmaST)
            Cpl = (self._clr-Tl)/(3*SigmaST)
            return {'name':'Cpk','value':round(min(Cpu,Cpl),2)}
        else:
            SigmaLT = np.std(self._pointx)
            Ppu = (Tu-self._clr)/(3*SigmaLT)
            Ppl = (self._clr-Tu)/(3*SigmaLT)
            return {'name':'Ppk','value':round(min(Ppu,Ppl),2)}

    def getData(self):
        size = len(self._original_points)
        self._pointx = np.array([i.x for i in self._original_points])
        self._pointr = np.array([i.r for i in self._original_points])
        self._uslx = self._control_plan.usl
        self._lslx = self._control_plan.lsl

        self._clr = np.average(self._pointr)
        self._uclr = SPC_parameters['IMR']['D4'][size] * self._clr
        self._lclr = SPC_parameters['IMR']['D3'][size] * self._clr

        self._clx = np.average(self._pointx)
        self._uclx = self._clx + SPC_parameters['XR']['E2'][size] * self._clr
        self._lclx = self._clx - SPC_parameters['XR']['E2'][size] * self._clr

        uRange = self._uclx - self._clx
        lRange = self._clx - self._lclx
        self._sigmax = [self._lclx, self._clx - lRange * 2 / 3, self._clx - lRange / 3, self._clx,
                        self._clx + uRange / 3, self._clx + uRange * 2 / 3, self._uclx]
        self._Xmin = self._lclx - lRange * SCALE
        self._Xmax = self._uclx + uRange * SCALE

        uRange = self._uclr - self._clr
        lRange = self._clr - self._lclr
        self._sigmar = [self._lclr, self._clr - lRange * 2 / 3, self._clr - lRange / 3, self._clr,
                        self._clr + uRange / 3, self._clr + uRange * 2 / 3, self._uclr]
        self._Rmin = self._lclr - lRange * SCALE
        self._Rmax = self._uclr + uRange * SCALE


class pChart(Graph):
    def __init__(self, measure_plan: measure_plan_info, control_plan: control_plan_info, points, **kwargs):
        super().__init__(measure_plan, control_plan, points, **kwargs)
        self._point = None
        self._cl = self._ucl = self._lcl = None
        self._sigma = None
        self._usl = None
        self._lsl = None
        self._min = self._max = None

    @property
    def point(self):
        return [round(i, self.scale) for i in self._point]

    @property
    def cl(self):
        return round(self._cl, self.scale)

    @property
    def ucl(self):
        return round(self._ucl, self.scale)

    @property
    def lcl(self):
        return round(self._lcl, self.scale)

    @property
    def usl(self):
        return None if self._usl is None else round(self._usl, self.scale)

    @property
    def lsl(self):
        return None if self._lsl is None else round(self._lsl, self.scale)

    @property
    def min(self):
        return round(self._min, self.scale - 1)

    @property
    def max(self):
        return round(self._max, self.scale - 1)

    def getData(self):
        self._point = np.array([i.p for i in self._original_points])
        self._usl = self._control_plan.usl
        self._lsl = self._control_plan.lsl

        self._cl = np.average(self._point)
        self._ucl = self._cl + 3 * math.sqrt(self._cl * (1 - self._cl)) / math.sqrt(self._size)
        self._lcl = self._cl - 3 * math.sqrt(self._cl * (1 - self._cl)) / math.sqrt(self._size)

        uRange = self._ucl - self._cl
        lRange = self._cl - self._lcl
        self._sigma = [self._lcl, self._cl - lRange * 2 / 3, self._cl - lRange / 3, self._cl, self._cl + uRange / 3,
                       self._cl + uRange * 2 / 3, self._ucl]
        self._min = self._lcl - lRange * SCALE
        self._max = self._ucl + uRange * SCALE

    def analyze(self):
        self._reportAbnormality(self._analyze(self._point, self._sigma, SPC_analyzer[:5]))

    def getAbnormality(self):
        return self._generateReport(self._analyze(self._point, self._sigma, SPC_analyzer[:5]))

    def generateEchartsDict(self):
        return generatePNpCUEchartsDict(self)


class npChart(pChart):
    def getData(self):
        self._point = np.array([i.p for i in self._original_points])
        self._usl = self._control_plan.usl
        self._lsl = self._control_plan.lsl

        self._cl = np.average(self._point)
        self._ucl = self._cl + 3 * math.sqrt(self._cl * (1 - self._cl / self._size))
        self._lcl = self._cl - 3 * math.sqrt(self._cl * (1 - self._cl / self._size))

        uRange = self._ucl - self._cl
        lRange = self._cl - self._lcl
        self._sigma = [self._lcl, self._cl - lRange * 2 / 3, self._cl - lRange / 3, self._cl, self._cl + uRange / 3,
                       self._cl + uRange * 2 / 3, self._ucl]
        self._min = self._lcl - lRange * SCALE
        self._max = self._ucl + uRange * SCALE


class cChart(pChart):
    def getData(self):
        self._point = np.array([i.p for i in self._original_points])
        self._usl = self._control_plan.usl
        self._lsl = self._control_plan.lsl

        self._cl = np.average(self._point)
        self._ucl = self._cl + 3 * math.sqrt(self._cl)
        self._lcl = self._cl - 3 * math.sqrt(self._cl)

        uRange = self._ucl - self._cl
        lRange = self._cl - self._lcl
        self._sigma = [self._lcl, self._cl - lRange * 2 / 3, self._cl - lRange / 3, self._cl, self._cl + uRange / 3,
                       self._cl + uRange * 2 / 3, self._ucl]
        self._min = self._lcl - lRange * SCALE
        self._max = self._ucl + uRange * SCALE


class uChart(pChart):
    def getData(self):
        self._point = np.array([i.p for i in self._original_points])
        self._usl = self._control_plan.usl
        self._lsl = self._control_plan.lsl

        self._cl = np.average(self._point)
        self._ucl = self._cl + 3 * math.sqrt(self._cl / self._size)
        self._lcl = self._cl - 3 * math.sqrt(self._cl / self._size)

        uRange = self._ucl - self._cl
        lRange = self._cl - self._lcl
        self._sigma = [self._lcl, self._cl - lRange * 2 / 3, self._cl - lRange / 3, self._cl, self._cl + uRange / 3,
                       self._cl + uRange * 2 / 3, self._ucl]
        self._min = self._lcl - lRange * SCALE
        self._max = self._ucl + uRange * SCALE


graphType = {
    'Xbar-R': Xbar_R,
    'Xbar-s': Xbar_s,
    'I-MR': I_MR,
    'p': pChart,
    'np': npChart,
    'c': cChart,
    'u': uChart
}

from warehouse.util.EXAMPLE import *

def getGraph(measure_plan_id, parameter_id, history_points=None):
    control_plan = control_plan_info.objects.get(parameter_id=parameter_id)
    measure_plan = measure_plan_info.objects.get(uid=measure_plan_id)
    if not history_points:
        history_points = control_point_info.objects.filter(control_plan=control_plan,
                                                           measure_form__measure_plan_id=measure_plan_id).order_by('-uid')[
                         :measure_plan.batch_count]
    type = control_plan.get_type_display()

    graph = graphType[type](measure_plan, control_plan, history_points)
    graph.getData()

    # todo: disable this
    uploadData(measurePlanUpdator(measure_plan).generateForm())

    return graph


def getGraphByTime(measure_plan_id, parameter_id, start_time, end_time=None):
    control_plan = control_plan_info.objects.get(parameter_id=parameter_id)
    measure_plan = measure_plan_info.objects.get(uid=measure_plan_id)
    type = control_plan.get_type_display()

    graph = graphType[type](measure_plan, control_plan, None,start_time=start_time, end_time=end_time)
    graph.getData()
    return graph
