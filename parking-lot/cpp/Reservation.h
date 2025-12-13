// Reservation.h
// Represents a parking spot reservation made in advance
// Association: Links a Vehicle to a reserved ParkingSpot for a time window
// Purpose: Allows advance booking and guarantees spot availability

#pragma once
#include "Vehicle.h"
#include "ParkingSpot.h"
#include <ctime>
#include <iostream>

using namespace std;

/**
 * Reservation - Pre-booking of a parking spot
 * Association: References both Vehicle and ParkingSpot
 * Time-based: Has validity period (reservedFrom to reservedTo)
 * States: Active -> Completed (when used) or Cancelled
 */
class Reservation
{
private:
    static int reservationCounter; // Auto-incrementing reservation ID
    int reservationId;
    Vehicle *vehicle;              // Vehicle for this reservation (Association)
    ParkingSpot *spot;            // Reserved spot (Association)
    time_t reservedFrom;          // Reservation start time
    time_t reservedTo;            // Reservation end time
    string status;                // "Active", "Completed", "Cancelled"

public:
    /**
     * Constructor - Create a new reservation
     * Automatically marks the spot as reserved
     */
    Reservation(Vehicle *v, ParkingSpot *s, int durationHours = 2)
        : vehicle(v), spot(s), status("Active"), reservationId(++reservationCounter)
    {
        reservedFrom = time(nullptr);
        reservedTo = reservedFrom + (durationHours * 3600); // Convert hours to seconds
        spot->reserve(); // Mark spot as reserved
    }

    // Check if reservation time window has passed
    bool isExpired() const
    {
        return time(nullptr) > reservedTo;
    }

    // Valid = Active status AND not expired
    bool isValid() const
    {
        return status == "Active" && !isExpired();
    }

    // Mark reservation as completed (when vehicle actually parks)
    void complete()
    {
        status = "Completed";
        spot->unreserve(); // Free the spot's reserved flag
    }

    // Cancel the reservation
    void cancel()
    {
        status = "Cancelled";
        spot->unreserve(); // Free the spot's reserved flag
    }

    // Getters
    int getId() const { return reservationId; }
    Vehicle *getVehicle() const { return vehicle; }
    ParkingSpot *getSpot() const { return spot; }
    string getStatus() const { return status; }
    time_t getReservedFrom() const { return reservedFrom; }
    time_t getReservedTo() const { return reservedTo; }
};

int Reservation::reservationCounter = 0;