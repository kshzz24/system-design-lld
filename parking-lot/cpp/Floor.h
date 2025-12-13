#pragma once
#include "ParkingSpot.h"
#include <vector>
#include <map>
#include <iostream>
using namespace std;

class Floor
{
private:
    int floorNumber;
    vector<ParkingSpot *> allSpots;

public:
    Floor(int number) : floorNumber(number) {}
    ~Floor()
    {
        for (auto spot : allSpots)
        {
            delete spot;
        }
    }
    void addSpot(ParkingSpot *spot)
    {
        allSpots.push_back(spot);
    }
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
    int getFloorNumber() const
    {
        return floorNumber;
    }

    void displayStatus() const
    {
        cout << "\n--- Floor " << floorNumber << " ---\n";
        int total = allSpots.size();
        int available = getTotalAvailableSpots();
        cout << "Total: " << total << " | Available: " << available << "\n";
    }
};