from zope.interface import Interface
from uvc.api import api

api.templatedir('templates')

class TimerPage(api.Page):
    api.context(Interface)

    def update(self):
        self.timersnippet = """\
          <script>
            var timeleft = 15;
            var downloadTimer = setInterval(function(){
            document.getElementById("progressBar").value = 15 - timeleft;
            timeleft -= 1;
            if(timeleft <= 0)
            clearInterval(downloadTimer);
            }, 1000);
          </script>"""

        self.texttimer = """\
          <script>
            var timeleft = 15;
            var downloadTimer = setInterval(function(){
            document.getElementById("countdown").innerHTML = timeleft + " Sekunden verbleiben";
            timeleft -= 1;
            if(timeleft <= 0){
            clearInterval(downloadTimer);
            document.getElementById("countdown").innerHTML = "Zeit abgelaufen"
            }
            }, 1000);
          </script>"""

        self.delaysnippet = """\
          <script>
            setTimeout("location.href = '@@delaypage';",15000);
          </script>"""


class DelayPage(api.Page):
    api.context(Interface)


    def render(self):
        return '<h1>Hey, eingeschlafen??</h1>'

