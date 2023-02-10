import threading
from queue import Queue

from flask import Flask, request, render_template, redirect, url_for

from src.web.FlaskAppWrapper import FlaskAppWrapper




class ThreadFlask(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.app=Flask(__name__)
        self.user_input=None

    def run(self):
        flask_wrapper=FlaskAppWrapper(self.app)
        flask_wrapper.add_endpoint('/', 'root', self.select_coordinator_index, methods=["GET","POST"])
        flask_wrapper.add_endpoint('/transactions', "transactions", self.create_transaction_index, methods=["GET","POST"])
        flask_wrapper.run()

    def select_coordinator_index(self):
        if request.method == 'POST':
            coordinator = request.form['coordinator']
            self.user_input=(coordinator,None)
            return redirect(url_for("transactions"))
        return render_template("index.html")


    def create_transaction_index(self):
        if request.method == 'POST':
            amount = request.form['amount']
            # Do something with the coordinator and data values
            self.user_input=self.user_input[0],amount
            return redirect(url_for("transactions"))
        return render_template("create_transactions.html")












