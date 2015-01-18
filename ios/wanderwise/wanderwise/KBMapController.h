//
//  KBMapController.h
//  wanderwise
//
//  Created by Kurt DaCosta on 2015-01-17.
//  Copyright (c) 2015 kurtbardd. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <MapKit/MapKit.h>
#import <CoreLocation/CoreLocation.h>

@interface KBMapController : UIViewController <CLLocationManagerDelegate, MKMapViewDelegate, NSStreamDelegate>

- (instancetype)initWithDirectionSteps:(NSArray *)steps;

@end
