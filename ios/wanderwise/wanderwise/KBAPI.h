//
//  KBAPI.h
//  wanderwise
//
//  Created by Kurt DaCosta on 2015-01-17.
//  Copyright (c) 2015 kurtbardd. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface KBAPI : NSObject

- (void)getDirectionsToDestination:(NSString *)destination
                        fromOrigin:(NSString *)origin
             withCompletionHandler:(void(^)(id response, NSError *error))handler;

@end
