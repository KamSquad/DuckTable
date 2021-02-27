from lib import config

from io import BytesIO


def verify_attachments(mail_object):
    """
    Function to verify mail attachments with needed conditions
    :type mail_object: target mail object with attachments
    :return: bool
    """
    return True


def update_table_files(mail_objects):
    """
    Function to export attach from incoming mails
    :type mail_objects: specify mail objects to parse
    :return: updated '<project>/attach' folder
    """
    for mail in mail_objects:
        if verify_attachments(mail):  # verify mail object with attachments
            for att in mail.attach:  # for every attachments
                with open(config.get_argument('data_attach_path') + att['filename'], 'wb+') as f:
                    f.write(att['content'].getbuffer())  # write object
