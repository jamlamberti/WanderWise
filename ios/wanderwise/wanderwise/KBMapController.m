//
//  KBMapController.m
//  wanderwise
//
//  Created by Kurt DaCosta on 2015-01-17.
//  Copyright (c) 2015 kurtbardd. All rights reserved.
//

#import "KBMapController.h"
#import "KBDirectionStep.h"
#import <AVFoundation/AVFoundation.h>

typedef NS_ENUM(NSUInteger, DirectionState) {
    kFindStartingPosition,
    kStarted,
    kFinalDestination,
    kArrived
};

@interface KBMapController ()

@property (strong, nonatomic) NSArray* steps;
@property (nonatomic) NSInteger currentSegmentIdx;
@property (nonatomic) DirectionState currentState;
@property (strong, nonatomic) NSMutableArray* segments;
@property (strong, nonatomic) AVSpeechSynthesizer *synth;
@property (strong, nonatomic) IBOutlet MKMapView *mapView;
@property (strong, nonatomic) IBOutlet UIButton *mapButton;
@property (strong, nonatomic) CLLocationManager *locationManager;

@end

@implementation KBMapController

- (instancetype)initWithDirectionSteps:(NSArray *)steps
{
    self = [super init];
    if (self) {
        self.steps = steps;
        self.synth = [[AVSpeechSynthesizer alloc]init];
        self.segments = [[NSMutableArray alloc] init];
        self.currentState = kFindStartingPosition;
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self.mapView setShowsUserLocation:YES];
    [self setLocationManager:[[CLLocationManager alloc] init]];
    [self.locationManager setDelegate:self];
    [self.locationManager setDistanceFilter:kCLDistanceFilterNone];
    [self.locationManager setDesiredAccuracy:kCLLocationAccuracyBest];
    
    [self.mapButton addTarget:self action:@selector(mapButtonClicked) forControlEvents:UIControlEventTouchUpInside];
    if (self.currentState == kFindStartingPosition) [self.mapButton setTitle:@"Start GPS Tracking" forState:UIControlStateNormal];
    
    for (KBDirectionStep *step in self.steps) {
        CLLocation *start = [[CLLocation alloc]initWithLatitude:[step.startLocation[@"lat"] floatValue] longitude:[step.startLocation[@"lng"] floatValue]];
        CLLocation *end = [[CLLocation alloc]initWithLatitude:[step.endLocation[@"lat"] floatValue] longitude:[step.endLocation[@"lng"] floatValue]];
        NSMutableDictionary *dict =  [[NSMutableDictionary alloc] init];
        dict[@"start"] = start;
        dict[@"end"] = end;
        dict[@"directionStep"] = step;
        NSLog(@"%@", step.arrival);
        NSLog(@"%@", dict);
        [self.segments addObject:dict];
    }
}

- (void)mapButtonClicked
{
    switch (self.currentState) {
        case kFindStartingPosition: {
            self.currentSegmentIdx = 0;
            [self.locationManager startUpdatingLocation];
            [self.mapButton setUserInteractionEnabled:FALSE];
            KBDirectionStep *step = (KBDirectionStep *)[self.segments[self.currentSegmentIdx] objectForKey:@"directionStep"];
            [self.mapButton setTitle:step.instructionString forState:UIControlStateNormal];
            break;
        }
        case kStarted:
            //
            break;
        case kFinalDestination:
            //
            break;
        case kArrived:
            //
            break;
        default:
            break;
    }
}

#pragma mark - CLLocationManager delgate
- (void)locationManager:(CLLocationManager *)manager didUpdateLocations:(NSArray *)locations{
    CLLocation *location = [locations firstObject];

    if (self.currentState == kFindStartingPosition) {
        CLLocation *startLocation = [self.segments[self.currentSegmentIdx] objectForKey:@"start"];
        CLLocationDistance distance = [location distanceFromLocation:startLocation];
        if (distance < 10.0) {
            NSLog(@"Close to Starting Point");
            self.currentState = kStarted;
//            self.currentSegmentIdx++;
            KBDirectionStep *step = (KBDirectionStep *)[self.segments[self.currentSegmentIdx] objectForKey:@"directionStep"];
            NSLog(@"%@", step.instructionString);
        } else {
            NSLog(@"%f meters away from starting point", distance);
        }
    }
    

    if (self.currentState == kStarted) {
        CLLocation *startLocation = [self.segments[self.currentSegmentIdx] objectForKey:@"end"];
        CLLocationDistance distance = [location distanceFromLocation:startLocation];
        if (distance < 10.0) {
            NSLog(@"Close to End Point");
            [self goToNextSegment];
        } else {
            NSLog(@"%f meters away from end point", distance);
        }
    }
    
    if (self.currentState == kFinalDestination) {
        CLLocation *startLocation = [self.segments[self.currentSegmentIdx] objectForKey:@"end"];
        CLLocationDistance distance = [location distanceFromLocation:startLocation];
        if (distance < 10.0) {
            NSLog(@"Close to Final Destination");
            [self goToNextSegment];
        } else {
            NSLog(@"%f meters away from final destination", distance);
        }
    }
}

- (void)goToNextSegment
{
    if (self.currentState == kFinalDestination) {
        NSLog(@"You have reached your final destination");
        return;
    }
    
    self.currentSegmentIdx++;
    KBDirectionStep *step = (KBDirectionStep *)[self.segments[self.currentSegmentIdx] objectForKey:@"directionStep"];
    NSLog(@"%@", step.instructionString);

    if (step.arrival) {
        self.currentState = kFinalDestination;
        NSLog(@"has arrival property");
        NSLog(@"%@", step.arrival);
    }
}

@end
