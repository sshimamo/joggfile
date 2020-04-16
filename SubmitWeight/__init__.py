import logging
import azure.functions as func
import mechanize

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    br = mechanize.Browser()
    br.set_handle_robots( False )
    br.open("https://joggfile.com/")

    br.select_form(nr=0)
    br["signin[login_name]"] = req_body.get('email')
    br["signin[password]"] = req_body.get('password')
    br.submit()
    br.open("https://joggfile.com/jog_note/new")
    br.select_form(nr=0)
    rundate = req_body.get('year') + '-' + req_body.get('month') + '-' + req_body.get('day')
    br["jog_note[date]"] = rundate
    br["jog_note[physical_condition][weight]"] = req_body.get('weight') 
    br.submit()

    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
    )