#!/usr/bin/env python3
"""
This module connects to Zendesk to update products info
"""
import requests
import sys
import os
from config import MY
from config import ZENDESK_CONFIG


class ZendeskLogin:
    """
    This class contains zendesk login info
    """
    url = 'https://bytefoods.zendesk.com/api/v2/ticket_fields/114094969751.json'
    user = ZENDESK_CONFIG['user']
    pwd = ZENDESK_CONFIG['token']
    headers = {'content-type': 'application/json'}


def db_query():
    """
    This function runs the query and saves results in a file
    """
    my_sql_string = """
SELECT title, 
    id 
    FROM schema1.product 
    ORDER BY title
    """
    qry = MY.engine.execute(my_sql_string)

    f = open('products1.txt', 'w')
    for row in qry.fetchall():
        linne = '{"name": "%s","value": "product_%s"},' % (row[0], row[1])
        f.write(linne)
    f.close()


def unwanted_char():
    """
    This function is used to get rid of unwanted characters
    """
    fille = open("products1.txt")
    lines = fille.readlines()
    fille.close()
    fille1 = open("products1.txt", 'w')
    for line in lines:
        fille1.write(line.encode().decode('ascii', 'ignore'))
    fille1.close()


def remove_comma():
    """
    This function is used to remove last comma from the product file and add 
    """
    fille = open("products1.txt")
    lines = fille.readlines()
    fille.close()
    fille1 = open("products1.txt", 'w')
    for line in lines:
        if line.endswith(','):
            fille1.write('{"ticket_field": {"custom_field_options": [')
            fille1.write(line[:-1])
            fille1.write("] }}")
        else:
            fille1.write('{"ticket_field": {"custom_field_options": [')
            fille1.write(line)
            fille1.write("] }}")
    fille1.close()


def first_entry():
    """
    This function is used to remove everything in zendesk and re-add in order.
        If not, new items will be added out of order
    """
    data = '{"ticket_field": {"custom_field_options": [{"name": "1", "value": "product_1"}]}}'
    response = requests.put(ZendeskLogin.url,
                            data=data,
                            auth=(ZendeskLogin.user, ZendeskLogin.pwd),
                            headers=ZendeskLogin.headers)
    if response.status_code != 200:
        print('Status:', response.status_code)
        exit()


def load_data():
    """
    This function is used to get all data from the product file and load it into zendesk
    """
    fille1 = open("products1.txt")
    lines = fille1.read()
    fille1.close()

    response = requests.put(ZendeskLogin.url,
                            data=lines,
                            auth=(ZendeskLogin.user, ZendeskLogin.pwd),
                            headers=ZendeskLogin.headers)
    if response.status_code != 200:
        print('Status:', response.status_code)
        exit()


def main():
    db_query()
    unwanted_char()
    remove_comma()
    first_entry()
    load_data()


if __name__ == "__main__":
    sys.exit(main())
