//
//  EventInterceptor.m
//  TouchyFeely
//
//  Created by Sean Kelley on 8/18/12.
//  Copyright (c) 2012 Sean Kelley. All rights reserved.
//

#import "EventInterceptor.h"

#import <ApplicationServices/ApplicationServices.h>

//the CGEvent callback that does the heavy lifting
CGEventRef myCGEventCallback(CGEventTapProxy proxy, CGEventType type, CGEventRef theEvent, void *refcon) {
    NSLog(@"type: %d", type);
    //handle the event here
    //if you want to capture the event and prevent it propagating as normal, return NULL.
    
    //if you want to let the event process as normal, return theEvent.
    return theEvent;
}

void createEventTap() {
    CFRunLoopSourceRef runLoopSource;
    
    // Keyboard event taps need Universal Access enabled,
    // I'm not sure about multi-touch. If necessary, this code needs to
    // be here to check whether we're allowed to attach an event tap
    if (!AXAPIEnabled()&&!AXIsProcessTrusted()) {
        // error dialog here
        NSAlert *alert = [[[NSAlert alloc] init] autorelease];
        [alert addButtonWithTitle:@"OK"];
        [alert setMessageText:@"Could not start event monitoring."];
        [alert setInformativeText:@"Please enable \"access for assistive devices\" in the Universal Access pane of System Preferences."];
        [alert runModal];
        return;
    }
    
    
    //create the event tap
    CFMachPortRef eventTap = CGEventTapCreate(kCGHIDEventTap, //this intercepts events at the lowest level, where they enter the window server
                                kCGHeadInsertEventTap,
                                kCGEventTapOptionDefault,
                                kCGEventMaskForAllEvents,
                                myCGEventCallback, //this is the callback that we receive when the event fires
                                nil);
    
    // Create a run loop source.
    runLoopSource = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, eventTap, 0);
    
    // Add to the current run loop.
    CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource, kCFRunLoopCommonModes);
    
    // Enable the event tap.
    CGEventTapEnable(eventTap, true);
}
