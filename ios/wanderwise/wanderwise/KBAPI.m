//
//  KBAPI.m
//  wanderwise
//
//  Created by Kurt DaCosta on 2015-01-17.
//  Copyright (c) 2015 kurtbardd. All rights reserved.
//

#import <AFNetworking/AFNetworking.h>
#import "KBAPI.h"

@interface KBAPI ()

@property (nonatomic, strong) NSOperationQueue *operationQueue;

@end

@implementation KBAPI

@synthesize operationQueue = _operationQueue;

- (instancetype)init
{
    return [super init];
}


- (NSOperationQueue *)operationQueue
{
    if (!_operationQueue) {
        _operationQueue = [[NSOperationQueue alloc] init];
    }
    return _operationQueue;
}


- (void)getDirectionsToDestination:(NSString *)destination
                        fromOrigin:(NSString *)origin
             withCompletionHandler:(void(^)(id response, NSError *error))handler
{
    AFHTTPRequestOperation *op =
    [self POSTOperationWithURLString:@"http://571e5e85.ngrok.com/directions"
                         parameters:@{@"origin": origin, @"destination":destination}
                            success:^(AFHTTPRequestOperation *operation, id responseObject) {
                                if (handler) handler(responseObject, nil);
                            }
                            failure:^(AFHTTPRequestOperation *operation, NSError *error) {
                                if (handler) handler(nil, error);
                            }];
    [self.operationQueue addOperation:op];
}

- (void)getGoogleDirectionsToDestination:(NSString *)destination
                              fromOrigin:(NSString *)origin
                   withCompletionHandler:(void(^)(id response, NSError *error))handler
{
    NSString *url = @"https://maps.googleapis.com/maps/api/directions/json?mode=walking";
    NSString *originParam = [NSString stringWithFormat:@"&origin=%@", [origin stringByAddingPercentEscapesUsingEncoding:NSUTF8StringEncoding]];
    NSString *destinationParam = [NSString stringWithFormat:@"&destination=%@", [destination stringByAddingPercentEscapesUsingEncoding:NSUTF8StringEncoding]];
    AFHTTPRequestOperation *op =
    [self GETOperationWithURLString:[@[url, originParam, destinationParam] componentsJoinedByString:@""]
                          parameters:nil
                             success:^(AFHTTPRequestOperation *operation, id responseObject) {
                                 if (handler) handler(responseObject[@"routes"][0][@"legs"][0], nil);
                             }
                             failure:^(AFHTTPRequestOperation *operation, NSError *error) {
                                 if (handler) handler(nil, error);
                             }];
    [self.operationQueue addOperation:op];
}


- (AFHTTPRequestOperation *)POSTOperationWithURLString:(NSString *)urlString
                                           parameters:(NSDictionary *)parameters
                                              success:(void (^)(AFHTTPRequestOperation *operation, id responseObject))success
                                              failure:(void (^)(AFHTTPRequestOperation *operation, NSError *error))failure
{
    NSMutableURLRequest *request =[[AFHTTPRequestSerializer serializer] requestWithMethod:@"POST"
                                                                                URLString:urlString
                                                                               parameters:parameters
                                                                                    error:nil];
    AFHTTPRequestOperation *operation = [[AFHTTPRequestOperation alloc] initWithRequest:request];
    operation.responseSerializer = [AFJSONResponseSerializer serializer];
    [operation setCompletionBlockWithSuccess:success failure:failure];
    return operation;
}

- (AFHTTPRequestOperation *)GETOperationWithURLString:(NSString *)urlString
                                            parameters:(NSDictionary *)parameters
                                               success:(void (^)(AFHTTPRequestOperation *operation, id responseObject))success
                                               failure:(void (^)(AFHTTPRequestOperation *operation, NSError *error))failure
{
    NSMutableURLRequest *request =[[AFHTTPRequestSerializer serializer] requestWithMethod:@"GET"
                                                                                URLString:urlString
                                                                               parameters:parameters
                                                                                    error:nil];
    AFHTTPRequestOperation *operation = [[AFHTTPRequestOperation alloc] initWithRequest:request];
    operation.responseSerializer = [AFJSONResponseSerializer serializer];
    [operation setCompletionBlockWithSuccess:success failure:failure];
    return operation;
}

@end
















