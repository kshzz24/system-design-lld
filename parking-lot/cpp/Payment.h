// Payment.h
// Represents a payment transaction for parking fees
// Association: Links to a ParkingTicket
// Purpose: Tracks payment details and provides receipt generation

#pragma once
#include "ParkingTicket.h"
#include <iostream>
#include <iomanip>

/**
 * Payment - Records payment transaction when vehicle exits
 * Association: References the ParkingTicket being paid for
 * Future: Can be extended for different payment processors, refunds
 */
class Payment
{
private:
    static int paymentCounter;  // Auto-incrementing payment ID
    int paymentId;
    double amount;              // Total amount paid
    string paymentMethod;       // "Cash", "Credit Card", "Debit Card"
    string paymentStatus;       // "Pending", "Completed", "Failed"
    time_t paymentTime;         // When payment was processed
    ParkingTicket *ticket;      // Associated ticket (Association)

public:
    /**
     * Constructor - Create payment record
     * Initial status is "Pending" until processed
     */
    Payment(double amt, string method, ParkingTicket *t)
        : amount(amt), paymentMethod(method), paymentStatus("Pending"),
          ticket(t), paymentTime(0), paymentId(++paymentCounter) {}

    /**
     * Process the payment
     * In real system: Would integrate with payment gateway
     */
    bool processPayment()
    {
        paymentTime = time(nullptr);
        paymentStatus = "Completed";
        return true; // In real system: return gateway response
    }

    // Generate and display payment receipt
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

    // Getters
    int getId() const { return paymentId; }
    string getStatus() const { return paymentStatus; }
    double getAmount() const { return amount; }
};

int Payment::paymentCounter = 0;