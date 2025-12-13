// ParkingLot.h
// Central controller for the entire parking lot system
// Pattern: Singleton (ensures only one parking lot instance exists)
// Uses: Strategy Pattern for parking and fee calculations
// Composition: Owns Floors, Panels, manages active Tickets and Reservations

#pragma once
#include <mutex>
#include <vector>
#include <map>
#include "Floor.h"
#include "Panel.h"
#include "ParkingTicket.h"
#include "ParkingStrategy.h"
#include "FeeStrategy.h"
#include "Reservation.h"
#include "Payment.h"
using namespace std;

/**
 * ParkingLot - Main system controller (Singleton Pattern)
 * Thread-safe singleton ensures only one instance exists
 * Orchestrates all parking operations: parking, unparking, reservations, payments
 * Composition: Owns Floors, Panels
 * Association: Manages active Tickets and Reservations
 * Strategy Pattern: Uses ParkingStrategy and FeeStrategy for flexible algorithms
 */
class ParkingLot
{
private:
    static ParkingLot *instance;  // Singleton instance
    static mutex mtx;             // Thread safety for singleton and operations

    // Core components (Composition)
    vector<Floor *> floors;
    vector<EntryPanel *> entryPanels;
    vector<ExitPanel *> exitPanels;

    // Active sessions (Association - manages but doesn't own vehicles/spots)
    map<int, ParkingTicket *> activeTickets;      // Ticket ID -> Ticket
    map<int, Reservation *> activeReservations;   // Reservation ID -> Reservation

    // Strategy Pattern - Interchangeable algorithms
    ParkingStrategy *parkingStrategy;  // How to select parking spots
    FeeStrategy *feeStrategy;          // How to calculate fees

    double totalRevenue;  // Track total revenue

    /**
     * Private constructor - Part of Singleton pattern
     * Initializes with default strategies
     */
    ParkingLot() : totalRevenue(0.0)
    {
        parkingStrategy = new NearestFirstStrategy();  // Default: nearest spot
        feeStrategy = new HourlyFeeStrategy();         // Default: flat hourly rate
    }

public:
    /**
     * Singleton getInstance() - Thread-safe Double-Checked Locking
     * Returns the single instance of ParkingLot
     * Thread-safe: Uses mutex to prevent race conditions
     */
    static ParkingLot *getInstance()
    {
        if (instance == nullptr)  // First check (fast path)
        {
            lock_guard<mutex> lock(mtx);  // Acquire lock
            if (instance == nullptr)       // Second check (inside lock)
            {
                instance = new ParkingLot();
            }
        }
        return instance;
    }

    // Prevent copying (Singleton pattern)
    ParkingLot(const ParkingLot &) = delete;
    ParkingLot &operator=(const ParkingLot &) = delete;

    // Destructor - Clean up all owned resources
    ~ParkingLot()
    {
        for (auto floor : floors)
            delete floor;
        for (auto panel : entryPanels)
            delete panel;
        for (auto panel : exitPanels)
            delete panel;
        for (auto &pair : activeTickets)
            delete pair.second;
        for (auto &pair : activeReservations)
            delete pair.second;
        delete parkingStrategy;
        delete feeStrategy;
    }

    // ========== ADMIN/SETUP METHODS ==========

    // Add a floor to the parking lot
    void addFloor(Floor *floor)
    {
        lock_guard<mutex> lock(mtx);
        floors.push_back(floor);
    }

    // Add an entry panel
    void addEntryPanel(EntryPanel *panel)
    {
        lock_guard<mutex> lock(mtx);
        entryPanels.push_back(panel);
    }

    // Add an exit panel
    void addExitPanel(ExitPanel *panel)
    {
        lock_guard<mutex> lock(mtx);
        exitPanels.push_back(panel);
    }

    /**
     * Change parking spot selection strategy at runtime
     * Strategy Pattern: Allows switching algorithms dynamically
     */
    void setParkingStrategy(ParkingStrategy *strategy)
    {
        lock_guard<mutex> lock(mtx);
        delete parkingStrategy;
        parkingStrategy = strategy;
    }

    /**
     * Change fee calculation strategy at runtime
     * Strategy Pattern: Allows switching pricing models dynamically
     */
    void setFeeStrategy(FeeStrategy *strategy)
    {
        lock_guard<mutex> lock(mtx);
        delete feeStrategy;
        feeStrategy = strategy;
    }

    // ========== RESERVATION METHODS ==========(

    /**
     * Reserve a parking spot in advance
     * Uses parking strategy to find best available spot
     * Marks spot as reserved for specified duration
     */
    Reservation *reserveSpot(Vehicle *vehicle, int durationHours = 2)
    {
        lock_guard<mutex> lock(mtx);
        vector<ParkingSpot *> allAvailable;

        // Collect all available spots from all floors
        for (Floor *floor : floors)
        {
            vector<ParkingSpot *> floorSpots = floor->getAllAvailableSpots();
            allAvailable.insert(allAvailable.end(), floorSpots.begin(), floorSpots.end());
        }

        // Use strategy to find best spot
        ParkingSpot *spot = parkingStrategy->findSpot(allAvailable, vehicle);

        if (!spot)
        {
            cout << "X No spot available for reservation\n";
            return nullptr;
        }

        // Create and track reservation
        Reservation *reservation = new Reservation(vehicle, spot, durationHours);
        activeReservations[reservation->getId()] = reservation;

        cout << "✓ Reservation created! ID: " << reservation->getId() << "\n";
        return reservation;
    }

