// Floor.h
// Represents a floor in the parking lot containing multiple parking spots
// Composition: Floor owns and manages multiple ParkingSpots
// Purpose: Organizes parking spots by floor level

#pragma once
#include "ParkingSpot.h"
#include <vector>
#include <map>
#include <iostream>
using namespace std;

/**
 * Floor - Represents one level of the parking lot
 * Composition: Owns multiple ParkingSpots (creates and destroys them)
 * Provides aggregate operations like counting available spots
 */
class Floor
{
private:
    int floorNumber;                  // Floor identifier (1, 2, 3, ...)
    vector<ParkingSpot *> allSpots;   // All spots on this floor (Composition)

public:
    Floor(int number) : floorNumber(number) {}

    // Destructor - Clean up all owned parking spots
    ~Floor()
    {
        for (auto spot : allSpots)
        {
            delete spot;
        }
    }

    // Add a parking spot to this floor
    void addSpot(ParkingSpot *spot)
    {
        allSpots.push_back(spot);
    }

    /**
     * Get all available (unoccupied and unreserved) spots on this floor
     * Used by ParkingLot to find available spots
     */
    vector<ParkingSpot *> getAllAvailableSpots()
    {
        vector<ParkingSpot *> allAvailableSpots;
        for (auto &spot : allSpots)
        {
            if (spot->isAvailable())
            {
                allAvailableSpots.push_back(spot);
            }
        }
        return allAvailableSpots;
    }

    // Count how many spots are currently available
    int getTotalAvailableSpots() const
    {
        int count = 0;
        for (auto &spot : allSpots)
        {
            if (spot->isAvailable())
            {
                count++;
            }
        }
        return count;
    }

    int getFloorNumber() const { return floorNumber; }

    // Display floor status (total vs available spots)
    void displayStatus() const
    {
        cout << "\n--- Floor " << floorNumber << " ---\n";
        int total = allSpots.size();
        int available = getTotalAvailableSpots();
        cout << "Total: " << total << " | Available: " << available << "\n";
    }
};