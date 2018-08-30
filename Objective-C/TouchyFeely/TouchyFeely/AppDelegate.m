//
//  AppDelegate.m
//  TouchyFeely
//
//  Created by Sean Kelley on 8/18/12.
//  Copyright (c) 2012 Sean Kelley. All rights reserved.
//

#import "AppDelegate.h"
#import "EventInterceptor.h"

@implementation AppDelegate

- (void)dealloc
{
    [super dealloc];
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    createEventTap();
}

@end
