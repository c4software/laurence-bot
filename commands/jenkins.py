import json
from rest import callrest
from settings import JENKINS_DOMAIN, JENKIN_PORT
from libs import make_message
from .decorators import register_as_command

@register_as_command("jstatus", "Affiche la liste des builds en cours", "Jenkins")
def cmd_building(data):
    data = get_jenkins_data("/api/json")
    currently_building = []
    data = json.loads(data)
    if "jobs" in data:
        for job in data['jobs']:
            if "_anime" in job['color']:
                currently_building.append("{0} ({1})".format(job['name'], job['url']))

    message = "Aucun build en cours"
    if currently_building:
        message = "- {0}".format("\r\n- ".join(currently_building))

    return make_message("Jenkins", "http://jenkins.dev:8070/static/b68f063e/favicon.ico", message,"", "Liste des builds", "http://jenkins.dev:8070/", message, "#7A9EC5")

@register_as_command("jbuild", "Lancer un build (Ex: jbuild wifilib)", "Jenkins")
def cmd_build(data):
    job = data["text"][0].split(' ')[2]
    get_jenkins_data("/job/{0}/build".format(job))
    return make_message("Jenkins", "http://jenkins.dev:8070/static/b68f063e/favicon.ico","Lancement du build ok.","", "Lancement du build", "http://jenkins.dev:8070/job/{0}".format(job), "Lancement du build OK.", "#7A9EC5")

def get_jenkins_data(path):
    try:
        return callrest(domain=JENKINS_DOMAIN,port=JENKIN_PORT, path=path, params={})[2]
    except:
        return "{}"
