import hashlib
import time
import datetime

from datetime import datetime
from imbox import Imbox

from lib import database
from lib import files
from lib import log
from lib import config

script_name = 'Pushwer'


class MailService:
    def __init__(self, white_list_univer_names=None):
        self.mail = Imbox(config.get_argument('mail_server'),
                          username=config.get_argument('mail_login'),
                          password=config.get_argument('mail_pass'),
                          ssl=True,
                          ssl_context=None,
                          starttls=False)
        self.inbox = []
        self.white_list = white_list_univer_names
        self.used_mail_ids = []
        self.db = database.LocalDB()

        self.mail_whitelist_univers = config.get_argument('mail_whitelist_univers')
        self.mail_subject_format = config.get_argument('mail_subject_format')

    class MailObject:
        def __init__(self, m_id, date, subject, body, attach):
            self.msg_id = m_id
            self.date = date
            self.subject = subject
            self.body = body
            self.attach = attach
            # univer vars
            self.univer = ''
            self.fak = ''

        def output_record(self):
            """
            Make dictionary msg object for export
            :return: dict
            """
            out_attach = []
            for att in self.attach:
                out_attach.append({'filename': att['filename'],
                                   'size': att['size'],
                                   'type': att['content-type'],
                                   'content-id': att['content-id']})
            return {'msg_id': self.msg_id,
                    'date': self.date.strftime('%d %b %Y %H:%M:%S'),
                    'univer': self.univer,
                    'fak': self.fak,
                    'subject': self.subject,
                    'body': self.body,
                    'attach': out_attach}

    def get_new_mail_objects(self, remote_mail_list):
        """
        Get new mail object that not listed in local db
        :param remote_mail_list: mail list from mail response
        :return: list of MailObjs
        """
        res_buf = []
        local_mail_list = self.db.get_table_records()

        # if there is local records
        if local_mail_list:
            # make list of local msg ids
            local_mail_list_ids = [i[1] for i in local_mail_list]

            for remote_mail in remote_mail_list:
                if remote_mail.msg_id not in local_mail_list_ids:
                    res_buf.append(remote_mail)

        # add new records if no local records
        else:
            for remote_mail in remote_mail_list:
                res_buf.append(remote_mail)
        return res_buf

    def get_mail_box(self):
        """
        Get all inbox objects
        :return:
        """
        t_inbox = []
        if self.white_list:
            for white in self.white_list:
                un = self.mail_whitelist_univers[white]
                for key in un:
                    # print('Update process started for', key, ':\t', un[key])

                    mail_subj = self.mail_subject_format.format(univer=white,
                                                                fak=key)

                    # filter by fak mail with attach
                    box_mails = self.mail.messages(
                        # date__on=datetime.date(2021, 1, 18),
                        folder='inbox',
                        raw='from:{mail} has:attachment  '.format(sub=mail_subj,
                                                                  mail=un[key]))
                    for one_mail in box_mails:
                        # filter by subject
                        if one_mail[1].subject == mail_subj:
                            # get mail time as object
                            temp_time_str = ' '.join(one_mail[1].date.split()[1:-1:])
                            mail_time = datetime.strptime(temp_time_str, '%d %b %Y %H:%M:%S')
                            # get message id as md5 of original msg id
                            msg_id = hashlib.md5(bytes(one_mail[1].message_id, 'utf-8')).hexdigest()
                            # add mail to pool
                            m = self.MailObject(m_id=msg_id,
                                                date=mail_time,
                                                subject=one_mail[1].subject,
                                                body=one_mail[1].body['plain'][0],
                                                attach=one_mail[1].attachments)
                            m.fak = key
                            m.univer = white
                            t_inbox.append(m)

        new_mails = self.get_new_mail_objects(remote_mail_list=t_inbox)
        if new_mails:
            log.new_mails_print(new_mails)
        # проводим манипуляции с новыми письмами
        files.update_table_files(new_mails)
        # сохраняем обработанные записи в бд
        self.db.save_local_records(records=new_mails)
        # print()  # enable for debug


def run():
    sleep_timer = config.get_argument('sleep_timer_seconds')
    mail_services = [MailService(['КамГУ'])]
    log.start_script(script_name)
    while True:
        for mail in mail_services:
            mail.get_mail_box()
            time.sleep(sleep_timer)


if __name__ == '__main__':
    run()
