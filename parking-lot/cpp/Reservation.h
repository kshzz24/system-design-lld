// Reservation.h
#pragma once
#include "Vehicle.h"
#include "ParkingSpot.h"
#include <ctime>
#include <iostream>

using namespace std;

class Reservation
{
private:
    static int reservationCounter;
    int reservationId;
    Vehicle *vehicle;
    ParkingSpot *spot;
    time_t reservedFrom;
    time_t reservedTo;
    string status;

public:
    Reservation(Vehicle *v, ParkingSpot *s, int durationHours = 2) : vehicle(v), spot(s), status("Active"), reservationId(++reservationCounter)
    {
        reservedFrom = time(nullptr);
        reservedTo = reservedFrom + (durationHours * 3600);
        spot->reserve();
    }
    bool isExpired() const
    {
        return time(nullptr) > reservedTo;
    }

    bool isValid() const
    {
        return status == "Active" && !isExpired();
    }

    void complete()
    {
        status = "Completed";
        spot->unreserve();
    }

    void cancel()
    {
        status = "Cancelled";
        spot->unreserve();
    }

    int getId() const { return reservationId; }
    Vehicle *getVehicle() const { return vehicle; }
    ParkingSpot *getSpot() const { return spot; }
    string getStatus() const { return status; }
    time_t getReservedFrom() const { return reservedFrom; }
    time_t getReservedTo() const { return reservedTo; }
};

int Reservation::reservationCounter = 0;