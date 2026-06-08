from datetime import datetime
from constants.transaction import OperationType,TransactionStatus

class Transaction:
    transaction_id: str
    operation_type: OperationType
    amount:float
    timestamp:datetime
    status: TransactionStatus
    
    def __init__(self, transaction_id:str, operation_type:OperationType, amount:float )->None:
        self.transaction_id = transaction_id
        self.operation_type = operation_type
        self.amount = amount
        self.status = TransactionStatus.FAILED
        self.timestamp = datetime.now()


    def get_receipt(self)->str:
        receipt = f"""
        
        Transaction ID : {self.transaction_id}
        Transaction Type : {self.operation_type}
        Amount: {self.amount}
        Status: {self.status}
        Time : { self.timestamp}
        """

        return receipt

