import datetime


def start_script(service_name):
    print('{c_time}\tService {s_name} started, listen mails..'
          .format(c_time=datetime.datetime.now(),
                  s_name=service_name))


def new_mails_print(new_mails):
    mail_list = []
    # add unique list of unique mails
    for m in new_mails:
        mail_str = '{uni}-{fak}'.format(uni=m.univer,
                                        fak=m.fak)
        if mail_str not in mail_list:
            mail_list.append(mail_str)
    print('{c_time}\tNew mails: count={mail_count}\tlist={m_list}'.format(
        c_time=datetime.datetime.now(),
        mail_count=len(new_mails),
        m_list=mail_list)
    )
