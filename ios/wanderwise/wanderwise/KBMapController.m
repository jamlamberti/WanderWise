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
#import "AsyncUdpSocket.h"
#import "GCDAsyncUdpSocket.h"
//#import "GCDAsyncSocket.h"

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
@property (strong, nonatomic) NSInputStream *inputStream;
@property (strong, nonatomic) NSOutputStream *outputStream;

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
        
        [self.navigationController.navigationBar setTranslucent:YES];
        [[UINavigationBar appearance] setTintColor:[self buildColorWithRed:242 green:242 blue:242]];
        [[UINavigationBar appearance] setBarStyle:UIBarStyleBlack];
        [[UINavigationBar appearance] setBarTintColor:[self buildColorWithRed:0 green:203 blue:248]];
        [[UINavigationBar appearance] setTitleTextAttributes:@{NSFontAttributeName:[UIFont fontWithName:@"HelveticaNeue-Bold" size:22.0],
                                                               NSForegroundColorAttributeName:[self buildColorWithRed:242 green:242 blue:242]}];
        [[UIBarButtonItem appearance] setTitleTextAttributes:@{NSFontAttributeName:[UIFont fontWithName:@"HelveticaNeue-Light" size:14],
                                                               NSForegroundColorAttributeName:[self buildColorWithRed:242 green:242 blue:242]}
                                                    forState:UIControlStateNormal];
        
    }
    return self;
}

- (void)speakTest:(NSString *)text
{
    AVSpeechUtterance *utterance = [[AVSpeechUtterance alloc] initWithString:text];
    utterance.rate = 0.2;
    utterance.voice = [AVSpeechSynthesisVoice voiceWithLanguage:@"en-US"];
    [self.synth speakUtterance:utterance];
}

-(UIStatusBarStyle)preferredStatusBarStyle{
    return UIStatusBarStyleLightContent;
}


- (UIColor *)buildColorWithRed:(CGFloat)red
                         green:(CGFloat)green
                          blue:(CGFloat)blue
{
    return [UIColor colorWithRed:red/255.0 green:green/255.0 blue:blue/255.0 alpha:1.0];
}

- (void)initNetworkCommunication {
    CFReadStreamRef readStream;
    CFWriteStreamRef writeStream;
    CFStreamCreatePairWithSocketToHost(NULL, (CFStringRef)@"158.130.161.107", 9999, &readStream, &writeStream);
    self.inputStream = (__bridge NSInputStream *)readStream;
    self.outputStream = (__bridge NSOutputStream *)writeStream;
    [self.inputStream setDelegate:self];
    [self.outputStream setDelegate:self];
    [self.inputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
    [self.outputStream scheduleInRunLoop:[NSRunLoop currentRunLoop] forMode:NSDefaultRunLoopMode];
    [self.inputStream open];
    [self.outputStream open];
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self setNeedsStatusBarAppearanceUpdate];
    [self initNetworkCommunication];
    
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
    if (self.currentState == kFindStartingPosition) {
        self.currentSegmentIdx = 0;
        [self.locationManager startUpdatingLocation];
        [self.mapButton setUserInteractionEnabled:FALSE];
        [self.mapButton setTitle:@"Head to starting position." forState:UIControlStateNormal];
    }
}

#pragma mark - CLLocationManager delgate
- (void)locationManager:(CLLocationManager *)manager didUpdateLocations:(NSArray *)locations{
    CLLocation *location = [locations firstObject];

    if (self.currentState == kFindStartingPosition) {
        CLLocation *startLocation = [self.segments[self.currentSegmentIdx] objectForKey:@"start"];
        CLLocationDistance distance = [location distanceFromLocation:startLocation];
        if (distance < 10.0) {
            NSLog(@"At Starting Position");
            self.currentState = kStarted;
            KBDirectionStep *step = (KBDirectionStep *)[self.segments[self.currentSegmentIdx] objectForKey:@"directionStep"];
            [self.mapButton setTitle:step.instructionString forState:UIControlStateNormal];
            NSLog(@"%@", step.instructionString);
            [self speakTest:step.instructionString];
            [self sendStringOverSockets:[NSString stringWithFormat:@"Turn: %@", step.maneuverDirection]];
        } else {
            NSLog(@"Starting Point Distance: %f", distance);
        }
    }
    

    if (self.currentState == kStarted) {
        CLLocation *startLocation = [self.segments[self.currentSegmentIdx] objectForKey:@"end"];
        CLLocationDistance distance = [location distanceFromLocation:startLocation];
        if (distance < 10.0) {
            NSLog(@"At Segment End, Loading Next Segment");
            [self goToNextSegment];
        } else {
            NSLog(@"Segment End Distance: %f", distance);
        }
    }
    
    if (self.currentState == kFinalDestination) {
        CLLocation *startLocation = [self.segments[self.currentSegmentIdx] objectForKey:@"end"];
        CLLocationDistance distance = [location distanceFromLocation:startLocation];
        if (distance < 10.0) {
            NSLog(@"Close to Final Destination");
            [self goToNextSegment];
        } else {
            NSLog(@"Final Destination Distance: %f", distance);
        }
    }
}

- (void)goToNextSegment
{
    if (self.currentState == kFinalDestination) {
        NSLog(@"You Have Reached Your Final Destination.");
        [self sendStringOverSockets:@"Arrived"];
        return;
    }
    
    self.currentSegmentIdx++;
    KBDirectionStep *step = (KBDirectionStep *)[self.segments[self.currentSegmentIdx] objectForKey:@"directionStep"];
    [self.mapButton setTitle:step.instructionString forState:UIControlStateNormal];
    NSLog(@"%@", step.instructionString);
    [self speakTest:step.instructionString];
    [self sendStringOverSockets:[NSString stringWithFormat:@"Turn: %@", step.maneuverDirection]];
    
    if (step.arrival || self.currentSegmentIdx == self.segments.count-1) {
        self.currentState = kFinalDestination;
        NSLog(@"Final Segment Of Directions");
        if (step.arrival) {
            [self speakTest:step.arrival];
            return NSLog(@"%@", step.arrival);
        }
        //  send final destination location left or right to sockets or that this is the final segment
    }
}

- (void)sendStringOverSockets:(NSString *)string
{
	NSData *data = [[NSData alloc] initWithData:[string dataUsingEncoding:NSASCIIStringEncoding]];
	[self.outputStream write:[data bytes] maxLength:[data length]];
}

@end
