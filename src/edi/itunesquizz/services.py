from plone.rest import Service
import ast
import jsonlib
from Products.Five import BrowserView

class ValidateAufgabe(BrowserView):

    def __call__(self):
        data = self.request.get('data')
        data = ast.literal_eval(data)
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
        self.request.response.setHeader("Content-type", "application/json")     
        self.request.response.setHeader("Access-Control-Allow-Origin", "*")     
        retdict = {'result':result,
                   'solution':solution}
        payload = jsonlib.write(retdict)
        return payload
