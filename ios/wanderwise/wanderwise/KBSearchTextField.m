//
//  KBSearchTextField.m
//  dictionary
//
//  Created by Kurt DaCosta on 2014-12-03.
//  Copyright (c) 2014 kurtbardd. All rights reserved.
//

#import "KBSearchTextField.h"

@implementation KBSearchTextField

- (id)initWithFrame:(CGRect)frame
{
    if (self = [super initWithFrame:frame]) [self commonInit];
    return self;
}

- (instancetype)initWithCoder:(NSCoder *)aDecoder
{
    if (self = [super initWithCoder:aDecoder]) [self commonInit];
    return self;
}

- (void)commonInit
{
    [self setTintColor:[self buildColorWithRed:242 green:242 blue:242]];
    [self setClearButtonMode:UITextFieldViewModeWhileEditing];
    [self setFont:[UIFont fontWithName:@"HelveticaNeue" size:16]];
    [self setTextColor:[self buildColorWithRed:242 green:242 blue:242]];
    
    UIButton *clearBtn = [self valueForKey:@"_clearButton"];
    [clearBtn setImage:[UIImage imageNamed:@"clearButton"] forState:UIControlStateNormal];
    [clearBtn setImage:[UIImage imageNamed:@"clearButtonPressed"] forState:UIControlStateHighlighted];
    
    CALayer *bottomBorder = [CALayer layer];
    bottomBorder.frame = CGRectMake(0.0f, self.frame.size.height - 1, self.frame.size.width, 1.0f);
    [bottomBorder setBackgroundColor:[self buildColorWithRed:242 green:242 blue:242].CGColor];
    [self.layer addSublayer:bottomBorder];
}

- (UIColor *)buildColorWithRed:(CGFloat)red
                         green:(CGFloat)green
                          blue:(CGFloat)blue
{
    return [UIColor colorWithRed:red/255.0 green:green/255.0 blue:blue/255.0 alpha:1.0];
}


@end
