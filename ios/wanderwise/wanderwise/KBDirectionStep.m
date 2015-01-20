//
//  KBDirectionStep.m
//  wanderwise
//
//  Created by Kurt DaCosta on 2015-01-17.
//  Copyright (c) 2015 kurtbardd. All rights reserved.
//

#import "KBDirectionStep.h"

@implementation KBDirectionStep

- (instancetype)initWithData:(NSMutableDictionary *)data
{
    self = [super init];
    if (self) {
        self.maneuver = data[@"maneuver"];
        self.maneuverDirection = data[@"maneuverDirection"];
        self.maneuverPrepostion = data[@"maneuverPrepostion"];
        self.maneuverStreet = data[@"maneuverStreet"];
        self.heading = data[@"heading"];
        self.headingStreet = data[@"headingStreet"];
        self.arrival = data[@"arrival"];
        self.arrivalLocation = data[@"arrivalLocation"];
        self.instructionString = data[@"instructionString"];
        self.startLocation = data[@"startLocation"];
        self.endLocation = data[@"endLocation"];
    }
    return self;
}

@end
