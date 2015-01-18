//
//  KBDirectionStep.h
//  wanderwise
//
//  Created by Kurt DaCosta on 2015-01-17.
//  Copyright (c) 2015 kurtbardd. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface KBDirectionStep : NSObject

@property (nonatomic, strong) NSString *maneuver;
@property (nonatomic, strong) NSString *maneuverDirection;
@property (nonatomic, strong) NSString *maneuverPrepostion;
@property (nonatomic, strong) NSString *maneuverStreet;
@property (nonatomic, strong) NSString *heading;
@property (nonatomic, strong) NSString *headingStreet;
@property (nonatomic, strong) NSString *arrival;
@property (nonatomic, strong) NSString *arrivalLocation;
@property (nonatomic, strong) NSString *instructionString;
@property (nonatomic, strong) NSDictionary *startLocation;
@property (nonatomic, strong) NSDictionary *endLocation;

- (instancetype)initWithData:(NSMutableDictionary *)data;

@end
