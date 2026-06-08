from enum import Enum

class TransactionStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class OperationType(Enum):
    WITHDRAW  = "WITHDRAW"
    DEPOSIT  = "DEPOSIT"
    CHECK_BALANCE  = "CHECK_BALANCE"