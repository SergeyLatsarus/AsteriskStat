class Manager(object):

    def __init__(self, clid, cnam):

        self.caller_id = clid
        self.caller_name = cnam
        self.inbound_calls = 0
        self.outbound_calls = 0
        self.inbound_calls_time = 0
        self.outbound_calls_time = 0
        self.succesed_calls = 0
        self.unsuccesed_calls = 0
        self.total_calls_time = 0
        self.average_time = self.avg_time()
        self.detailsIn = {'00' : Detail('00',0,0,0), '01' : Detail('01',0,0,0),
                        '02' : Detail('02',0,0,0), '03' : Detail('03',0,0,0),
                        '04' : Detail('04',0,0,0), '05' : Detail('05',0,0,0),
                        '06' : Detail('06',0,0,0), '07' : Detail('07',0,0,0),
                        '08' : Detail('08',0,0,0), '09' : Detail('09',0,0,0),
                        '10' : Detail('10',0,0,0), '11' : Detail('11',0,0,0),
                        '12' : Detail('12',0,0,0), '13' : Detail('13',0,0,0),
                        '14' : Detail('14',0,0,0), '15' : Detail('15',0,0,0),
                        '16' : Detail('16',0,0,0), '17' : Detail('17',0,0,0),
                        '18' : Detail('18',0,0,0), '19' : Detail('19',0,0,0),
                        '20' : Detail('20',0,0,0), '21' : Detail('21',0,0,0),
                        '22' : Detail('22',0,0,0), '23' : Detail('23',0,0,0),
                        '24' : Detail('24',0,0,0)}
        self.detailsOut = {'00' : Detail('00',0,0,0), '01' : Detail('01',0,0,0),
                        '02' : Detail('02',0,0,0), '03' : Detail('03',0,0,0),
                        '04' : Detail('04',0,0,0), '05' : Detail('05',0,0,0),
                        '06' : Detail('06',0,0,0), '07' : Detail('07',0,0,0),
                        '08' : Detail('08',0,0,0), '09' : Detail('09',0,0,0),
                        '10' : Detail('10',0,0,0), '11' : Detail('11',0,0,0),
                        '12' : Detail('12',0,0,0), '13' : Detail('13',0,0,0),
                        '14' : Detail('14',0,0,0), '15' : Detail('15',0,0,0),
                        '16' : Detail('16',0,0,0), '17' : Detail('17',0,0,0),
                        '18' : Detail('18',0,0,0), '19' : Detail('19',0,0,0),
                        '20' : Detail('20',0,0,0), '21' : Detail('21',0,0,0),
                        '22' : Detail('22',0,0,0), '23' : Detail('23',0,0,0),
                        '24' : Detail('24',0,0,0)}


    def store_call_in(self, hour, positive_status, negative_status, billed_seconds):

        if hour in self.detailsIn:
            self.detailsIn[hour].duration += int(round(billed_seconds / 60.0))

            self.detailsIn[hour].positive += positive_status

            self.detailsIn[hour].negative += negative_status
        else:
           self.detailsIn[hour] = Detail(hour, positive_status, negative_status, billed_seconds)


    def store_call_out(self, hour, positive_status, negative_status, billed_seconds):

        if hour in self.detailsIn:
            self.detailsOut[hour].duration += int(round(billed_seconds / 60.0))

            self.detailsOut[hour].positive += positive_status

            self.detailsOut[hour].negative += negative_status
        else:
           self.detailsOut[hour] = Detail(hour, positive_status, negative_status, billed_seconds)


    def avg_time(self):

        time = round(self.total_calls_time / float(self.succesed_calls), 1) if self.succesed_calls != 0 else 0
        return time


class Detail(object):

    def __init__(self, hour, positive_call, negative_call, billsec ):

        self.hour = hour
        self.positive = positive_call
        self.negative = negative_call
        self.duration = int(round(billsec / 60.0))



