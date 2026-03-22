from vending_machine import VendingMachine
from money import Coin, Note


def main():
    # Get singleton instance
    machine = VendingMachine.get_instance()

    # Stock the machine
    machine.add_item("A1", "Coke", 50, 5)
    machine.add_item("A2", "Pepsi", 45, 3)
    machine.add_item("A3", "Water", 25, 10)

    # === Test 1: Happy path - exact change ===
    print("=== Test 1: Buy Coke (price=50) with exact change ===")
    machine.insert_coin(Coin.QUARTER)  # balance = 25
    machine.insert_coin(Coin.QUARTER)  # balance = 50
    machine.select_item("A1")
    machine.dispense()
    print(f"Balance after: {machine.balance}")
    print()

    # === Test 2: Buy with change ===
    print("=== Test 2: Buy Water (price=25) with overpayment ===")
    machine.insert_coin(Coin.QUARTER)  # balance = 25
    machine.insert_coin(Coin.DIME)     # balance = 35
    machine.select_item("A3")
    machine.dispense()
    print(f"Balance after: {machine.balance}")
    print()

    # === Test 3: Buy with a note ===
    print("=== Test 3: Buy Pepsi (price=45) with $1 note ===")
    machine.insert_note(Note.ONE)  # balance = 100
    machine.select_item("A2")
    machine.dispense()
    print(f"Balance after: {machine.balance}")
    print()

    # === Test 4: Not enough money ===
    print("=== Test 4: Try to buy Coke with only 1 dime ===")
    machine.insert_coin(Coin.DIME)  # balance = 10
    machine.select_item("A1")       # Should print insufficient balance
    print(f"Balance: {machine.balance}")
    print()

    # === Test 5: Refund ===
    print("=== Test 5: Refund from HasMoneyState ===")
    machine.refund_balance()  # Should go back to IdleState
    print(f"Balance after refund: {machine.balance}")
    print()

    # === Test 6: Invalid operations ===
    print("=== Test 6: Invalid operations in IdleState ===")
    machine.select_item("A1")  # Should print "Please Enter coin first"
    machine.dispense()          # Should print "Invalid Operation"
    print()

    # === Test 7: Item not found ===
    print("=== Test 7: Select non-existent item ===")
    machine.insert_coin(Coin.QUARTER)
    machine.select_item("Z9")  # Should print "Item Z9 not available"
    machine.refund_balance()
    print()


if __name__ == "__main__":
    main()
