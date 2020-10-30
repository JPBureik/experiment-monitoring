#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:39:24 2020

@author: jp
"""

import smtplib, ssl
from auxil_p import mail
import datetime


port = 465  # For SSL
password = mail()

sender_email = "jan-philipp.bureik@institutoptique.fr"
receiver_email = "jan-philipp.bureik@institutoptique.fr"

message = """\
Subject: Experiment Surveillance Alert

This message is an automatic alert to inform you that on %s the experiment
parameter depassed the critical value.""" % (datetime.datetime.now().strftime("%m/%d %H:%M"))

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtps.u-psud.fr", port, context=context) as server:
    server.login("jan-philipp.bureik@institutoptique.fr", password)
    server.sendmail(sender_email, receiver_email, message)
password = ''