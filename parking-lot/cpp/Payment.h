#pragma once
#include "ParkingTicket.h"
#include <iostream>
#include <iomanip>

class Payment
{
private:
    static int paymentCounter;
    int paymentId;
    double amount;
    string paymentMethod; // "Cash", "Credit Card", "Debit Card"
    string paymentStatus; // "Pending", "Completed", "Failed"
    time_t paymentTime;
    ParkingTicket *ticket;

public:
    Payment(double amt, string method, ParkingTicket *t) : amount(amt), paymentMethod(method), paymentStatus("Pending"), ticket(t), paymentTime(0), paymentId(++paymentCounter) {}

    bool processPayment()
    {
        paymentTime = time(nullptr);
        paymentStatus = "Completed";
        return true;
    }

    void printReceipt() const
    {
        cout << "\n========== PAYMENT RECEIPT ==========\n";
        cout << "Payment ID: " << paymentId << "\n";
        cout << "Ticket ID: " << ticket->getId() << "\n";
        cout << "Vehicle: " << ticket->getVehicle()->getLicenseNumber() << "\n";
        cout << "Amount: $" << fixed << setprecision(2) << amount << "\n";
        cout << "Method: " << paymentMethod << "\n";
        cout << "Duration: " << fixed << setprecision(2)
             << ticket->getDurationInHours() << " hours\n";
        cout << "Payment Time: " << ctime(&paymentTime);
        cout << "Status: " << paymentStatus << "\n";
        cout << "=====================================\n";
    }
    int getId() const { return paymentId; }
    string getStatus() const { return paymentStatus; }
    double getAmount() const { return amount; }
};

int Payment::paymentCounter = 0;