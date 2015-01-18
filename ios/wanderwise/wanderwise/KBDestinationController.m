//
//  KBDestinationController.m
//  wanderwise
//
//  Created by Kurt DaCosta on 2015-01-17.
//  Copyright (c) 2015 kurtbardd. All rights reserved.
//

#import "KBDestinationController.h"
#import "KBDirectionStep.h"
#import "KBMapController.h"
#import "KBSearchTextField.h"
@interface KBDestinationController ()

@property (nonatomic, strong) IBOutlet KBSearchTextField *origin;
@property (nonatomic, strong) IBOutlet KBSearchTextField *destination;
@property (nonatomic, strong) KBAPI *api;
@property (nonatomic, strong) NSArray *maneuvers;
@property (nonatomic, strong) NSArray *directions;
@property (nonatomic, strong) NSArray *prepostions;
@property (strong, nonatomic) NSInputStream *inputStream;
@property (strong, nonatomic) NSOutputStream *outputStream;


@end

@implementation KBDestinationController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    if (self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil]) {
        self.api = [[KBAPI alloc] init];
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self initNetworkCommunication];
    [self setNeedsStatusBarAppearanceUpdate];
    [self.origin setDelegate:self];
    [self.destination setDelegate:self];
    [self.view addGestureRecognizer:[[UITapGestureRecognizer alloc] initWithTarget:self.view
                                                                            action:@selector(endEditing:)]];
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

-(UIStatusBarStyle)preferredStatusBarStyle{
    return UIStatusBarStyleLightContent;
}

- (void)viewWillAppear:(BOOL)animated {
    [self.navigationController setNavigationBarHidden:YES animated:animated];
    [super viewWillAppear:animated];
}

- (void)viewWillDisappear:(BOOL)animated {
    [self.navigationController setNavigationBarHidden:NO animated:animated];
    [super viewWillDisappear:animated];
}

- (BOOL)textFieldShouldReturn:(UITextField *)textField
{
    if ([textField isEqual:self.origin]) {
        return [self.destination becomeFirstResponder];
    }
    [textField resignFirstResponder];
    return NO;
}

- (IBAction)testRoute {
    self.origin.text = @"3312 Walnut St, Philadelphia, PA 19104";
    self.destination.text = @"240 S 33rd St, Philadelphia, PA 19104";
}

- (IBAction)simulateLeft {
    [self sendStringOverSockets:@"Turn: Left"];    
}

- (IBAction)simulateRight:(id)sender {
    [self sendStringOverSockets:@"Turn: Right"];
}

- (void)sendStringOverSockets:(NSString *)string
{
	NSData *data = [[NSData alloc] initWithData:[string dataUsingEncoding:NSASCIIStringEncoding]];
	[self.outputStream write:[data bytes] maxLength:[data length]];
}

- (IBAction)getDirections
{
    [self.view endEditing:YES];
    if (!(self.origin.text.length && self.destination.text.length)) return;
    [self.api getGoogleDirectionsToDestination:self.destination.text
                                    fromOrigin:self.origin.text
                         withCompletionHandler:^(id response, NSError *error) {
                             if (error) return [self showAnError];
                             NSArray *directionSteps = [self parseRouteResponse:response];
                             if (directionSteps) {
                                 [self.navigationController pushViewController:[[KBMapController alloc]initWithDirectionSteps:directionSteps] animated:YES];
                             }
                         }];
}

- (void)showAnError
{
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Error"
                                                    message:@"Looks like something went wrong :("
                                                   delegate:nil
                                          cancelButtonTitle:@"Ok"
                                          otherButtonTitles: nil];
    return [alert show];
}

