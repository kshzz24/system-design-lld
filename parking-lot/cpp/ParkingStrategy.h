// ParkingStrategy.h
// Implements Strategy Pattern for different parking spot selection algorithms
// Pattern: Strategy Pattern
// Purpose: Allows runtime selection of different parking algorithms (Nearest, BestFit, Farthest)

#pragma once
#include "ParkingSpot.h"
#include <vector>
#include <limits>
using namespace std;

/**
 * Abstract Strategy class for parking spot selection
 * Defines the interface for different parking algorithms
 * Pattern: Strategy Pattern - allows switching algorithms at runtime
 */
class ParkingStrategy
{
public:
    virtual ~ParkingStrategy() = default;

    // Find the best parking spot based on the strategy's algorithm
    virtual ParkingSpot *findSpot(vector<ParkingSpot *> &spots, Vehicle *vehicle) = 0;

    virtual string getName() const = 0;
};

/**
 * NearestFirstStrategy - Parks vehicle in the closest available spot
 * Use case: Customer convenience, minimize walking distance
 */
class NearestFirstStrategy : public ParkingStrategy
{
public:
    ParkingSpot *findSpot(vector<ParkingSpot *> &spots, Vehicle *vehicle) override
    {
        ParkingSpot *nearest = nullptr;
        double minDistance = numeric_limits<double>::max();

        // Find the available spot with minimum distance from entry
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

    string getName() const override { return "Nearest First"; }
};

/**
 * BestFitStrategy - Parks vehicle in the most appropriate spot type
 * Use case: Optimize space utilization, save larger spots for larger vehicles
 * Lower score = more specific/restrictive spot type
 */
class BestFitStrategy : public ParkingStrategy
{
private:
    // Assign priority scores to spot types (lower = more restrictive)
    int getSpotScore(string category) const
    {
        if (category == "Bike")        return 1; // Most restrictive
        if (category == "Compact")     return 2;
        if (category == "Handicapped") return 3;
        if (category == "Electric")    return 4;
        if (category == "Large")       return 5; // Least restrictive
        return 10;
    }

public:
    ParkingSpot *findSpot(vector<ParkingSpot *> &spots, Vehicle *vehicle) override
    {
        ParkingSpot *bestFit = nullptr;
        int minScore = numeric_limits<int>::max();

        // Find the most restrictive spot that can fit this vehicle
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

    string getName() const override { return "Best Fit"; }
};

/**
 * FarthestFirstStrategy - Parks vehicle in the farthest available spot
 * Use case: Keep spots near entrance available for customers, long-term parking
 */
class FarthestFirstStrategy : public ParkingStrategy
{
public:
    ParkingSpot *findSpot(vector<ParkingSpot *> &spots, Vehicle *vehicle) override
    {
        ParkingSpot *farthest = nullptr;
        double maxDistance = 0.0;

        // Find the available spot with maximum distance from entry
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

    string getName() const override { return "Farthest First"; }
};