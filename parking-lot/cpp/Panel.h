// Panel.h
// Represents entry and exit panels in the parking lot
// Association: Each panel is associated with a Floor
// Purpose: Entry/Exit points for the parking system (expandable for future features)

#pragma once
#include "Floor.h"
using namespace std;

/**
 * EntryPanel - Represents an entry point to the parking lot
 * Association: Associated with a specific Floor
 * Future: Can be extended to handle ticket dispensing, access control
 */
class EntryPanel
{
private:
    static int panelCounter; // Auto-incrementing panel ID
    int panelId;
    Floor *floor;            // Which floor this panel is on (Association)

public:
    EntryPanel(Floor *f) : floor(f), panelId(++panelCounter) {}

    int getId() const { return panelId; }
    Floor *getFloor() const { return floor; }
};

int EntryPanel::panelCounter = 0;

/**
 * ExitPanel - Represents an exit point from the parking lot
 * Association: Associated with a specific Floor
 * Future: Can be extended to handle payment processing, barrier control
 */
class ExitPanel
{
private:
    static int panelCounter; // Auto-incrementing panel ID
    int panelId;
    Floor *floor;            // Which floor this panel is on (Association)

public:
    ExitPanel(Floor *f) : floor(f), panelId(++panelCounter) {}

    int getId() const { return panelId; }
    Floor *getFloor() const { return floor; }
};

int ExitPanel::panelCounter = 0;