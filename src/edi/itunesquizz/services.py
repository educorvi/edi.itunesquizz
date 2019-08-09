from plone.rest import Service

class ValidateAufgabe(Service):

    def render(self):
        data = self.request.get('data')
        result = True
        solution = []
        for i in self.context.antworten:
            if i.get('bewertung') == 'richtig':
                solution.append(True)
                if not self.context.antworten.index(i) in data:
                    result = False
            else:
                solution.append(False)
                if self.context.antworten.index(i) in data:
                    result = False
        import pdb;pdb.set_trace()
        retdict = {'result':result,
                   'solution':solution}
        return str(retdict)
