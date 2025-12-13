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

class ParkingLot
{
private:
    static ParkingLot *instance;
    static mutex mtx;

    vector<Floor *> floors;
    vector<EntryPanel *> entryPanels;
    vector<ExitPanel *> exitPanels;
    map<int, ParkingTicket *> activeTickets;
    map<int, Reservation *> activeReservations;

    ParkingStrategy *parkingStrategy;
    FeeStrategy *feeStrategy;

    double totalRevenue;
    ParkingLot() : totalRevenue(0.0)
    {
        parkingStrategy = new NearestFirstStrategy();
        feeStrategy = new HourlyFeeStrategy();
    }

public:
    static ParkingLot *getInstance()
    {
        if (instance == nullptr)
        {
            lock_guard<mutex> lock(mtx);
            if (instance == nullptr)
            {
                instance = new ParkingLot();
            }
        }
        return instance;
    }
    ParkingLot(const ParkingLot &) = delete;
    ParkingLot &operator=(const ParkingLot &) = delete;
    ~ParkingLot()
    {
        // TODO: Delete all resources
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
    // admin

    void addFloor(Floor *floor)
    {
        lock_guard<mutex> lock(mtx);
        floors.push_back(floor);
    }
    void addEntryPanel(EntryPanel *panel)
    {
        lock_guard<mutex> lock(mtx);
        entryPanels.push_back(panel);
    }
    void addExitPanel(ExitPanel *panel)
    {
        lock_guard<mutex> lock(mtx);
        exitPanels.push_back(panel);
    }

    void setParkingStrategy(ParkingStrategy *strategy)
    {
        lock_guard<mutex> lock(mtx);
        delete parkingStrategy;
        parkingStrategy = strategy;
    }
    void setFeeStrategy(FeeStrategy *strategy)
    {
        lock_guard<mutex> lock(mtx);
        delete feeStrategy;
        feeStrategy = strategy;
    }

    Reservation *reserveSpot(Vehicle *vehicle, int durationHours = 2)
    {
        lock_guard<mutex> lock(mtx);
        vector<ParkingSpot *> allAvailable;

        for (Floor *floor : floors)
        {
            vector<ParkingSpot *> floorSpots = floor->getAllAvailableSpots();
            allAvailable.insert(allAvailable.end(), floorSpots.begin(), floorSpots.end());
        }
        ParkingSpot *spot = parkingStrategy->findSpot(allAvailable, vehicle);

        if (!spot)
        {
            cout << "X No spot available for reservation\n";
            return nullptr;
        }

        Reservation *reservation = new Reservation(vehicle, spot, durationHours);
        activeReservations[reservation->getId()] = reservation;

        cout << "✓ Reservation created! ID: " << reservation->getId() << "\n";
        return reservation;
    }
    bool cancelReservation(int reservationId)
    {
        lock_guard<mutex> lock(mtx);

        auto it = activeReservations.find(reservationId);
        if (it == activeReservations.end())
        {
            return false;
        }

        it->second->cancel();
        delete it->second;
        activeReservations.erase(it);
        return true;
    }

    ParkingTicket *parkVehicle(Vehicle *vehicle, int reservationId = -1)
    {
        lock_guard<mutex> lock(mtx);
        ParkingSpot *spot = nullptr;
        if (reservationId != -1)
        {
            auto activeReservation = activeReservations.find(reservationId);
            if (activeReservation != activeReservations.end() && activeReservation->second->isValid())
            {
                spot = activeReservation->second->getSpot();
                activeReservation->second->complete();
                activeReservations.erase(activeReservation);
            }
            else
            {
                cout << "✗ Invalid or expired reservation\n";
                return nullptr;
            }
        }
        else
        {
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
            spot = parkingStrategy->findSpot(allAvailable, vehicle);
        }
        if (!spot || !spot->park(vehicle))
        {
            cout << "✗ Failed to park vehicle\n";
            return nullptr;
        }
        ParkingTicket *ticket = new ParkingTicket(vehicle, spot);
        activeTickets[ticket->getId()] = ticket;
        cout << "\n✓ Vehicle parked successfully!\n";
        cout << "Strategy: " << parkingStrategy->getName() << "\n";
        ticket->printTicket();

        return ticket;
    }
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
        ticket->markExit();

        double fee = feeStrategy->calculateFee(ticket);
        cout << "\nFee Strategy: " << feeStrategy->getName() << "\n";
        cout << "Total Fee: $" << fixed << setprecision(2) << fee << "\n";

        Payment *payment = new Payment(fee, paymentMethod, ticket);
        payment->processPayment();
        payment->printReceipt();
        totalRevenue += fee;

        ticket->getSpot()->unpark();

        activeTickets.erase(it);
        delete ticket;

        return payment;
    }
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
    double getTotalRevenue() const
    {
        lock_guard<mutex> lock(mtx);
        return totalRevenue;
    }
};

ParkingLot *ParkingLot::instance = nullptr;
mutex ParkingLot::mtx;