    /**
     * Cancel an existing reservation
     * Frees up the reserved spot
     */
    bool cancelReservation(int reservationId)
    {
        lock_guard<mutex> lock(mtx);

        auto it = activeReservations.find(reservationId);
        if (it == activeReservations.end())
        {
            return false;
        }

        it->second->cancel();  // Unreserves the spot
        delete it->second;
        activeReservations.erase(it);
        return true;
    }

    // ========== PARKING OPERATIONS ==========

    /**
     * Park a vehicle (with or without reservation)
     * Two modes:
     *   1. With reservation: Uses pre-reserved spot
     *   2. Without reservation: Finds available spot using strategy
     * Creates and returns a ParkingTicket for fee calculation
     */
    ParkingTicket *parkVehicle(Vehicle *vehicle, int reservationId = -1)
    {
        lock_guard<mutex> lock(mtx);
        ParkingSpot *spot = nullptr;

        // Mode 1: Parking with reservation
        if (reservationId != -1)
        {
            auto activeReservation = activeReservations.find(reservationId);
            if (activeReservation != activeReservations.end() && activeReservation->second->isValid())
            {
                spot = activeReservation->second->getSpot();
                activeReservation->second->complete();  // Mark reservation complete
                activeReservations.erase(activeReservation);
            }
            else
            {
                cout << "✗ Invalid or expired reservation\n";
                return nullptr;
            }
        }
        // Mode 2: Regular parking without reservation
        else
        {
            // Collect all available spots
            vector<ParkingSpot *> allAvailable;
            for (Floor *floor : floors)
            {
                vector<ParkingSpot *> floorSpots = floor->getAllAvailableSpots();
                allAvailable.insert(allAvailable.end(), floorSpots.begin(), floorSpots.end());
            }

            if (allAvailable.empty())
            {
                cout << "✗ Parking lot is full\n";
                return nullptr;
            }

            // Use strategy to select best spot
            spot = parkingStrategy->findSpot(allAvailable, vehicle);
        }

        // Attempt to park vehicle in selected spot
        if (!spot || !spot->park(vehicle))
        {
            cout << "✗ Failed to park vehicle\n";
            return nullptr;
        }

        // Create ticket and track it
        ParkingTicket *ticket = new ParkingTicket(vehicle, spot);
        activeTickets[ticket->getId()] = ticket;

        cout << "\n✓ Vehicle parked successfully!\n";
        cout << "Strategy: " << parkingStrategy->getName() << "\n";
        ticket->printTicket();

        return ticket;
    }
    /**
     * Unpark a vehicle and process payment
     * Steps:
     *   1. Mark ticket exit time
     *   2. Calculate fee using fee strategy
     *   3. Process payment
     *   4. Unpark vehicle from spot
     *   5. Clean up ticket
     */
    Payment *unparkVehicle(int ticketId, string paymentMethod)
    {
        lock_guard<mutex> lock(mtx);

        auto it = activeTickets.find(ticketId);
        if (it == activeTickets.end())
        {
            cout << "✗ Invalid ticket ID\n";
            return nullptr;
        }

        ParkingTicket *ticket = it->second;
        ticket->markExit();  // Record exit time

        // Calculate fee using current fee strategy
        double fee = feeStrategy->calculateFee(ticket);
        cout << "\nFee Strategy: " << feeStrategy->getName() << "\n";
        cout << "Total Fee: $" << fixed << setprecision(2) << fee << "\n";

        // Process payment and print receipt
        Payment *payment = new Payment(fee, paymentMethod, ticket);
        payment->processPayment();
        payment->printReceipt();
        totalRevenue += fee;

        // Free up the parking spot
        ticket->getSpot()->unpark();

        // Clean up ticket
        activeTickets.erase(it);
        delete ticket;

        return payment;
    }

    // ========== STATUS & REPORTING ==========

    /**
     * Display complete parking lot status
     * Shows active tickets, reservations, strategies, revenue, floor status
     */
    void displayStatus() const
    {
        lock_guard<mutex> lock(mtx);

        cout << "\n========== PARKING LOT STATUS ==========\n";
        cout << "Active Tickets: " << activeTickets.size() << "\n";
        cout << "Active Reservations: " << activeReservations.size() << "\n";
        cout << "Parking Strategy: " << parkingStrategy->getName() << "\n";
        cout << "Fee Strategy: " << feeStrategy->getName() << "\n";
        cout << "Total Revenue: $" << fixed << setprecision(2) << totalRevenue << "\n\n";

        for (Floor *floor : floors)
        {
            floor->displayStatus();
        }
        cout << "========================================\n";
    }

    // Check if parking lot is completely full
    bool isFull() const
    {
        lock_guard<mutex> lock(mtx);
        for (Floor *floor : floors)
        {
            if (floor->getTotalAvailableSpots() > 0)
            {
                return false;
            }
        }
        return true;
    }

    // Get total revenue collected
    double getTotalRevenue() const
    {
        lock_guard<mutex> lock(mtx);
        return totalRevenue;
    }
};

ParkingLot *ParkingLot::instance = nullptr;
mutex ParkingLot::mtx;