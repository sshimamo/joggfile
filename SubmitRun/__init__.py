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
    try:
        temp = br.form.find_control(name="jog_note[workouts][0][meter]")
    except :
        br.form.new_control('text','jog_note[workouts][0][meter]',{'value':''})
        br.form.new_control('text','jog_note[workouts][0][sec][hour]',{'value':''})
        br.form.new_control('text','jog_note[workouts][0][sec][minute]',{'value':''})
        br.form.new_control('text','jog_note[workouts][0][sec][second]',{'value':''})
        br.form.new_control('text','jog_note[workouts][0][memo]',{'value':''})
        br.form.new_control('text','jog_note[workouts][0][name]',{'value':'run'})
        br.form.fixup()

    rundate = req_body.get('year') + '-' + req_body.get('month') + '-' + req_body.get('day')
    br["jog_note[date]"] = rundate
    br["jog_note[workouts][0][meter]"] = req_body.get('distance')
    br["jog_note[workouts][0][sec][hour]"] = req_body.get('hour')
    br["jog_note[workouts][0][sec][minute]"] = req_body.get('minute')
    br["jog_note[workouts][0][sec][second]"] = req_body.get('second')
    br["jog_note[workouts][0][memo]"] = req_body.get('memo')
    br["jog_note[diary]"] = req_body.get('diary')
    br.submit()

    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
    )
