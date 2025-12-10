#pragma once
#include <string>
#include <ctime>
#include <iostream>
#include <iomanip>
#include "Vehicle.h"
#include "ParkingSpot.h"

using namespace std;

class ParkingTicket
{
    static int ticketCounter;

private:
    int ticketId;
    Vehicle *vehicle;
    ParkingSpot *spot;
    time_t entryTime;
    time_t exitTime;
    bool isActive;

public:
    ParkingTicket(Vehicle *v, ParkingSpot *s)
        : vehicle(v), spot(s), exitTime(0), isActive(true),
          entryTime(time(nullptr)), ticketId(++ticketCounter) {}

    void markExit()
    {
        exitTime = time(nullptr);
        isActive = false;
    }

    double getDurationInHours() const
    {
        time_t endTime = (exitTime == 0) ? time(nullptr) : exitTime;
        double seconds = difftime(endTime, entryTime);
        return seconds / 3600.0;
    }

    int getId() const { return ticketId; }
    Vehicle *getVehicle() const { return vehicle; }
    ParkingSpot *getSpot() const { return spot; }
    time_t getEntryTime() const { return entryTime; }
    time_t getExitTime() const { return exitTime; }
    bool getIsActive() const { return isActive; }

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