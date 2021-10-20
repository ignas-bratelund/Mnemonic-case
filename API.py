from flask import Flask
from connector import dbQuery, dbQueryList
from flask_restful import Resource, Api, reqparse
import time

app = Flask(__name__)
api = Api(app)

class Accounts(Resource):

    def get(self):
        result = dbQuery("SELECT * FROM mnemonic.account;")
        if isinstance(result, list):
            data = {}
            for row in result:
                data["account" + str(row[0])] = {'id': row[0], 'name': row[1], 'availableCash': row[2]}
            return {'accounts': data}, 200 
        else:
            return str(result), 400


class Transactions(Resource):
    
    def transactionResultToDict(self, result):
        transaction_dict = {}
        for row in result:
            transaction_dict["transaction" + str(row[0])] = {'id': row[0], 'registeredTime': row[1],
            'executedTime': row[2], 'success': bool(row[3]), 'cashAmount': row[4],
            'sourceAccount': row[5], 'destinationAccount': row[6]}
        return transaction_dict

    def get(self):
        result = dbQuery("SELECT * FROM mnemonic.transaction;")
        if isinstance(result, list):
            data = self.transactionResultToDict(result)
            return {'transactions': data}, 200 
        else:
            return str(result), 400

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('cashAmount', required=True)
        parser.add_argument('sourceAccount', required=True)
        parser.add_argument('destinationAccount', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        
        if float(args["cashAmount"]) < 0:
            return "CashAmount has to be a positive number", 400

        #Adds unfinished transaction
        result = dbQuery("Insert into mnemonic.transaction(registeredTime, success, cashAmount,"+
         "sourceAccount, destinationAccount) values("+ str(int(time.time()*1000.0)) +
         ", 0 ,"+ str(args["cashAmount"]) +","+ str(args["sourceAccount"]) + ","+ 
         str(args["destinationAccount"]) +");")
        
        #if not there are id or internal errors
        if isinstance(result, list):
            #checks that source account has enough funds
            source_account_funds = dbQuery("SELECT availableCash FROM Account WHERE id="+ str(args["sourceAccount"]))[0][0]
            if source_account_funds < int(args["cashAmount"]):
                return "The source account does not have enough funds available", 400

            #Transfers the money in a single access to the db to reduce error
            #NB: ikke en bra løsning, problemer hvis det er mange transaksjoner
            dbQueryList(["UPDATE Account SET availableCash = availableCash - "+ 
            str(args["cashAmount"] + " WHERE id=" + str(args["sourceAccount"])),
            "UPDATE Account SET availableCash = availableCash + "+ 
            str(args["cashAmount"] + " WHERE id=" + str(args["destinationAccount"]))])
            
            #Updates success and executedTime of transaction
            dbQuery("UPDATE Transaction SET success = 1, executedTime="+ str(int(time.time()*1000.0)) +" ORDER BY id DESC LIMIT 1")

            data = self.transactionResultToDict(dbQuery("SELECT * FROM transaction ORDER BY id DESC LIMIT 1"))
            return data, 200 
        else:
            #Code for foreign key not found
            if str(result)[:4] == "1452":
                return "One of the accounts does not exist", 400
            return "Some internal error in the system", 400

        return "It should be imposible to get here", 400

api.add_resource(Accounts, '/accounts')
api.add_resource(Transactions, '/transactions')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=105)