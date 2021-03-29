import rpa as r



r.init(visual_automation = True)
r.dclick('outlook_icon.png')
r.click('new_mail.png')
...
r.type('message_box.png', 'message')
r.click('send_button.png')
r.close()