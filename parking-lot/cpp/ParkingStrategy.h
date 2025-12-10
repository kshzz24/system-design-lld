#pragma once
#include "ParkingSpot.h"
#include <vector>
#include <limits>
using namespace std;

class ParkingStrategy
{
public:
    virtual ~ParkingStrategy() = default;
    virtual ParkingSpot *findSpot(vector<ParkingSpot *> &spots, Vehicle *vehicle) = 0;
    virtual string getName() const = 0;
};

class NearestFirstStrategy : public ParkingStrategy
{
public:
    ParkingSpot *findSpot(vector<ParkingSpot *> &spots, Vehicle *vehicle) override
    {
        ParkingSpot *nearest = nullptr;
        double minDistance = numeric_limits<double>::max();

        for (auto &spot : spots)
        {
            if (spot->isAvailable() && spot->canFitVehicle(vehicle))
            {
                double spotDistance = spot->getDistance();
                if (spotDistance < minDistance)
                {
                    minDistance = spotDistance;
                    nearest = spot;
                }
            }
        }
        return nearest;
    }

    string getName() const override
    {
        return "Nearest First";
    }
};

class BestFitStrategy : public ParkingStrategy
{
private:
    int getSpotScore(string category) const
    {
        if (category == "Bike")
            return 1;
        if (category == "Compact")
            return 2;
        if (category == "Handicapped")
            return 3;
        if (category == "Electric")
            return 4;
        if (category == "Large")
            return 5;
        return 10;
    }

public:
    ParkingSpot *findSpot(vector<ParkingSpot *> &spots, Vehicle *vehicle) override
    {
        ParkingSpot *bestFit = nullptr;
        int minScore = numeric_limits<int>::max();

        for (auto &spot : spots)
        {
            if (spot->isAvailable() && spot->canFitVehicle(vehicle))
            {
                int spotScore = getSpotScore(spot->getSpotCategory());

                if (spotScore < minScore)
                {
                    minScore = spotScore;
                    bestFit = spot;
                }
            }
        }

        return bestFit;
    }

    string getName() const override
    {
        return "Best Fit";
    }
};

class FarthestFirstStrategy : public ParkingStrategy
{
public:
    ParkingSpot *findSpot(vector<ParkingSpot *> &spots, Vehicle *vehicle) override
    {
        ParkingSpot *farthest = nullptr;
        double maxDistance = 0.0;

        for (auto &spot : spots)
        {
            if (spot->isAvailable() && spot->canFitVehicle(vehicle))
            {
                double spotDistance = spot->getDistance();
                if (spotDistance > maxDistance)
                {
                    maxDistance = spotDistance;
                    farthest = spot;
                }
            }
        }
        return farthest;
    }

    string getName() const override
    {
        return "Farthest First";
    }
};