// ParkingTicket.h
// Represents a parking ticket issued when a vehicle parks
// Association: Links a Vehicle to a ParkingSpot and tracks parking duration
// Purpose: Used for fee calculation and tracking active parking sessions

#pragma once
#include <string>
#include <ctime>
#include <iostream>
#include <iomanip>
#include "Vehicle.h"
#include "ParkingSpot.h"

using namespace std;

/**
 * ParkingTicket - Issued when a vehicle enters and parks
 * Association: References both Vehicle and ParkingSpot
 * Tracks entry/exit time for fee calculation
 */
class ParkingTicket
{
    static int ticketCounter; // Auto-incrementing ticket ID generator

private:
    int ticketId;             // Unique ticket identifier
    Vehicle *vehicle;         // Associated vehicle (Association)
    ParkingSpot *spot;        // Associated parking spot (Association)
    time_t entryTime;         // When vehicle entered
    time_t exitTime;          // When vehicle exited (0 if still parked)
    bool isActive;            // Is this ticket still active?

public:
    /**
     * Constructor - Create ticket when vehicle parks
     * Automatically sets entry time and generates unique ID
     */
    ParkingTicket(Vehicle *v, ParkingSpot *s)
        : vehicle(v), spot(s), exitTime(0), isActive(true),
          entryTime(time(nullptr)), ticketId(++ticketCounter) {}

    // Mark the vehicle as exited (called during unparking)
    void markExit()
    {
        exitTime = time(nullptr);
        isActive = false;
    }

    /**
     * Calculate parking duration in hours
     * If not exited yet, uses current time
     */
    double getDurationInHours() const
    {
        time_t endTime = (exitTime == 0) ? time(nullptr) : exitTime;
        double seconds = difftime(endTime, entryTime);
        return seconds / 3600.0; // Convert seconds to hours
    }

    // Getters
    int getId() const { return ticketId; }
    Vehicle *getVehicle() const { return vehicle; }
    ParkingSpot *getSpot() const { return spot; }
    time_t getEntryTime() const { return entryTime; }
    time_t getExitTime() const { return exitTime; }
    bool getIsActive() const { return isActive; }

    // Display ticket information
    void printTicket() const
    {
        cout << "\n========== PARKING TICKET ==========\n";
        cout << "Ticket ID: " << ticketId << "\n";
        cout << "Vehicle: " << vehicle->getLicenseNumber() << "\n";
        cout << "Spot: " << spot->getId() << " (Floor " << spot->getFloor() << ")\n";
        cout << "Entry Time: " << ctime(&entryTime);
        cout << "====================================\n";
    }
};

int ParkingTicket::ticketCounter = 0;