// returns array of steps to follow
- (NSArray *)parseRouteResponse:(NSDictionary *)response
{
    NSMutableArray *directionSteps = [[NSMutableArray alloc] init];
    NSArray *steps = response[@"steps"];
    if (!(steps && steps.count > 0)) return nil;
    for (NSDictionary *step in steps) {
        NSString *instruction = step[@"html_instructions"];
        NSString *destinationLocation;
        NSRegularExpression *divRegex = [NSRegularExpression regularExpressionWithPattern:@"</? *div[^>]*>" options:0 error:nil];
        NSArray *matchingDivRanges = [divRegex matchesInString:instruction options:0 range:NSMakeRange(0, [instruction length])];
        if (matchingDivRanges.count == 2) { //has div regex
            NSTextCheckingResult *firstMatch = matchingDivRanges[0];
            destinationLocation = [instruction substringFromIndex:firstMatch.range.location + firstMatch.range.length];
            destinationLocation = [destinationLocation substringToIndex:destinationLocation.length-6];
        }
        
        NSRegularExpression *elementRegex = [NSRegularExpression regularExpressionWithPattern:@"<[^>]*>" options:0 error:nil];
        instruction = [elementRegex stringByReplacingMatchesInString:instruction options:0 range:NSMakeRange(0, instruction.length) withTemplate:@""];
        if (destinationLocation) {
            NSRange destRange = [instruction rangeOfString:destinationLocation];
            instruction = [instruction substringToIndex:destRange.location];
        }
        
        NSMutableDictionary *dict = [[NSMutableDictionary alloc] init];
        dict[@"startLocation"] = step[@"start_location"];
        dict[@"endLocation"] = step[@"end_location"];
        NSArray *instructionParts = [[instruction uppercaseString] componentsSeparatedByString:@" "];
        if ([instructionParts containsObject:@"HEAD"]) {
            dict[@"maneuver"] = instructionParts[[instructionParts indexOfObject:@"HEAD"]];
        }
        if ([instructionParts containsObject:@"TURN"]) {
            dict[@"maneuver"] = instructionParts[[instructionParts indexOfObject:@"TURN"]];
        }
        if ([instructionParts containsObject:@"LEFT"]) {
            dict[@"maneuverDirection"] = instructionParts[[instructionParts indexOfObject:@"LEFT"]];
        }
        if ([instructionParts containsObject:@"RIGHT"]) {
            dict[@"maneuverDirection"] = instructionParts[[instructionParts indexOfObject:@"RIGHT"]];
        }
        if ([instructionParts containsObject:@"EAST"]) {
            dict[@"maneuverDirection"] = instructionParts[[instructionParts indexOfObject:@"EAST"]];
        }
        if ([instructionParts containsObject:@"WEST"]) {
            dict[@"maneuverDirection"] = instructionParts[[instructionParts indexOfObject:@"WEST"]];
        }
        if ([instructionParts containsObject:@"NORTH"]) {
            dict[@"maneuverDirection"] = instructionParts[[instructionParts indexOfObject:@"NORTH"]];
        }
        if ([instructionParts containsObject:@"SOUTH"]) {
            dict[@"maneuverDirection"] = instructionParts[[instructionParts indexOfObject:@"SOUTH"]];
        }
        if ([instructionParts containsObject:@"NORTHWEST"]) {
            dict[@"maneuverDirection"] = instructionParts[[instructionParts indexOfObject:@"NORTHWEST"]];
        }
        if ([instructionParts containsObject:@"NORTHEAST"]) {
            dict[@"maneuverDirection"] = instructionParts[[instructionParts indexOfObject:@"NORTHEAST"]];
        }
        if ([instructionParts containsObject:@"ON"]) {
            dict[@"maneuverPrepostion"] = instructionParts[[instructionParts indexOfObject:@"ON"]];
        }
        if ([instructionParts containsObject:@"ONTO"]) {
            dict[@"maneuverPrepostion"] = instructionParts[[instructionParts indexOfObject:@"ONTO"]];
        }
        if ([instructionParts containsObject:@"TOWARD"]) {
            if (!dict[@"maneuverPrepostion"]) {
                dict[@"maneuverPrepostion"] = instructionParts[[instructionParts indexOfObject:@"TOWARD"]];
            }else {
                dict[@"heading"] = instructionParts[[instructionParts indexOfObject:@"TOWARD"]];
            }
        }
        
        if (dict[@"heading"]) {
            NSInteger indexOfManeuverPrepostion = [instructionParts indexOfObject:dict[@"maneuverPrepostion"]];
            NSInteger indexOfHeading = [instructionParts indexOfObject:dict[@"heading"]];
            NSIndexSet *maneuverSet = [NSIndexSet indexSetWithIndexesInRange:NSMakeRange(indexOfManeuverPrepostion+1, indexOfHeading - 1 -indexOfManeuverPrepostion)];
            NSIndexSet *headingSet = [NSIndexSet indexSetWithIndexesInRange:NSMakeRange(indexOfHeading+1, instructionParts.count-1-indexOfHeading)];
            if (!dict[@"heading"]) {
                dict[@"headingStreet"] = [[instructionParts objectsAtIndexes:headingSet] componentsJoinedByString:@" "];
            } else {
                dict[@"maneuverStreet"] = [[instructionParts objectsAtIndexes:maneuverSet] componentsJoinedByString:@" "];
                dict[@"headingStreet"] = [[instructionParts objectsAtIndexes:headingSet] componentsJoinedByString:@" "];
            }
        } else {
            NSInteger indexOfManeuverPrepostion = [instructionParts indexOfObject:dict[@"maneuverPrepostion"]];
            NSIndexSet *maneuverSet = [NSIndexSet indexSetWithIndexesInRange:NSMakeRange(indexOfManeuverPrepostion+1, instructionParts.count - 1 -indexOfManeuverPrepostion)];
            dict[@"maneuverStreet"] = [[instructionParts objectsAtIndexes:maneuverSet] componentsJoinedByString:@" "];
        }
        
        if ([instructionParts containsObject:@"DESTINATION"]) {
            dict[@"arrival"] = instructionParts[[instructionParts indexOfObject:@"TOWARD"]];
        }
        
        if (destinationLocation) {
            dict[@"arrival"] = destinationLocation;
            dict[@"arrivalLocation"] = [[destinationLocation componentsSeparatedByString:@" "] lastObject];
        }
        
        dict[@"instructionString"] = instruction;
//        NSLog(@"%@", instruction);
        NSLog(@"%@", dict);
        [directionSteps addObject:[[KBDirectionStep alloc] initWithData:dict]];
    }
    return directionSteps;
}


@end
